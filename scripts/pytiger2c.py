#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar PyTiger2C desde la linea de comandos.
"""

import os
import sys
import optparse
import subprocess

# Add the directory containing the packages in the source distribution to the path.
# This should be removed when Tiger2C is installed.
PACKAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'packages'))
sys.path.insert(0, PACKAGES_DIR)

from pytiger2c import __version__, __authors__, tiger2c, tiger2dot
from pytiger2c.errors import PyTiger2CError


EXIT_SUCCESS, EXIT_FAILURE = 0, 1


def _parse_args(argv):
    """
    Reconoce las opciones especificadas como argumentos.
    
    @type argv: C{list}
    @param argv: Lista de argumentos del programa.
    
    @rtype: C{tuple}
    @return: Retorna una tupla donde el primer elemento es una estructura
        que almacena la información acerca de las opciones especificadas
        y el segundo elemento es una lista con el resto de los argumentos.
    """
    usage = '%prog <tiger-file> --output <output-file> [--output-type <output-type>]'
    version = '%%prog (PyTiger2C) %s\n' % __version__
    authors = '\n'.join(['Copyright (C) 2009, 2010 %s' % a for a in __authors__])
    desc = 'Translates a Tiger program received as argument into a C program ' \
        'and then compiles the C program into an executable using a C compiler. ' \
        'This behavior can be modified using the --output-type option.'
    parser = optparse.OptionParser(usage=usage, 
                                   version=version + authors, 
                                   description=desc, 
                                   prog=os.path.basename(argv[0]))
    parser.add_option('-o', '--output', action='store', dest='output', metavar='FILE', 
                      help='write the output to FILE')
    parser.add_option('-t', '--output-type', action='store', dest='output_type', metavar='TYPE',
                      type='choice', choices=('ast', 'c', 'binary'),
                      help="output type: 'ast', 'c' or 'binary' (default '%default')")
    parser.set_default('output_type', 'binary')
    options, args = parser.parse_args(args=argv[1:])
    optparse.check_choice(parser.get_option('--output-type'), '--output-type', options.output_type)
    if not options.output:
        parser.error('missing required --output option')
    elif len(args) != 1:
        parser.error('invalid number of arguments')
    else:
        return options, args


def main(argv):
    """
    Función principal del script.
    
    @type argv: C{list}
    @param argv: Lista de argumentos del programa.
    
    @rtype: C{int}
    @return: Retorna 0 si no ocurrió ningún error durante la ejecución 
        del programa y 1 en el caso contrario.
    """
    options, args = _parse_args(argv)
    tiger_filename = os.path.abspath(args[0])
    output_filename = os.path.abspath(options.output)
    try:
        if options.output_type == 'ast':
            tiger2dot(tiger_filename, output_filename)
        elif options.output_type == 'c':
            tiger2c(tiger_filename, output_filename)
            # Translation completed. Beautify the code using GNU Indent.
            INDENT_CMD = ['indent', '-gnu', '-l100', '-o', output_filename, output_filename]
            if subprocess.call(INDENT_CMD) != EXIT_SUCCESS:
                # Leave the c file for debugging.
                sys.exit(EXIT_FAILURE)            
        elif options.output_type == 'binary':
            basename = os.path.basename(tiger_filename)
            index = basename.rfind('.')
            c_filename = '%s.c' % (basename[:index] if index > 0 else basename)
            c_filename = os.path.join(os.path.dirname(tiger_filename), c_filename)
            tiger2c(tiger_filename, c_filename)
            # Translation completed. Compile using GCC.
            GCC_CMD = ['gcc', '-std=c99', '-lgc', '-o', output_filename, c_filename]
            if subprocess.call(GCC_CMD) != EXIT_SUCCESS:
                # Leave the temporal c file for debugging.
                sys.exit(EXIT_FAILURE)
            os.unlink(c_filename)
    except PyTiger2CError, error:
        print >> sys.stderr, error
        sys.exit(EXIT_FAILURE)
    else:
        sys.exit(EXIT_SUCCESS)    


if __name__ == '__main__':
    main(sys.argv)