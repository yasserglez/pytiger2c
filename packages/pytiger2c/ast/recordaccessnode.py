# -*- coding: utf-8 -*-

"""
Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode
from pytiger2c.types.recordtype import RecordType


class RecordAccessNode(AccessNode):
    """
    Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de acceso a un campo de un record del lenguaje
    Tiger. La estructura de acceso a un campo de un record del lenguaje 
    Tiger permite obtener el valor de un campo de un tipo record determinado 
    o asignarle un nuevo valor a este record en este campo. Esta estructura 
    recibe la expresión que representa el acceso al record y el nombre 
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
        Método para obtener el valor de la propiedad record.
        """
        return self._record
    
    record = property(_get_record)
    
    def __init__(self, record, field_name):
        """
        Inicializa la clase C{RecordAccessNode}.
        
        @type record: C{LanguageNode}
        @param record: Expresión correspondiente al record que se quiere acceder.
            
        @type field_name: C{str}
        @param field_name: Nombre del campo del record al que se quiere acceder.
        """
        super(RecordAccessNode, self).__init__()
        self._record = record
        self._field_name = field_name
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de acceso a un campo de un record del lenguaje Tiger
        permite obtener el valor de un campo de un tipo record determinado 
        o asignarle un nuevo valor a este record en este campo. Esta 
        estructura recibe la expresión que representa el acceso al record 
        y el nombre correspondiente al campo que se quiere acceder.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se verifica que la expresión que se correspondiente al record retorne
        valor y que este sea del tipo record, luego se comprueba que el tipo 
        record tenga un campo con ese nombre. 
        
        En el proceso de comprobación semántica toma valor las propiedades
        C{return_type} y C{read_only} 
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.record.check_semantics(self.scope, errors)
        
        if errors_before == len(errors):
            if self.record.has_return_value():
                record_type = self.record.return_type
                if isinstance(record_type, RecordType):
                    if self.field_name in record_type.fields_names:
                        index = record_type.fields_names.index(self.field_name)
                        self._return_type = record_type.fields_types[index]
                    else:
                        message = 'Undefined field {field} on record access at line {line}'
                        errors.append(message.format(field = self.field_name, 
                                                     line=self.line_number))
                else:
                    message = 'Invalid record type on record access at line {line}'
                    errors.append(message.format(line=self.line_number))
            else:
                message = 'Invalid non value type on record access at line {line}'
                errors.append(message.format(line=self.line_number))

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        record = self.record.generate_dot(generator)
        generator.add_edge(me, record)
        field_name = generator.add_node(self.field_name)
        generator.add_edge(me, field_name)
        return me
    
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.
        
        En particular el nodo de acceso a un C{array}, no genera ninguna
        instrucción de código C{C} sino que toma valor la propiedad C{code_name}.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        self.record.generate_code(generator)
        record_type = self.record.return_type
        index = record_type.fields_names.index(self.field_name)
        field_code_name = record_type.field_code_names[index]
        stmt = 'if({record} == NULL) {{ pytiger2c_error("{msg}"); }}'
        stmt = stmt.format(record=self.record.code_name, msg='Getting a field of a nil record.')       
        generator.add_statement(stmt)
        self._code_name = '{record}->{field}'.format(record=self.record.code_name, field=field_code_name)
