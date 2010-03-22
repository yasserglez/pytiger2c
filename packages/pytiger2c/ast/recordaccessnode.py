# -*- coding: utf-8 -*-

"""
Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode
from pytiger2c.types.recordtype import RecordType


class RecordAccessNode(AccessNode):
    """
    Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de acceso a un campo de un C{record} del lenguaje
    Tiger. La estructura de acceso a un campo de un C{record} del lenguaje 
    Tiger permite obtener el valor de un campo de un tipo C{record} determinado 
    o asignarle un nuevo valor a este C{record} en este campo. Esta estructura 
    recibe la expresión que representa el acceso al C{record} y el nombre 
    correspondiente al campo que se quiere acceder. 
    """
    
    def _get_field_name(self):
        """
        Método para obtener el valor de la propiedad C{field_name}.
        """
        return self._field_name
    
    field_name = property(_get_field_name)
    
    def _get_record(self):
        """
        Método para obtener el valor de la propiedad C{record}.
        """
        return self._record
    
    record = property(_get_record)
    
    def __init__(self, record_expression, field_name):
        """
        Inicializa la clase C{RecordAccessNode}.
        
        @type record_expression: C{LanguageNode}
        @param record_expression: Expresión correspondiente al C{record} 
            que se quiere acceder.
            
        @type field_name: C{str}
        @param field_name: Nombre del campo al que se quiere acceder.
        """
        super(RecordAccessNode, self).__init__()
        self._record = record_expression
        self._field_name = field_name
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de acceso a un campo de un C{record} del lenguaje Tiger
        permite obtener el valor de un campo de un tipo C{record} determinado 
        o asignarle un nuevo valor a este C{record} en este campo. Esta 
        estructura recibe la expresión que representa el acceso al C{record} 
        y el nombre correspondiente al campo que se quiere acceder.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se verifica que la expresión que se correspondiente al C{record} retorne
        valor y que este sea del tipo C{record}, luego se comprueba que el tipo 
        C{record} tenga un campo con ese nombre. 
        
        En el proceso de comprobación semántica toma valor las propiedades
        C{return_type} y C{read_only} 
        """
        self._scope = scope
        self.record.check_semantics(self.scope, errors)
        
        if self.record.has_return_value():
            record_type = self.record.return_type
            if isinstance(record_type, RecordType):
                if self.field_name in record_type.fields_names:
                    index = record_type.fields_names.index(self.field_name)
                    self._return_type = record_type.fields_types[index]
                else:
                    message = 'Undefined field {field} for record access'\
                              ' at line {line}'
                    errors.append(message.format(field = self.field_name, 
                                                 line=self.line_number))
            else:
                message = 'Invalid record type for record access'\
                          ' at line {line}'
                errors.append(message.format(line=self.line_number))
        else:
            message = 'Invalid non value type for record access'\
                      ' at line {line}'
            errors.append(message.format(line=self.line_number))