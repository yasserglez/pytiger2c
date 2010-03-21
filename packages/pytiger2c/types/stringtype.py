# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo cadena de caracteres.
"""

from pytiger2c.types.basictype import BasicType


class StringType(BasicType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo cadena de caracteres.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo cadena de caracteres.
        """
        super(StringType, self).__init__()
