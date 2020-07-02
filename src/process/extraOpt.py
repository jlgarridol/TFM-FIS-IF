from fishubuia import Interfaz

ia = Interfaz()

def opt(key, value):
      # Esta función es configurada manualmente por el programador
    pos, esq = ia.obtenerPosicion(value, 3)

    return key, esq