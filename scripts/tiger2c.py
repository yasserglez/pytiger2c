# -*- coding: utf-8 -*-

"""
Script para ejecutar Tiger2C desde la linea de comandos.
"""

import os
import sys
import optparse
import subprocess

# Add the directory containing the packages in the source distribution to the path.
# This should be removed when Tiger2C is installed.
PACKAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'packages'))
sys.path.insert(0, PACKAGES_DIR)

from tiger2c import __version__, __authors__, translate
from tiger2c.errors import Tiger2CError


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def _parse_args():
    """
    Reconoce las opciones especificadas como argumentos.
    """
    usage = '%prog [options] <tiger-filename> <output-filename>'
    version = '%prog (Tiger2C) {0}\n'.format(__version__)
    authors = '\n'.join(['Copyright (C) 2009 {0}'.format(a) for a in __authors__])
    desc = 'Translates a Tiger program received as argument into a C ' \
        'program and then (optionally) compiles the C program into an ' \
        'executable using a C compiler.'
    parser = optparse.OptionParser(usage=usage, version=version + authors,
                                   description=desc)
    parser.add_option('-c', '--compile', action='store_true', dest='compile',
                      help='compile the C program, generate an executable as output')
    parser.set_default('compile', False)          
    parser.add_option('-s', '--save-tmp', action='store_true', dest='save_tmp',
                      help="do not remove the C program created for compilation")
    parser.set_default('save_tmp', False)    
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error('invalid number of arguments')
    else:
        return options, args


def main():
    """
    Función principal del script.
    """
    options, args = _parse_args()
    tiger_file = os.path.abspath(args[0])
    if options.compile:
        basename = os.path.basename(tiger_file)
        index = basename.rfind('.')
        c_file = '{0}.c'.format(basename[:index] if index > 0 else basename)
        c_file = os.path.join(os.path.dirname(tiger_file), c_file)
        exec_file = os.path.abspath(args[1])
    else: 
        c_file = os.path.abspath(args[1])
    try:
        translate(tiger_file, c_file)
    except Tiger2CError, error:
        # TODO: Print information about sintantic or semantic errors.
        sys.exit(EXIT_FAILURE)
    else:
        if options.compile:
            GCC_CMD = ['gcc',  c_file, '-o', exec_file]
            if subprocess.call(GCC_CMD) != 0:
                sys.exit(EXIT_FAILURE)
            if not options.save_tmp:
                os.unlink(c_file)
        sys.exit(EXIT_SUCCESS)    


if __name__ == '__main__':
    main()