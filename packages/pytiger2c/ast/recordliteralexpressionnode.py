# -*- coding: utf-8 -*-

"""
Clase C{RecordLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class RecordLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{RecordLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa la creación de una instancia de un tipo record definido con 
    anterioridad. La creación de una instancia de un tipo record recibe el 
    nombre del tipo de record que se quiere crear, una lista con los nombres
    de los campos del record y otra lista con las expresiones correspondientes
    a los valores que se le quieren dar a cada campo del record.
    """
    
    def _get_type_name(self):
        """
        Método para obtener el valor de la propiedad C{type_name}.
        """
        return self._type_name
    
    type_name = property(_get_type_name)
    
    def _get_fields_names(self):
        """
        Método para obtener el valor de la propiedad C{fields_names}.
        """
        return self._fields_names
    
    fields_names = property(_get_fields_names)
    
    def _get_fields_values(self):
        """
        Método para obtener el valor de la propiedad C{fields_values}.
        """
        return self._fields_values
    
    fields_values = property(_get_fields_values)
    
    def __init__(self, type_name, fields_names, fields_values):
        """
        Inicializa la clase C{RecordLiteralExpressionNode}.
        
        @type type_name: C{str}
        @param type_name: Nombre del tipo record que se quiere crear.
        
        @type fields_names: C{list}
        @param fields_names: Lista con los nombres de los campos del record, en
            el mismo orden en que aparecen en el programa.
            
        @type fields_values: C{list}
        @param fields_values: Lista con las expresiones de los campos del 
            record, en el mismo orden que aparecen en el programa.
        """
        super(RecordLiteralExpressionNode, self).__init__()
        self._type_name = type_name
        self._fields_names = fields_names
        self._fields_values = fields_values

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La creación de una instancia de un tipo record recibe el nombre del 
        tipo de record que se quiere crear, una lista con los nombres de los
        campos del record y otra lista con las expresiones correspondientes
        a los valores que se le quieren dar a cada campo del record.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueba que el tipo record que se quiere crear ha sido definido
        en el ámbito correspondiente, luego se comprueban que los campos.Cada 
        campo debe tener exactamente el mismo nombre que el campo correspondiente 
        en la declaración del tipo, en cuanto al tipo deben corresponder de igual 
        manera, con la excepción de un tipo record en cuyo caso, es permitido 
        también el tipo C{nil}.          
        """
        self._scope = scope
        
        errors_before = len(errors)

        try:
            self._return_type = self.scope.get_type_definition(self.type_name)
        except KeyError:
            message = 'Undefined type {name} at line {line}'
            errors.append(message.format(name=self._type_name, line=self.line_number))
            
        if errors_before == len(errors):
            if isinstance(self.return_type, RecordType):
                fields_names_given = len(self._fields_names)
                fields_names_original = len(self.return_type.fields_names)
                if fields_names_given == fields_names_original:
                    self.check_parameters(errors)
                else:
                    message = 'Invalid number of fields in record literal at line {line}'
                    errors.append(message.format(line=self.line_number))
            else:
                message = 'Invalid non record type {type_name} at line {line}'
                errors.append(message.format(type_name = self._type_name, 
                                             line=self.line_number))
    
    def check_parameters(self, errors):
        """
        Comprueba semánticamente los campos dados. Cada campo debe tener exactamente 
        el mismo nombre que el campo correspondiente en la declaración del tipo, en
        cuanto al tipo deben corresponder de igual manera, con la excepción de un 
        tipo record en cuyo caso, es permitido también el tipo C{nil}
        
        @type errors: C{list}
        @param errors: Lista a la cual se deben añadir los mensajes de error de
            los errores semánticos encontrados durante esta comprobación.
        """
        for index in xrange(len(self.fields_names)):
            if self.fields_names[index] != self.return_type.fields_names[index]:
                message = 'Invalid name {name} of the field #{index} of ' \
                          'the record literal at line {line}'
                errors.append(message.format(name=self.fields_names[index], index=index + 1,
                                             line=self.line_number))

            errors_before = len(errors)
            
            self.fields_values[index].check_semantics(self.scope, errors)
            
            if errors_before == len(errors): 
                if not self.fields_values[index].has_return_value():
                    message = 'Invalid non valued expression for the field #{index} ' \
                              'of the record literal at line {line}'
                    errors.append(message.format(index=index + 1, line=self.line_number))
                elif self.fields_values[index].return_type == NilType():
                    if not isinstance(self.return_type.fields_types[index], RecordType):
                        message = 'Invalid nil assignment to the field #{index} ' \
                                  'of the record literal at line {line}'
                        errors.append(message.format(index=index + 1, line=self.line_number))
                elif (self.fields_values[index].return_type != 
                      self.return_type.fields_types[index]):
                    message = 'Invalid type for field #{index} of ' \
                              'the record literal at line {line}'
                    errors.append(message.format(index=index + 1, line=self.line_number))

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        type_name = generator.add_node(self.type_name)
        generator.add_edge(me, type_name)
        for field_name, field_value in zip(self.fields_names, self.fields_values):
            field_name = generator.add_node(field_name)
            generator.add_edge(me, field_name)
            field_value = field_value.generate_dot(generator)
            generator.add_edge(field_name, field_value)
        return me
    
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        
        record_code_type = self.return_type.code_type
        local_var = generator.define_local(record_code_type)
        statement = '{local_var} = NULL;'.format(local_var = local_var)
        generator.add_statement(statement, allocate = True)
        statement = '{local_var} = pytiger2c_malloc(sizeof({type}));'
        statement = statement.format(local_var = local_var, 
                                     type = record_code_type[:-1])
        generator.add_statement(statement)
        # Initialize the record.
        for field_value in self.fields_values:
            field_value.generate_code(generator)
        for field_value, field_code_name in zip(self.fields_values, 
                                                self.return_type.field_code_names):
            statement = '{local_var}->{field} = {value};'
            statement = statement.format(local_var = local_var, 
                                         field = field_code_name,
                                         value = field_value.code_name)
            generator.add_statement(statement)
        generator.add_statement('free({0});'.format(local_var), free = True)
        self._code_name = local_var 
