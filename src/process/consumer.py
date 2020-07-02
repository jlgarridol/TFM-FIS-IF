from pyspark.streaming.kafka import KafkaUtils, Broker
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
import numpy as np
import os
from getopt import getopt, GetoptError
from sys import argv
import traceback
import cv2
import pickle
import zlib, lzma
import sys
import imageProcesor as ip
from extraOpt import opt as opt_

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.5 pyspark-shell'

def help_(salida=0):
    print("Ayuda el consumidor de Kafka")
    print("---------------------")
    print("\t-h:\tImprime esta ayuda")
    print("Parámetros necesarios:")
    print("\t--topic=<Topic de Kafka> (Por defecto: video-stream-event)")
    print("\t--output=<Carpeta de salida> (Por defecto: output)")
    print("\t--kafkahost=<Dirección de kafka> (Por defecto: localhost:9092)")
    print("\t--sparkhost=<Dirección de Spark> (Por defecto: local)")
    print("Parámetros adicionales:")
    print("\t-a -> Anonimizar rostros, por defecto usa pixel")
    print("\t\t-g <Factor> | --blur=<Factor> (Por defecto: 3) -> Anonimizar con blur")
    print("\t\t-p <Factor> | --pixel=<Factor> (Por defecto: 15) -> Anonimizar con pixelado")
    print("\t-b -> Auto ajustar brillo")
    print("\t-c -> Auto ajustar contraste")
    print("\t-f <FPS> | --fps=<FPS> (Por defecto: 15) tasa de frames a procesar")
    print("\t--no-save -> No guarda los frames")
    sys.exit(salida)

TOPIC = "video-stream-event"
OUTPUT = "output"


KAFKA_HOST = "localhost:9092"
SPARK_HOST = "local"


ANONIMIZE = False
ANON_ALG = ip.pixel
ANON_FACTOR = 15
FPS = 15

SAVE = True

BRIGHT = False
CONTRAST = False

try:
    optlist, args = getopt(argv[1:], "habcg:p:f:", ["output=","topic=","blur=","pixel=","no-save","fps=","kafkahost=","sparkhost="])
    for o, a in optlist:
        if o == "-h":
            help_()
        elif o == "--topic":
            TOPIC = a
        elif o == "--output":
            OUTPUT = a
        elif o == "--blur" or o == "-g":
            if a != "":                
                ANON_FACTOR = float(a)
            else:
                ANON_FACTOR = 3
            ANON_ALG = ip.blur
        elif o == "--pixel" or o == "-p":
            if a != "":
                ANON_FACTOR = int(a)
            else:
                ANON_FACTOR = 15
            ANON_ALG = ip.pixel
        elif o == "--kafkahost":
            KAFKA_HOST = a
        elif o == "--sparkhost":
            SPARK_HOST = a
        elif o == "-f" or o == "--fps":
            if a != "":
                FPS = int(a)
            else:
                FPS = 15
        elif o == "-a":
            ANONIMIZE = True
        elif o == "-b":
            BRIGHT = True
        elif o == "-c":
            CONTRAST = True
        elif o == "--no-save":
            SAVE = False
        else:
            print("Parámetro",o,"no reconocido")
            help_(1)
except GetoptError as e:
    print(e)
    help_(2)

if TOPIC is None or OUTPUT is None:
    print("Falta algún parámetro")
    help_(1)

sc = SparkContext(SPARK_HOST, "ImageProcessor_"+TOPIC)
ssc = StreamingContext(sc, float(1/FPS))

def deserializer(file):
    file = cv2.imdecode(np.frombuffer(zlib.decompress(file), dtype=np.uint8), 1)
    return file

options = {"bootstrap.servers": KAFKA_HOST, 
           "group.id":TOPIC}

kafkaStream = KafkaUtils.createDirectStream(ssc, [TOPIC], options, valueDecoder=deserializer)

def op(package):
    k = package[0]
    img = package[1]
    if img is not None and k is not None:
        try:
            if ANONIMIZE:
                img = ip.anonimize(img, ANON_ALG, ANON_FACTOR)
            if BRIGHT or CONTRAST:
                img = ip.repair_bright_and_contrast(img, BRIGHT, CONTRAST)
            k, img = opt_(k, img)
        except:
            traceback.print_exc()
            print("Hubo un error procesando la imagen",k)
    return k, img

def save(img):
    try:
        if SAVE:
            cv2.imwrite(os.path.join(OUTPUT,str(img[0])+".jpg"), img[1])
    except:
        traceback.print_exc()
        print("Hubo un error guardando la imagen", img[0])
    return img

    

#kafkaStream.map(lambda x: print(x))
anonimizeStream = kafkaStream.map(lambda x: op(x))
anonimizeStream.map(lambda x: save(x)).pprint(0)
ssc.start()
ssc.awaitTermination()