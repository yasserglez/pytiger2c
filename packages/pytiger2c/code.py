# -*- coding: utf-8 -*-

"""
Clases utilizadas en la generación código C a partir de un programa Tiger.
"""

import os

from pytiger2c.errors import CodeGenerationError


class CodeGenerator(object):
    """
    Generador de código C.
    """
    
    def __init__(self, stdlib_dir=None):
        """
        Inicializa el generador de código C.
        
        @type stdlib_dir: C{str} 
        @param stdlib_dir: Ruta absoluta al directorio que contiene los archivos
            de código C con la implementación de la biblioteca standard de Tiger
            y las funciones y tipos auxiliares utilizados por PyTiger2C.
        """
        if stdlib_dir is None:
            # Assume the stdlib directory in the root of the source distribution.
            package_dir = os.path.dirname(__file__)
            stdlib_dir = os.path.join(package_dir, os.pardir, os.pardir, 'stdlib')
        self._stdlib_dir = os.path.abspath(stdlib_dir)
        
        # Prefixes of the functions and variables defined during the code generation.
        self._functions_prefix = 'function_'
        self._locals_prefix = 'local_var'
        
        # Initialize a set with the reserved keywords of the C language.
        self._init_keywords()
        
        # Global counter of local variables in the program.
        self._locals_count = 0
        
        # Structures holding the information of the functions of the C program.
        self._function_stack = []
        self._function_headers = {}
        self._function_locals = {}
        self._function_bodies = {}
        
    def _init_keywords(self):
        """
        Inicializa un conjunto con las palabras reservadas del lenguaje C. Ningún
        nombre de variable o función puede conincidir con una de estas palabras.
        """
        self._keywords = frozenset([
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
            'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 
            'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            '_Complex', '_Bool', '_Imaginary', '__asm__', '__extension__',
            '__inline__', '__typeof__',
        ])

    def define_integer(self):
        """
        Devuelve el identificador de código C que se debe utilizar para referirse
        al tipo C{int} de Tiger en el código C generado.
        
        @rtype: C{str}
        @return: Identificador de código C para este tipo.
        """
        return 'int64_t'
    
    def define_string(self):
        """
        Devuelve el identificador de código C que se debe utilizar para referirse
        al tipo C{string} de Tiger en el código C generado.
        
        @rtype: C{str}
        @return: Identificador de código C para este tipo.        
        """
        return 'struct tiger_string*'
    
    def define_struct(self):
        """
        """
        
    def define_array(self):
        """
        """

    def begin_function(self):
        """
        """
        
    def end_function(self):
        """
        Termina la definición de la función actual. Luego de que este método
        se ejecute no será posible añadir código a la definición de dicha
        función. 
        """
        self.add_statement('}')
        del self._function_stack[0]
        
    def define_local(self, code_type):
        """
        Añade la definición de una nueva variable local a la función actual.
        
        @type code_type: C{str}
        @param code_type: Identificador de código C para el tipo de la variable. 
        
        @rtype: C{str}
        @return: Nombre asignado a la variable local. Se garantiza que este
            nombre no coincida con el de otra variable local de la función.
        """
        self._locals_count += 1
        local_name = '{prefix}{number}'.format(prefix=self._locals_prefix,
                                               number=self._locals_count)
        declaration = '{type} {name};'.format(type=code_type, name=local_name) 
        func = self._function_stack[0]
        self._function_locals[func].append(declaration)
        
    def add_statement(self, statement):
        """
        Añade una instrucción al cuerpo de la función actual. Este método no realiza
        ninguna comprobación acerca de la correctitud de la instrucción, simplemente
        la añade como una nueva línea con la indentación data al cuerpo de la función.
        
        @type statement: C{str}
        @param statement: Instrucción que se debe añadir al cuerpo de la función
            actual del generador de código.
        """
        func = self._function_stack[0]
        self._function_bodies[func].append(statement)
    
    def close(self):
        """
        Termina la clase auxiliar utilizada en la generación de código. Luego de
        que se ejecute este método no es válido continuar generando código mediante
        esta clase, solamente es válido utilizar el método C{write} para escribir
        el código generado hacia un descriptor de fichero.
        
        @raise CodeGenerationError: Esta excepción se lanzará si se intenta cerrar
            el generador y existen funciones abiertas distintas de la función
            principal.
        """
        self.end_function()
        if len(self._function_stack) != 0:
            message = 'Trying to close the generator with opened functions'
            raise CodeGenerationError(message)
        
    def write(self, output_fd):
        """
        Escribe el código C generado hacia un descriptor de fichero.
        
        @type output_fd: C{file}
        @param output_fd: Descriptor de fichero donde se debe escribir el
            código C resultante de la traducción del programa Tiger.
        """
        functions_c = os.path.join(self._stdlib_dir, 'functions.c')
        includes_c = os.path.join(self._stdlib_dir, 'includes.c')
        prototypes_= os.path.join(self._stdlib_dir, 'c prototypes.c')
        types_c = os.path.join(self._stdlib_dir, 'types.c')
