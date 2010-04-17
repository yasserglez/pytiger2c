# -*- coding: utf-8 -*-

"""
Clases utilizadas en la generación código C a partir de un programa Tiger.
"""

import os

from pytiger2c.errors import CodeGenerationError
from pytiger2c.types.functiontype import FunctionType


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
        
        # Prefixes for functions and local variables defined in the program.
        self._functions_prefix = 'function_'
        self._locals_prefix = 'local_var'
        
        # Initialize a set with the reserved keywords of the C language.
        self._init_keywords()
        
        # Used to disambiguate names of the local variables and scopes structs.
        self._locals_count = 0
        self._scopes_count = 0
        
        # Structures with the information of the parts of the code.
        self._type_defs = {}
        self._func_stack = []
        self._func_header = {}
        self._func_locals = {}
        self._func_stmts = {}
        self._func_cleanups = {}
        self._func_return = {}
        
        # Define the main function of the program.
        self._define_main()
        
    def _init_keywords(self):
        """
        Inicializa un conjunto con las palabras reservadas del lenguaje C. Ningún
        nombre de variable o función puede conincidir con una de estas palabras.
        """
        keywords = [
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'inline', 'int', 'long', 'register', 'restrict', 'return',
            'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 
            'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
            
            '_Complex', '_Bool', '_Imaginary', 
            
            '__asm__', '__extension__', '__inline__', '__typeof__',
        ]
        self._keywords = frozenset(keywords)
        
    def _define_main(self):
        """
        Define la función principal del programa C.
        """
        func_code_name = 'main'
        self._func_header[func_code_name] = 'int main()'
        self._func_locals[func_code_name] = []
        self._func_stmts[func_code_name] = []
        self._func_cleanups[func_code_name] = []
        self._func_stack.insert(0, func_code_name)
        
    def _disambiguate(self, name, container):
        """
        Comprueba si un nombre coincide con alguno que se encuentra en un grupo 
        de nombres dado, si esto sucede, modifica el nombre para que sea un 
        nombre válido.
        
        @type name: C{str}
        @param name: Nombre al que se le debe realizar la comprobación.
        
        @type container: C{object}
        @param container: Contenedor con un grupo de nombres. 
        
        @rtype: C{str}
        @return: Nombre que no coincide con ninguna palabra reservada.
        """
        while name in container:
            name += '_'
        return name
    
    def define_struct(self, name, field_names, field_code_types):
        """
        Define un nuevo tipo correspondiente a una estructura del lenguaje C.
        Se tratará de definir el nuevo tipo con el nombre especificado por el
        parámetro C{name} si este no coincide con una palabra reservada del 
        lenguaje C o un tipo definido anteriormente. De manera semejante sucede
        con cada uno de los nombres dados para los campos de la estructura
        mediante el parámetro C{field_names}. 
        
        Esta función se utiliza para generar el código de los ámbitos de ejecución 
        y de los records del lenguaje Tiger que se definan en el programa.
        
        @type name: C{str}
        @param name: Nombre que se propone para el tipo de la nueva estructura.
        
        @type field_names: C{list}
        @param field_names: Nombres que se proponen para cada uno de los campos
            de la estructura.
        
        @type field_code_types: C{list}
        @param field_code_types: Identificadores de código devueltos anteriormente
            por métodos de esta clase correspondientes a los tipos de cada uno
            de los campos de la estructura.
        
        @rtype: C{tuple}
        @return: Este método retorna una tupla con dos elementos. El primer elemento
            es el identificador de código que se debe utilizar para referirse al 
            tipo de la nueva estructura definida. El segundo elemento es una lista
            con los identificadores de código que se pueden utilizar para acceder
            a cada uno de los campos de la estructura. 
        """
        code_name = self._disambiguate(name, self._keywords)
        code_name = self._disambiguate(code_name, self._type_defs)
        definition = 'struct {0}\n'.format(name)
        definition += '{\n'
        field_code_names = []
        for field_name, field_code_type in zip(field_names, field_code_types):
            field_name_code = self._disambiguate(field_name, self._keywords)
            field_code_names.append(field_name_code)
            definition += '{0} {1};\n'.format(field_code_type, field_name_code)
        definition += '};'
        self._type_defs[name] = definition
        return (code_name, field_code_names)
    
    def define_scope(self, member_names, member_types, parent_code_name=None):
        """
        Utilizado para generar las estructuras de código C que representan los 
        ámbitos de ejecución de un programa Tiger. Este método llama a 
        C{define_struct} con nombres para las estructuras garantizando que son 
        únicos utilizando un contador unido al nombre en lugar de los guiones 
        bajos añadidos por el método C{_disambiguate}.
        
        @type member_names: C{list}
        @param member_names: Lista con los nombres de las variables y 
            funciones que se definen en el ámbito de ejecución.
            
        @type member_types: C{list}
        @param member_types: Lista con las instancias de herederos de 
            C{TigerType} correspondiente a cada uno de los nombres en 
            la lista C{member_names}. Este método da valor a las propiedades
            C{code_name} o C{code_type} de estas instancias, según
            corresponda.
        
        @type parent_code_name: C{str}
        @param parent_code_name: Identificador en el código generado
            correspondiente a la estructura representando el ámbito de ejecución 
            padre del ámbito que se quiere definir. Si el ámbito es raíz, 
            especificar C{None}.
            
        @rtype: C{tuple}
        @return: Este método retorna una tupla con dos elementos. El primer 
            es el nombre de una variable local del tipo de la nueva estructura 
            definida. El segundo elemento es el identificador de código que se 
            debe utilizar para referirse al tipo de la nueva estructura definida.
        """
        self._scopes_count += 1
        code_name = 'scope{0}'.format(self._scopes_count)
        code_type = 'struct {0}* {0};'.format(code_name)
        func = self._func_stack[0]
        self._func_locals[func].append(code_type)
        stmt = '{0} = pytiger2c_malloc(sizeof(struct {0}));'.format(code_name)
        self._func_stmts[func].append(stmt)
        self._func_cleanups[func].append('free({0});'.format(code_name))
        field_names, field_types = [], []
        variable_types = []
        for member_name, member_type in zip(member_names, member_types):
            if isinstance(member_type, FunctionType):
                self.define_function(member_name, member_type)
            else:
                field_names.append(member_name)
                field_types.append(member_type.type.code_type)
                variable_types.append(member_type)
        if parent_code_name:
            field_names.insert(0, 'parent')
            field_types.insert(0, 'struct {0}*'.format(parent_code_name))
        code_name, field_code_names = \
            self.define_struct(code_name, field_names, field_types)
        for variable_type, variable_code_name in zip(variable_types, field_code_names):
            variable_type.code_name = variable_code_name
        return (code_name, code_type)
        
    def define_array(self):
        """
        """
        
    def define_function(self, func_name, func_type):
        """
        """
        # anadir el prefijo a function_name y desambiguar el nombre de la 
        # funcion con las funciones en func_headers.
        # crear el string de la cabecera y anadirla a func_headers.
        # asignare al function type cual fue el code name que le toco

    def begin_function(self, func_code_name):
        """
        Cambia la función actual utilizada por el generador. Anteriormente
        se debe haber definido la cabecera de esta función utilizando el
        método C{define_function}.
        
        @type func_code_name: C{str}
        @param func_code_name: Identificador de código de la función.
        
        @raise CodeGenerationError: Esta excepción se lanzará si se intenta 
            cambiar la función actual del generador por una cuya cabecera no 
            ha sido definida anteriormente.
        """
        if func_code_name in self._func_header:
            self._func_locals[func_code_name] = []
            self._func_stmts[func_code_name] = []
            self._func_cleanups[func_code_name] = []
            self._func_stack.insert(0, func_code_name)
        else:
            message = 'Trying to change to an undefined function'
            raise CodeGenerationError(message)            
        
    def end_function(self, return_var=None):
        """
        Termina la definición de la función actual. Luego de que este método se 
        ejecute no será posible añadir código a la definición de dicha función.
        
        @type return_var: C{str}
        @param return_var: Nombre de la variable local cuyo valor será el valor 
            de retorno de la función. Si la función no tiene valor de retorno
            se debe especificar C{None}. 
        """
        if return_var is not None:
            func = self._func_stack[0]
            self._func_return[func] = 'return {0};'.format(return_var)
        del self._func_stack[0]
        
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
        local_name = '{0}{1}'.format(self._locals_prefix, self._locals_count)
        declaration = '{0} {1};'.format(code_type, local_name) 
        func = self._func_stack[0]
        self._func_locals[func].append(declaration)
        return local_name
        
    def add_statement(self, statement, free=False):
        """
        Añade una instrucción al cuerpo de la función actual. Si la instrucción es 
        una llamada para liberar la memoria utilizada por alguna variable se debe 
        especificar el parámetro C{free} como C{True} para que sea ejecutada luego 
        de todas las funciones en el cuerpo de la función y antes de que termine 
        la función. 
        
        @type statement: C{str}
        @param statement: Instrucción que se debe añadir al cuerpo de la función
            actual del generador de código.
            
        @type free: C{bool}
        @param free: Indica que la instrucción que se añade libera la memoria 
            utilizada por alguna variable y debe ser ejecutada luego de las 
            instrucciones del cuerpo de la función.
        """
        func = self._func_stack[0]
        if free:
            self._func_cleanups[func].append(statement)
        else:
            self._func_stmts[func].append(statement)
        
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
        self.end_function('EXIT_SUCCESS')
        if self._func_stack:
            message = 'Trying to close the generator with opened functions'
            raise CodeGenerationError(message)
        
    def write(self, output_fd):
        """
        Escribe el código C generado hacia un descriptor de fichero.
        
        @type output_fd: C{file}
        @param output_fd: Descriptor de fichero donde se debe escribir el código 
            C resultante de la traducción del programa Tiger.
        """
        includes_c = os.path.join(self._stdlib_dir, 'includes.c')
        with open(includes_c) as fd:
            output_fd.write(fd.read())
            
        types_c = os.path.join(self._stdlib_dir, 'types.c')
        with open(types_c) as fd:
            output_fd.write(fd.read())
            
        # Types defined in the program.
        for definition in self._type_defs.itervalues():
            output_fd.write('\n')
            output_fd.write(definition)
            output_fd.write('\n')
        
        prototypes_c = os.path.join(self._stdlib_dir, 'prototypes.c')
        with open(prototypes_c) as fd:
            output_fd.write(fd.read())
            
        # Prototypes of the functions defined in the program.
        for header in self._func_header.itervalues():
            output_fd.write(header)
            output_fd.write(';\n\n')
        
        functions_c = os.path.join(self._stdlib_dir, 'functions.c')
        with open(functions_c) as fd:
            output_fd.write(fd.read())

        # Functions defined in the program.
        for func in self._func_header.iterkeys():
            output_fd.write(self._func_header[func])
            output_fd.write('\n{\n')
            
            for definition in self._func_locals[func]:
                output_fd.write(definition)
                output_fd.write('\n')
            
            output_fd.write('\n')
            for statement in self._func_stmts[func]:
                output_fd.write(statement)
                output_fd.write('\n')
            
            output_fd.write('\n')
            for cleanup in self._func_cleanups[func]:
                output_fd.write(cleanup)
                output_fd.write('\n')
            
            if func in self._func_return:
                output_fd.write('\n')
                output_fd.write(self._func_return[func])
                output_fd.write('\n')
            output_fd.write('}\n\n')
