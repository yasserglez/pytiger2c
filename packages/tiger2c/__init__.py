# -*- coding: utf-8 -*-

"""Paquete principal de Tiger2C. 
"""

from tiger2c.errors import Tiger2CError


__version__ = '0.1'

__authors__ = (
    'Yasser González Fernández <yglez@uh.cu>',
    'Ariel Hernández Amador <gnuaha7@uh.cu>',
)


def translate(tiger_filename, c_filename):
    """Traduce un programa Tiger a un programa C equivalente.
    """
    raise Tiger2CError()