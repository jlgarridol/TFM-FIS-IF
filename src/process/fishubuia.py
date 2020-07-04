# -*- coding: utf-8 -*-

# Clase para la posicion y comparación V 1.0
# Autor: José Miguel Ramírez Sanz


# imports
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

import pandas as pd
import pickle as pk
import numpy as np
import cv2
from matplotlib import pyplot as plt
import gc
from pynvml.smi import nvidia_smi

# import de utilities de detectron
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
import torch

from PosicionVF import Posicion

#Clase que sirve de conexión con el flujo para realizar las comparaciones de las posiciones
class Interfaz():

    #Constructor en el que se puede configurar el threshold
    #param threshold: sensibilidad de detectron2 al detectar una persona
    def __init__(self,threshold=0.99):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
        self.predictor = DefaultPredictor(self.cfg)

    #Función que permite liberar la memoria para que no se colapse la memoria en las tarjetas gráficas
    def __borrarMemoria(self):
        nvsmi = nvidia_smi.getInstance()
        nvsmi.DeviceQuery('memory.free, memory.total')
        torch.cuda.empty_cache()
        gc.collect()

    #Obtener la posición y la imagen procesada de una imagen
    #param imagen: imagen a procesar
    #param codigo: 0=sin imagen; 1=imagen normal; 2=esqueleto en blanco; 3 o superior = esqueleto en negro
    def obtenerPosicion(self,imagen,codigo=0):
        #Se obtiene la predicción
        output = self.predictor(imagen)
        pkP = output.get("instances").pred_keypoints

        #Si no se encuentran los puntos lanzar excepción
        if len(pkP)==0:
            raise Exception("No se ha detectado posición")
        if len(pkP[0])==17:
            x = pkP[0][:,0].cpu().numpy()
            y = pkP[0][:,1].cpu().numpy()
            pos = Posicion(x,y)
        #Si no existen exactamente 17 puntos la posición es erronea
        else:
            raise Exception("Posición erronea")

        #Dependiendo del codigo se devuelve o no la imagen
        if codigo==0:
            self.__borrarMemoria()
            im=None
        else:
            if codigo==1:
                visualizer = Visualizer(imagen[:,:,::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
            elif codigo==2:
                visualizer = Visualizer(np.full(imagen.shape,255)[:,:,::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
            else:
                visualizer = Visualizer(np.zeros(imagen.shape)[:,:,::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
            
            vis = visualizer.draw_instance_predictions(output["instances"].to("cpu"))
            im = vis.get_image()[:, :, ::-1]
            self.__borrarMemoria()
        return pos,im
            
    
    #Función que devuelve la diferencia media en grados y en porcentaje entre los posiciones atendiendo a uno pesos por cada zona
    #param pos1: posición 1
    #param pos2: posición 2
    #param pesos: diccionario con los pesos de las distintas zonas
    #return: diferencia media en grados, porcentaje de exactitud
    @staticmethod
    def compararPosiciones(pos1,pos2,pesos={"brazos":1,"piernas":1,"torso":1}):
        zonas={"brazos":["angCodo","angHombro"],"piernas":["angRodilla","angCadera"],"torso":["angCaderaTorso","angCuelloSup"]}
        res=0
        total=0
        
        #Se recoge el peso total
        for i in pesos:
            if i not in zonas:
                raise Exception("No se puede dar peso a una zona que no esté definida")
            total+=pesos[i]
            
        #Se recorren los distintos tipos de zonas y se les aplica el peso a la comparación
        for i in zonas:
            res+=(pesos[i]/total)*comparacionZona(pos1,pos2,zonas[i])
        
        porcentaje = res*100/180
        
        return res,100-porcentaje

    #Función que permite comparar unas zonas pasadas
    #param pos1: posición 1
    #param pos2: posición 2
    #param zonas: lista de las zonas a comparar
    #return: media de la diferencia de los grados de las zonas pasadas
    @staticmethod
    def comparacionZona(pos1,pos2,zonas):
        partes=["D","I"]
        res = 0.0
        for i in partes:
            for j in zonas:
                #aux es la diferencia entre los ángulos
                aux = abs(eval("pos1."+j+i)-eval("pos2."+j+i))
                #si la diferencia es mayor de 180 grados se coge el otro lado
                if aux > 180:
                    res += (360-aux)
                else:
                    res+=aux
        return res/(len(partes)*len(zonas))
        