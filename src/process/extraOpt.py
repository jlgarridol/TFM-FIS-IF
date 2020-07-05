# -*- coding: utf-8 -*-

from fishubuia import Interfaz

ia = Interfaz()

def opt(key, value):
      # Esta función es configurada manualmente por el programador
    pos, esq = ia.obtenerPosicion(value, 1)

    return key, esq