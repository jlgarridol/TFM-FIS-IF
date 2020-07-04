# -*- coding: utf-8 -*-

# Versión 3.0 clase posición reducida
# Autor: José Miguel Ramírez Sanz

#imports
import numpy as np
import math

#Posiciones versión 3.0 reducida
class Posicion():
    
    # param x: lista con los valores del eje x de los puntos obtenidos con detectron
    #param y: lista con los valores del eje y de los puntos obtenidos con detectron
    def __init__(self,x,y):
        self.nariz = [x[0],y[0]]
        self.hombroI=[x[5],y[5]]
        self.hombroD=[x[6],y[6]]
        self.cuello = self.calcularPuntoMedio(self.hombroI,self.hombroD)
        self.angCuelloSupI = self.calcularAuxAngulo(self.hombroI,self.cuello,self.nariz)
        self.angCuelloSupD = self.calcularAuxAngulo(self.hombroD,self.cuello,self.nariz)
        self.codoI = [x[7],y[7]]
        self.codoD = [x[8],y[8]]
        self.manoI=[x[9],y[9]]
        self.manoD = [x[10],y[10]]
        self.angCodoI = self.calcularAngulo(self.hombroI,self.codoI,self.manoI,0)
        self.angCodoD = self.calcularAngulo(self.hombroD,self.codoD,self.manoD,1)
        self.angHombroI = self.calcularAngulo(self.cuello,self.hombroI,self.codoI,0)
        self.angHombroD = self.calcularAngulo(self.cuello,self.hombroD,self.codoD,1)
        self.caderaI = [x[11],y[11]]
        self.caderaD = [x[12],y[12]]
        self.cadera = self.calcularPuntoMedio(self.caderaI,self.caderaD)
        self.rodillaI = [x[13],y[13]]
        self.rodillaD = [x[14],y[14]]
        self.angCaderaI = self.calcularAngulo(self.cadera,self.caderaI,self.rodillaI,0)
        self.angCaderaD = self.calcularAngulo(self.cadera,self.caderaD,self.rodillaD,1)
        self.angCaderaTorsoI = self.calcularAuxAngulo(self.cuello,self.cadera,self.caderaI)
        self.angCaderaTorsoD = self.calcularAuxAngulo(self.cuello,self.cadera,self.caderaD)
        self.tobilloI = [x[15],y[15]]
        self.tobilloD = [x[16],y[16]]
        self.angRodillaI = self.calcularAngulo(self.caderaI,self.rodillaI,self.tobilloI,0)
        self.angRodillaD = self.calcularAngulo(self.caderaD,self.rodillaD,self.tobilloD,1)

    #Función que permite calcular el punto medio entre dos puntos
    #param p1: punto 1
    #param p2: punto 2
    # return: punto medio    
    def calcularPuntoMedio(self,p1,p2):
        return [(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]
    
    #Función que devuelve el ángulo en 180 grados entre 3 puntos dados
    #param p1: punto 1
    #param p2: punto medio entre el punto 1 y 3
    #param p3: punto 3
    #return ángulo en 360 grados
    def calcularAuxAngulo(self,p1,p2,p3):
        v1 = self.calcularVector(p1,p2)
        v2 = self.calcularVector(p3,p2)
        uv1 = v1 / np.linalg.norm(v1)
        uv2 = v2 / np.linalg.norm(v2)
        dp = np.dot(uv1, uv2)
        if dp > 1:
            dp=1
        elif dp < -1:
            dp=-1
        return math.degrees(np.arccos(dp))
    
    #Función que permite calcular el vector entre dos puntos
    #param p1: punt 1
    #param p2: punto 2
    #return vector entre los dos puntos
    def calcularVector(self,p1,p2):
        return [p2[0]-p1[0],p2[1]-p1[1]]
    
    #Función que permite calcula una ángulo en 360 grados
    #param p1: punto 1
    #param p2: punto medio entre el punto 1 y 3
    #param p3: punto 3
    #param lado: 0 izquierdo, 1 derecho. Necesario para la comparación cunado los dos primeros puntos son una línea recta
    #return ángulo en 180 grados
    def calcularAngulo(self,p1,p2,p3,lado):
        flag=False
        ang = self.calcularAuxAngulo(p1,p2,p3)
        
        #Cuando la recta que une los dos primeros puntos es una línea vertical
        if (p2[0]-p1[0]) ==0:
            #lado derecho
            if lado:
                #Si la posicion está menos a la derecha se ha de cambiar el ángulo
                if p3[0]<p2[0]:
                    flag=True
            #lado izquierdo
            else:
                #Si la posicion está menos a la izquierda se ha de cambiar el ángulo
                if p3[0]>p2[0]:
                    flag=True
            #Cambio del ángulo
            if flag:
                ang = 360 - ang
        else:
            y = ((p2[1]-p1[1])*(p3[0]-p1[0])/(p2[0]-p1[0]))+p1[1]
            #Si está la tercera parte por encima de la recta que hacen las dos primera entonces se cambia el angulo
            if p3[1] > y:
                ang = 360 - ang
        
        return ang