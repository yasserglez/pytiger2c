# -*- coding: utf-8 -*-

"""
Paquete principal de PyTiger2C.

PyTiger2C es una implementación de un compilador del lenguaje de programación
Tiger que genera código en lenguaje C. Opcionalmente, el código C resultante 
puede ser compilado con un compilador de C para generar un ejecutable.
"""

import codecs

from pytiger2c.errors import PyTiger2CError, SyntacticError, SemanticError, CodeGenerationError 


__version__ = '0.1'

__authors__ = (
    'Yasser González Fernández <yglez@uh.cu>',
    'Ariel Hernández Amador <gnuaha7@uh.cu>',
)


def syntactic_analysis(input_fd):
    """
    Realiza análisis léxico-gráfico y sintáctico. 
    
    Si se encuentra algún error de sintáxis durante el análisis del programa se lanzará
    una exepción C{SyntacticError} que contendrá información acerca del error.
    
    @type input_fd: C{file}
    @param input_fd: Descriptor de fichero del programa Tiger a traducir.
    @rtype: C{LanguageNode}
    @return: Árbol de sintáxis abstracta correspondiente al programa Tiger.
    """
    raise SyntacticError()


def check_semantics(syntax_tree):
    """
    Realiza comprobación semántica.
    
    Si se encuentra algún error semántico se lanzará una excepción C{SemanticError} que
    contendrá información acerca del error. 
    
    @type syntax_tree: C{LanguageNode}
    @param syntax_tree: Árbol de sintáxis asbtracta correspondiente a un programa Tiger.
    """
    raise SemanticError()


def generate_code(syntax_tree, output_fd):
    """
    Realiza la generación de código.
    
    Si se produce algún error durante la generación de código se lanzará una excepción
    C{CodeGenerationError} que contendrá información acerca del error.
    
    @type syntax_tree: C{LanguageNode}
    @param syntax_tree: Árbol de sintáxis asbtracta correspondiente a un programa Tiger.
    @type output_fd: C{file}
    @param output_fd: Descriptor de fichero del archivo donde se generará el programa 
        resultante de la traducción.
    """
    raise CodeGenerationError()
    

def translate(tiger_filename, c_filename):
    """
    Traduce un programa Tiger a un programa C equivalente.
    
    Se utiliza las funciones auxiliares C{syntactic_analysis}, C{check_semantics} 
    y C{generate_code} para llevar a cabo cada una de las fases de la compilación 
    del programa.

    @type tiger_filename: C{str}
    @param tiger_filename: Ruta absoluta al archivo que contiene el código
        fuente del programa Tiger que se debe traducir al lenguaje C.
    @type c_filename: C{str}
    @param c_filename: Ruta absoluta al archivo donde se generará el código
        C resultante. Si existe un archivo en la ruta especificada este será
        sobreescrito.
    """
    try:
        with codecs.open(tiger_filename, encoding='utf-8', mode='rb') as input_fd: 
            syntax_tree = syntactic_analysis(input_fd)
    except IOError:
        raise PyTiger2CError(error_msg='Could not open the Tiger input file')
    check_semantics(syntax_tree)
    try:
        with codecs.open(c_filename, encoding='utf-8', mode='wb') as output_fd:
            generate_code(syntax_tree, output_fd)
    except IOError:
        raise PyTiger2CError(error_msg='Could not open the output file')
