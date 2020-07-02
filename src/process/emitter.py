"""
Creación de un flujo de vídeo simulado
Por UDP
"""
from time import sleep
import cv2, socket, traceback, struct, sys, zlib, pickle
from sys import argv
from getopt import getopt, GetoptError

__author__="José Luis Garrido Labrador"

def help_(salida=0):
    print("Ayuda sobre el emisor")
    print("---------------------")
    print("\t-h:\tImprime esta ayuda")
    print("Parámetros necesarios:")
    print("\t--ip=<IP de emisión> (Por defecto: localhost)")
    print("\t--port=<Puerto>")
    print("\t--file=<fichero MP4>")
    print("Parámetros opcionales:")
    print("\t--resize=<Proporcion> (por defecto: 1.0)")
    print("\t-f <FPS> | --fps=<FPS> (por defecto: 15) tasa de frames del vídeo a emitir")
    sys.exit(salida)

IP = "localhost"
PORT = None
FILE = None
RESIZE = 1.0
FPS = 15
DF = 15

try:
    optlist, args = getopt(argv[1:], "hf:", ["ip=","port=","file=","resize=","fps="])
    for o, a in optlist:
        if o == "-h":
            help_()
        elif o == "--ip":
            IP = a
        elif o == "--port":
            PORT = int(a)
        elif o == "--file":
            FILE = a
        elif o == "--resize":
            if "/" in a:
                RESIZE = float(eval(a))
            else:
                RESIZE = float(a)
        elif o == "-f" or o == "--fps":
            if a != "":
                FPS = int(a)
            else:
                FPS = 15
        else:
            print("Parámetro",o,"no reconocido")
            help_(1)
except GetoptError as e:
    print(e)
    help_(2)

if IP is None or PORT is None or FILE is None:
    print("Falta algún parámetro")
    help_(1)

count=0
countR=0
INTERVAL = float(1/DF)

ITVREAL = float(1/FPS)

RELATION = int(DF/FPS)


sum_ = 0

if __name__ == "__main__":
    # Creamos un socket (según https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    connection = s.makefile('wb')
    
    try:
        video = cv2.VideoCapture(FILE)

        while True: 
            # El vídeo de emite siempre en bucle ya que representa
            # Un vídeo real que no pararía
            success, frame = video.read()
            if frame is not None:
                if RESIZE != 1.0:
                    frame = cv2.resize(frame, (0,0), fx=RESIZE, fy=RESIZE)

                data = zlib.compress(cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95])[1])
                sum_ += len(data)
                countR+=1 # Por cada frame leido se aumenta el contador

                emitir = True # Este frame se emite casi siempre
                while_ = 1
                if INTERVAL < ITVREAL:
                    if (countR-1)%RELATION != 0: # Se desechan frames
                        emitir = False # Solo se deja de emitir en caso de que no sea módulo de la relación
                elif INTERVAL > ITVREAL:
                    while_ = int(FPS/DS) # Se emite el mismo frame tantas veces como por encima de los 15 FPS esté el video

                for _ in range(while_):
                    if emitir:
                        count += 1 # Por cada frame emitido aumentamos el número del contador de emitidos
                        print("Se han emitido:",count,"frames.","Tamaño medio:",sum_/count,end="\r")                
                        s.sendall(struct.pack(">L", len(data)) + data)
                    if while_ > 1:
                        sleep(ITVREAL)    # Se espera la unidad menor de tiempo

                if while_ <= 1: # En caso contrario ya se habrá esperado
                    sleep(INTERVAL)
            else:
                video = cv2.VideoCapture(FILE)
            

    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception:
        traceback.print_exc()



