# -*- coding: utf-8 -*-

from fishubuia import Interfaz
import pickle as pk

ia = Interfaz()

def opt(key, value, output="/"):
      # Esta función es configurada manualmente por el programador
    pos, esq = ia.obtenerPosicion(value, 0)
    # Hacemos un pickle de la posición
    pk.dump(pos, os.path.join(output,"pos_"+str(key))+".pickle")

    return key, esq