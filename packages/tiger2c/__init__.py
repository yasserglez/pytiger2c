# -*- coding: utf-8 -*-

"""
Paquete principal de Tiger2C.

Tiger2C es una implementación de un compilador del lenguaje de programación
Tiger que genera código en lenguaje C. Opcionalmente, el código C resultante 
puede ser compilado con un compilador de C para generar un ejecutable.
"""

from tiger2c.errors import Tiger2CError


__version__ = '0.1'

__authors__ = (
    'Yasser González Fernández <yglez@uh.cu>',
    'Ariel Hernández Amador <gnuaha7@uh.cu>',
)


def translate(tiger_filename, c_filename):
    """
    Traduce un programa Tiger a un programa C equivalente.
    
    @param tiger_filename: Ruta absoluta al archivo que contiene el código
        fuente del programa Tiger que se debe traducir al lenguaje C.
    @param c_filename: Ruta absoluta al archivo donde se generará el código
        C resultante. Si existe un archivo en la ruta especificada este será
        sobreescrito.
    """
    raise Tiger2CError()