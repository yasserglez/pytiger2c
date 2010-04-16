# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo entero.
"""

from pytiger2c.types.basictype import BasicType


class IntegerType(BasicType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo entero
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo array.
        """
        super(IntegerType, self).__init__()
        self._code_type = 'int64_t'
