# -*- coding: utf-8 -*-

import sys, cv2, zlib, pickle, struct, socket, traceback
from time import sleep
from kafka import KafkaProducer
from getopt import getopt, GetoptError
from sys import argv

def help_(salida=0):
    print("Ayuda sobre el injestor de Kafka")
    print("---------------------")
    print("\t-h:\tImprime esta ayuda")
    print("Parámetros necesarios:")
    print("\t--ip=<IP de recepción> (Por defecto: localhost)")
    print("\t--port=<Puerto>")
    print("\t--kafkahost=<Dirección de kafka> (Por defecto: localhost:9092)")
    print("\t--topic=<Topic de Kafka> (Por defecto: video-stream-event)")
    sys.exit(salida)

IP = "localhost"
PORT = None
TOPIC = "video-stream-event"
KAFKA_HOST = "localhost:9092"


try:
    optlist, args = getopt(argv[1:], "h", ["ip=","port=","topic=","kafkahost="])
    for o, a in optlist:
        if o == "-h":
            help_()
        elif o == "--ip":
            IP = a
        elif o == "--port":
            PORT = int(a)
        elif o == "--topic":
            TOPIC = a
        elif o == "--kafkahost":
            KAFKA_HOST = a
        else:
            print("Parámetro",o,"no reconocido")
            help_(1)
except GetoptError as e:
    print(e)
    help_(2)

if IP is None or PORT is None or TOPIC is None:
    print("Falta algún parámetro")
    help_(1)


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind((IP,PORT))
s.listen(10)

producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")

counter = 0
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    print("Se va a emitir a Kafka el frame",counter, end="\r")
    producer.send(TOPIC, key=bytes(str(counter),'utf-8'), value=frame_data)
    producer.flush()
    counter+=1
    
