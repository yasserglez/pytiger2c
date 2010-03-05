# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo record.
"""

from pytiger2c.types.tigertype import TigerType


class RecordType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo record.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo record.
        """
        super(RecordType, self).__init__()
