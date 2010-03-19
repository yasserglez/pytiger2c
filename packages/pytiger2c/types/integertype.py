# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo entero.
"""

from pytiger2c.types.tigertype import TigerType


class IntegerType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo entero
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo array.
        """
        super(IntegerType, self).__init__()
        self._defined = True
        