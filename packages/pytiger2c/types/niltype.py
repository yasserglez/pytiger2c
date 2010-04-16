# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo C{nil}.
"""

from pytiger2c.types.basictype import BasicType


class NilType(BasicType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo C{nil}.
    """

    def __init__(self):
        """
        Inicializa la clase representando el tipo C{nil}.
        """
        super(NilType, self).__init__()
        self._code_type = 'void*'
