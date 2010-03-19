# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo cadena de caracteres.
"""

from pytiger2c.types.tigertype import TigerType


class StringType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo cadena de caracteres.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo cadena de caracteres.
        """
        super(StringType, self).__init__()
        self._defined = True
