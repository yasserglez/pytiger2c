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
        
        if not name in self._types:
            self._types[name] = type
        else:
            pass
        
    def get_type_definition(self, name):
        """
        Retorna la definición de tipos correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: C{str} nombre del tipo que se quiere obtener.
        
        @rtype: C{TigerType}
        @return: C{TigerType} correspondiente a la definición de tipo 
            buscada.
        """
        if name in self._types:
            return self._types[name]
        else:
            pass
    
    
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
        if  not name in self._functions:
            self._functions[name] = data
        else:
            pass
    
    def get_function_data(self, name):
        """
        Retorna la definición de función correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: C{str} nombre de la función buscada.
        
        @rtype: C{FunctionType}
        @return: C{FunctionType} correspondiente a la definición 
            de la función buscada.
        """
        if name in self._functions:
            return self._functions[name]
        else:
            pass
    
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
        if  not name in self._variables:
            self._variables[name] = type
        else:
            pass
        
    def get_variable_type(self, name):
        """
        Retorna el nombre del tipo de la variable buscada
        
        @type name: C{str}
        @param name: C{str} nombre de la variable buscada.
        
        @rtype: C{str}
        @return: C{str} correspondiente al tipo de la variable buscada. 
        """
        if name in self._variables:
            return self._variables[name]
        else:
            pass