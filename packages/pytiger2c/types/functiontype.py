# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo función.
"""

from pytiger2c.types.tigertype import TigerType
from gaphor.UML.uml2 import Parameter


class FunctionType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo función.
    
    Esta clase es una manera de representar las funciones en tiger.
    """
    
    def _get_return_type(self):
        """
        Método para obtener el valor de la propiedad C{return_type}.
        """
        return self._return_type
    
    return_type = property(_get_return_type)
    
    def _get_parameters_type(self):
        """
        Método para obtener el valor de la propiedad C{parameters_type}.
        """
        return self._parameters_type
    
    parameters_type = property(_get_parameters_type)
    
    
    def __init__(self, return_type, parameters_type):
        """
        Inicializa la clase representando el tipo función.
        
        @type return_type: C{str}
        @param return_type: Nombre del tipo de retorno de la función.
        
        @type parameters_type: C{list}
        @param parameters_type: Lista de los nombres de los tipos de los 
            parámetros de la función, por pocisión. 
        """
        super(FunctionType, self).__init__()
        self._return_type = return_type
        self._parameters_type = parameters_type        