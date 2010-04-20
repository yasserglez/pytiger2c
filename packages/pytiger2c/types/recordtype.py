# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo record.
"""

from pytiger2c.types.tigertype import TigerType


class RecordType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo record.
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
    
    def _get_field_code_names(self):
        """
        Método para obtener el valor de la propiedad C{field_code_names}.
        """
        return self._field_code_names
    
    def _set_field_code_names(self, value):
        """
        Método para cambiar el valor de la propiedad C{field_code_names}.
        """
        self._field_code_names = value
        
    field_code_names = property(_get_field_code_names, _set_field_code_names)
    
    def _get_fields_names(self):
        """
        Método para obtener el valor de la propiedad C{fields_names}.
        """
        return self._fields_names
    
    fields_names = property(_get_fields_names)

    def __init__(self, fields_names, fields_typenames):
        """
        Inicializa la clase representando el tipo record.
        
        @type fields_names: C{list}
        @param fields_names: Lista con los nombres de los campos del record, por posición.
        
        @type fields_typenames: C{list}
        @param fields_typenames: Lista con los nombres de los tipos de los campos, por posición.
        """
        super(RecordType, self).__init__()
        self._fields_typenames = fields_typenames
        self._fields_names = fields_names
        self._fields_types = None
        self._code_name = None
        self._field_code_names = None
