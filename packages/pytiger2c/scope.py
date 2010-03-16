# -*- coding: utf-8 -*-

"""
Clase C{Scope} que representa un ámbito de ejecución de Tiger.
"""

from pytiger2c.types.functiontype import FunctionType


class Scope(object):
    """
    Clase C{Scope} que representa un ámbito de ejecución de Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución detereminado en Tiger.
    """
    
    def _get_parent(self):
        """
        Método para obtener el valor de la propiedad C{parent}.
        """
        return self._parent
    
    parent = property(_get_parent)
    
    def __init__(self, parent):
        """
        Inicializa la clase C{Scope}
        
        @type parent: C{Scope}
        @param parent: Ámbito en el que se define este nuevo ámbito. 
        """
        self._parent = parent
        self._types = {}
        self._variables = {}
        self._functions = {}

    def generate_code(self):
        """
        Genera el código correspondiente a la definición de las variables, tipos, 
        así como las cabeceras de funciones que están definidos en este.
        """
    
    def get_variable_code(self, name):
        """
        Genera el código correspondiente a acceder a una variable en este ámbito o en
        alguno superior.
        
        Una definida en un ámbito superior puede ser accedida desde algún ámbito inferior
        por lo que la variable en cuestión puede estar definida en el ámbito actual, en su
        padre o en algún ancestro suyo.
        
        @type name: C{str}
        @param name: C{str} correspondiente al nombre de la variable.
        
        @rtype: C{str}
        @return: C{str} correspondiente al código C{C} necesario para acceder a la 
            variable.
        """
        
    def define_type(self, name, type):
        """
        Añade una definición de tipos al ámbito actual. 
        
        @type name: C{str}
        @param name: C{str} correspondiente al nombre del tipo que se declara.
        
        @type type: C{TigerType}
        @param type: C{TigerType} correspondiente a la declaración de tipo.
        """
        
        self._types[name] = type
        
    def get_type_definition(self, name):
        """
        Retorna la definición de tipos correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: C{str} nombre del tipo que se quiere obtener.
        
        @rtype: C{TigerType}
        @return: C{TigerType} correspondiente a la definición de tipo 
            buscada.
            
        @raise C{KeyError}: Se lanza un C{KeyError} si el tipo no está
            definido en este scope o en alguno superior.
        """
        if name in self._types:
            return self._types[name]
        else:
            return self._parent.get_type_definition(name)
    
    def define_function(self, name, data):
        """
        Añade una definición de funciones al ámbito actual.
        
        @type name: C{str}
        @param name: C{str} correspondiente al nombre de la función
            que se declara.
            
        @type data: C{FunctionType}
        @param data: C{FunctionType} correspondiente a la definición de 
            función.
        """
        self._functions[name] = data
    
    def get_function_data(self, name):
        """
        Retorna la definición de función correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: C{str} nombre de la función buscada.
        
        @rtype: C{FunctionType}
        @return: C{FunctionType} correspondiente a la definición 
            de la función buscada.
        
        @raise C{KeyError}: Se lanza un C{KeyError} si la función no está
            definida en este scope o en alguno superior.
        """
        if name in self._functions:
            return self._functions[name]
        else:
            return self.parent.get_function_data(name)
    
    def define_variable(self, name, type):
        """
        Añade una definición de variable al ámbito actual.
        
        @type name: C{str}
        @param name: C{str} correspondiente al nombre de la variable
            que se declara.
            
        @type data: C{type}
        @param data: C{type} correspondiente al nombre del tipo que tiene
            la variable.
        """
        self._variables[name] = type
        
    def get_variable_type(self, name):
        """
        Retorna el nombre del tipo de la variable buscada
        
        @type name: C{str}
        @param name: C{str} nombre de la variable buscada.
        
        @rtype: C{str}
        @return: C{str} correspondiente al tipo de la variable buscada.
        
        @raise C{KeyError}: Se lanza un C{KeyError} si la variable no está
            definida en este scope o en alguno superior. 
        """
        if name in self._variables:
            return self._variables[name]
        else:
            return self.parent.get_variable_type(name)
        
class RootScope(Scope):
    """
    Clase C{RootScope} que representa el ámbito raíz de un programa Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución detereminado en Tiger.
    
    En esta clase se encuentran las definiciones de las funciones de 
    la librería estándar y tipos básicos de Tiger.
    """

    def get_type_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_type_definition}
        en la clase C{Scope}.
        """
        return self._types[name]

    def get_function_data(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_function_data}
        en la clase C{Scope}.
        """
        return self._functions[name]

    def get_variable_type(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_variable_type}
        en la clase C{Scope}.
        """
        return self._variables[name]
    
    def _init_types(self):
        """
        """
    
    def _init_functions(self):
        """
        """
    
    def _init_variables(self):
        """
        """
    
    def __init__(self):
        """
        Inicializa el ámbito inicial de un programa de Tiger.
        
        Inicializa las declaraciones de las funciones de la librería estándar
        y los tipos básicos.
        """
        super(RootScope, self).__init__(None)
        self._init_types()
        self._init_functions()
        self._init_variables()
        
    
        
        