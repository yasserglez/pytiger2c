# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo nil.
"""

from pytiger2c.types.tigertype import TigerType


class NilType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo nil.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo nil.
        """
        super(NilType, self).__init__()
