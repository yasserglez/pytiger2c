# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo array.
"""

from pytiger2c.types.tigertype import TigerType


class ArrayType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo array.
    """
    
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
    
    def _get_fields_typenames(self):
        """
        Método para obtener el valor de la propiedad C{fields_typenames}.
        """
        return self._fields_typenames
    
    fields_typenames = property(_get_fields_typenames)
    
    def _get_fields_types(self):
        """
        Método para obtener el valor de la propiedad C{fields_types}.
        """
        return self._fields_types
    
    def _set_fields_types(self, fields_types):
        """
        Método para cambiar el valor de la propiedad C{fields_types}.
        """
        self._fields_types = fields_types
    
    fields_types = property(_get_fields_types, _set_fields_types)
    
    def __init__(self, values_typename):
        """
        Inicializa la clase representando el tipo array.
        
        @type values_typename: C{str}
        @param values_typename: Nombre del tipo que tendrán los valores del array.
        """
        super(ArrayType, self).__init__()
        self._fields_typenames =  [values_typename]
        self._fields_types = None
        self._code_name = None
