# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo array.
"""

from pytiger2c.types.tigertype import TigerType


class ArrayType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo array.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo array.
        """
        super(ArrayType, self).__init__()
