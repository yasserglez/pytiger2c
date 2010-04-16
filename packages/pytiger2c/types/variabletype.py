# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando la definición de una 
variable.
"""

from pytiger2c.types.tigertype import TigerType


class VariableType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando la definición de una 
    variable. 
    """
    
    def _get_read_only(self):
        """
        Método para obtener el valor de la propiedad C{read_only}.
        """
        return self._read_only
    
    def _set_read_only(self, value):
        """
        Método para cambiar el valor de la propiedad C{read_only}.
        """
        self._read_only = value
        
    read_only = property(_get_read_only, _set_read_only)
    
    def _get_type(self):
        """
        Método para obtener el valor de la propiedad C{type}.
        """
        return self._type
    
    def _set_type(self, value):
        """
        Método para cambiar el valor de la propiedad C{type}.
        """
        self._type = value
        
    type = property(_get_type, _set_type)
    
    def __init__(self, tiger_type, read_only = False):
        """
        Inicializa la clase representando la definición de una variable.
        
        @type tiger_type: C{TigerType}
        @param tiger_type: Instancia de C{TigerType} correspondiente al 
             tipo de la variable que se quiere definir.
             
        @type read_only: C{bool}
        @param read_only: Indica si la variable que se define debe ser tratada
            como una variable de sólo lectura. El valor por defecto de este
            argumento es C{False}.
        """
        self._type = tiger_type
        self._read_only = read_only