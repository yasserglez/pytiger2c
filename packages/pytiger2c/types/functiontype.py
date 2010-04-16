# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo función.
"""

from pytiger2c.types.tigertype import TigerType


class FunctionType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo función.
    """
    
    def _get_return_type(self):
        """
        Método para obtener el valor de la propiedad C{return_type}.
        """
        return self._return_type
    
    def _set_return_type(self, type):
        """
        Método para cambiar el valor de la propiedad C{return_type}.
        """
        self._return_type = type
    
    return_type = property(_get_return_type, _set_return_type)
    
    def _get_parameters_types(self):
        """
        Método para obtener el valor de la propiedad C{parameters_types}.
        """
        return self._parameters_type
    
    def _set_parameters_types(self, types):
        """
        Método para cambiar el valor de la propiedad C{parameters_types}.
        """
        self._parameters_type = types        
    
    parameters_types = property(_get_parameters_types, _set_parameters_types)
    
    def _get_parameters_typenames(self):
        """
        Método para obtener el valor de la propiedad C{parameters_types}.
        """
        return self._parameters_typename
    
    parameters_typenames = property(_get_parameters_typenames)
    
    def _get_code_name(self):
        """
        Método para obtener el valor de la propiedad C{code_name}.
        """
        return self._code_name
    
    def _set_code_name(self, value):
        """
        Método para cambiar el valor de la propiedad C{code_name}.
        """
        self._code_name = value
    
    code_name = property(_get_code_name, _set_code_name)    
    
    def __init__(self, return_type, parameters_types, parameters_typename):
        """
        Inicializa la clase representando el tipo función.
        
        @type return_type: C{TigerType}
        @param return_type: Instance de C{TigerType} correspondiente al tipo del 
            valor de retorno de la función. Si la función no tiene valor de 
            retorno el valor de este argumento debe ser especificado como C{None}.
        
        @type parameters_types: C{list}
        @param parameters_types: Lista de las instancias de C{TigerType} 
            correspondientes a los tipos de los parámetros recibidos por la 
            función. Las posiciones de los elementos de la lista deben 
            corresponder con las posiciones de los parámetros de la función.
            Si la función no recibe parámetros el valor de este argumento 
            debe ser especificado como una lista vacía.
        
        @type parameters_typenames: C{list}
        @param parameters_typenames: Lista de los nombres de los tipos de los 
            parámetros de la función. Las posiciones de los elementos de la 
            lista deben corresponder con las posiciones de los parámetros de
            la función. Si la función no recibe parámetros el valor de este 
            argumento debe ser especificado como una lista vacía.
        """
        super(FunctionType, self).__init__()
        self._return_type = return_type
        self._parameters_type = parameters_types
        self._parameters_typename = parameters_typename
        self._code_name = None

