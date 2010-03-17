# -*- coding: utf-8 -*-

"""
Clases C{Scope} y C{RootScope} que representan ámbitos de ejecución en Tiger.
"""

from pytiger2c.types.tigertype import TigerType
from pytiger2c.types.functiontype import FunctionType


class Scope(object):
    """
    Clase C{Scope} que representa un ámbito de ejecución de Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución en Tiger. Además mantiene una referencia
    a un ámbito padre donde se encuentra contenido este ámbito.
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
        self._members = {}

    def generate_code(self):
        """
        Genera el código correspondiente a la definición de las variables, tipos, 
        así como las cabeceras de funciones que están definidos en este.
        """
        raise NotImplementedError()
    
    def get_variable_code(self, name):
        """
        Genera el código necesario para acceder a una variable definida en este 
        ámbito o en alguno superior.
        
        Una definida en un ámbito superior puede ser accedida desde algún ámbito 
        inferior por lo que la variable en cuestión puede estar definida en el 
        ámbito actual, en su padre o en algún ancestro suyo.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la variable.
        
        @rtype: C{str}
        @return: Cadena de caracteres correspondiente al código C necesario para 
            acceder a la variable.
        """
        
    def define_type(self, name, tiger_type):
        """
        Añade una definición de tipos al ámbito actual.
        
        Un tipo puede definirse con el mismo nombre que alguno contenido en 
        algún ámbito superior y este nuevo tipo oculta al existente en el 
        ámbito superior. En caso de que el nuevo tipo tenga el mismo nombre 
        que alguno definido en el mismo ámbito, ocurre un error.        
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre del 
            tipo que se declara.
        
        @type type: C{TigerType}
        @param type: Instancia de C{TigerType} correspondiente a la declaración 
            de tipo.
        
        @raise C{ValueError}: Se lanza una excepción C{ValueError} si el tipo 
            que se intenta declarar fue definido anteriormente en este ámbito. 
        """
        if not (name in self._types):
            self._types[name] = tiger_type
        else:
            raise ValueError('Type already defined in this scope')
        
    def get_type_definition(self, name):
        """
        Retorna la definición de tipos correspondiente al nombre dado. Si
        el tipo no se encuentra en el ámbito actual se buscará en los
        ancestros hasta llegar al ámbito raíz que lanzará una excepción
        si una definición de tipo para el nombre dado no es encontrado 
        finalmente.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre del 
            tipo que se quiere obtener.
        
        @rtype: C{TigerType}
        @return: Instancia de C{TigerType} correspondiente a la definición 
            de tipo buscada.
            
        @raise C{KeyError}: Se lanza una excepción C{KeyError} si el tipo no 
            está definido en este ámbito o en alguno superior.
        """
        if name in self._types:
            return self._types[name]
        else:
            return self._parent.get_type_definition(name)
    
    def define_function(self, name, function_type):
        """
        Añade una definición de funciones al ámbito actual.
        
        Una función puede definirse con el mismo nombre que alguna contenido en 
        algún ámbito superior y esta nueva función oculta a la existente en el 
        ámbito superior. En caso de que la nueva función tenga el mismo nombre
        que alguna definida en el mismo ámbito, ocurre un error. 
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            función que se declara.
            
        @type function_type: C{FunctionType}
        @param function_type: Instancia de C{FunctionType} correspondiente a la 
            definición de función.
            
        @raise C{ValueError}: Se lanza una excepción C{ValueError} si la función 
            que se intenta definir se definió anteriormente en este ámbito. 
        """
        if not (name in self._members):
            self._members[name] = function_type
        else:
            raise ValueError('Function already defined in this scope')
    
    def get_function_definition(self, name):
        """
        Retorna la definición de función correspondiente al nombre dado.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            función buscada.
        
        @rtype: C{FunctionType}
        @return: Instancia de C{FunctionType} correspondiente a la definición 
            de la función buscada.
        
        @raise C{KeyError}: Se lanza un C{KeyError} si la función no está
            definida en este scope o en alguno superior.

        @raise C{ValueError}: Se lanza una excepción C{ValueError} si el nombre
            no corresponde al de una función.
        """
        if name in self._members:
            function_type = self._members[name]
            if isinstance(function_type, FunctionType):
                return function_type
            else:
                raise ValueError('The member of the scope is not a function')
        else:
            return self.parent.get_function_definition(name)
    
    def define_variable(self, name, tiger_type):
        """
        Añade una definición de variable al ámbito actual.
        
        Una variable puede definirse con el mismo nombre que alguna contenida 
        en algún ámbito superior y esta nueva variable oculta a la existente en
        el ámbito superior. En caso de que la nueva variable tenga el mismo 
        nombre que alguna definida en el mismo ámbito, ocurre un error.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            variable que se declara.
            
        @type tiger_type: C{TigerType}
        @param tiger_type: Instancia de C{TigerType} correspondiente al 
             tipo de la variable que se quiere definir.
        """
        if not (name in self._members):
            self._members[name] = type
        else:
            raise ValueError('Variable already defined in this scope')
        
    def get_variable_definition(self, name):
        """
        Retorna el nombre del tipo de la variable buscada
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre de la 
            variable buscada.
        
        @rtype: C{TigerType}
        @return: Instancia de C{TigerType} correspondiente al tipo de la 
            variable buscada.
        
        @raise C{KeyError}: Se lanza una excepción C{KeyError} si la variable 
            no está definida en este ámbito o en alguno superior. 
        """
        if name in self._members:
            variable_type = self._members[name]
            if isinstance(variable_type, TigerType) and not isinstance(variable_type, FunctionType):
                return variable_type
            else:
                raise ValueError('The member of the scope is not a variable')
        else:
            return self.parent.get_variable_definition(name)
        

class RootScope(Scope):
    """
    Clase C{RootScope} que representa el ámbito raíz de un programa Tiger.
    
    Esta clase gestiona los tipos, variables y funciones disponibles
    en un ámbito de ejecución detereminado en Tiger.
    
    En esta clase se encuentran las definiciones de las funciones de 
    la librería estándar y tipos básicos de Tiger. Además, esta clase
    es la encargada de detener la búsqueda de tipos, funciones y 
    variables por los ámbitos padres lanzando una excepción C{KeyError}
    si no se encuentra una definición en este ámbito.
    """
    
    def __init__(self):
        """
        Inicializa el ámbito raíz de un programa de Tiger.
        
        Inicializa las declaraciones de las funciones de la librería estándar
        y los tipos básicos.
        """
        super(RootScope, self).__init__(None)
        self._init_types()
        self._init_functions()
        self._init_variables()
        
    def _init_types(self):
        """
        Inicializa los tipos básicos del lenguaje Tiger definidos implícitamente 
        en el ámbito raíz.
        """
    
    def _init_functions(self):
        """
        Inicializa las funciónes de la libraría standard del lenguaje Tiger
        definidas implícitamente el ámbito raíz.
        """
        
    def _init_variables(self):
        """
        Inicializa las variables definidas implícitamente por el lenguaje Tiger.
        """                

    def get_type_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_type_definition}
        en la clase C{Scope}.
        """
        return self._types[name]

    def get_function_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_function_definition}
        en la clase C{Scope}.
        """
        return self._members[name]

    def get_variable_definition(self, name):
        """
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{get_variable_definition}
        en la clase C{Scope}.
        """
        return self._members[name]
