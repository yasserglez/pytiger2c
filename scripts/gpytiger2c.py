#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar la interfaz gráfica de PyTiger2C.
"""

import os
import sys


if __name__ == '__main__':
    SRC_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir)
    DATA_DIR = os.path.abspath(os.path.join(SRC_DIR, 'data'))
    PYTIGER2C_SCRIPT = os.path.abspath(os.path.join(SRC_DIR, 'scripts', 'pytiger2c.py'))
    sys.path.insert(0, os.path.abspath(os.path.join(SRC_DIR, 'packages')))
    import gpytiger2c
    gpytiger2c.main(DATA_DIR, PYTIGER2C_SCRIPT)
