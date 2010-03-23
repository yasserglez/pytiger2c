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
    
    Representa la creación de una instancia de un tipo C{record} definido con 
    anterioridad. La creación de una instancia de un tipo C{record} recibe el 
    nombre del tipo de C{record} que se quiere crear, una lista con los nombres
    de los campos del C{record} y otra lista con las expresiones correspondientes
    a los valores que se le quieren dar a cada campo del C{record}.
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
        @param type_name: Nombre del tipo C{record} que se quiere crear.
        
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
        
        La creación de una instancia de un tipo C{record} recibe el nombre del 
        tipo de C{record} que se quiere crear, una lista con los nombres de los
        campos del C{record} y otra lista con las expresiones correspondientes
        a los valores que se le quieren dar a cada campo del C{record}.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueba que el tipo C{record} que se quiere crear ha sido definido
        en el ámbito correspondiente, luego se comprueban que los campos.Cada 
        campo debe tener exactamente el mismo nombre que el campo correspondiente 
        en la declaración del tipo, en cuanto al tipo deben corresponder de igual 
        manera, con la excepción de un tipo C{record} en cuyo caso, es permitido 
        también el tipo C{nil}.          
        """
        self._scope = scope
        try:
            self._return_type = self.scope.get_type_definition(self.type_name)
        except KeyError:
            message = 'Undefined type {type_name} at line {line}'
            errors.append(message.format(type_name = self._type_name, 
                                         line=self.line_number))
        if isinstance(self.return_type, RecordType):
            fields_names_given = len(self._fields_names)
            fields_names_original = len(self.return_type.fields_names)
            if fields_names_given == fields_names_original:
                self._check_parameters(errors)
            else:
                message = 'Invalid fields count, {needed} needed but {given} '\
                          'given at line {line}'
                errors.append(message.format(given = fields_names_given,
                                             needed = fields_names_original,
                                             line=self.line_number))
        else:
            message = 'Invalid non record type {type_name} at line {line}'
            errors.append(message.format(type_name = self._type_name, 
                                         line=self.line_number))
    
    def _check_parameters(self, errors):
        """
        Comprueba semánticamente los campos dados. Cada campo debe tener exactamente 
        el mismo nombre que el campo correspondiente en la declaración del tipo, en
        cuanto al tipo deben corresponder de igual manera, con la excepción de un 
        tipo C{record} en cuyo caso, es permitido también el tipo C{nil}
        
        @type errors: C{list}
        @param errors: Lista a la cual se deben añadir los mensajes de error de
            los errores semánticos encontrados durante esta comprobación.
        """
        for index in xrange(len(self.fields_names)):
            if self.fields_names[index] != self.return_type.fields_names[index]:
                message = 'Invalid name {name} of the field #{index} of '\
                          'the record literal at line {line}'
                errors.append(message.format(name=self.fields_names[index],
                                             index=index + 1,
                                             line=self.line_number))
            self.fields_values[index].check_semantics(self.scope, errors)
            if not self.fields_values[index].has_return_value():
                message = 'Invalid non valued expression for the field #{index} '\
                          'of the record literal at line {line}'
                errors.append(message.format(index=index + 1,
                                             line=self.line_number))
            elif self.fields_values[index].return_type == NilType():
                if not isinstance(self.return_type.fields_types[index], RecordType):
                    message = 'Invalid nil assignment to the field #{index} '\
                              'of the record literal at line {line}'
                    errors.append(message.format(index=index + 1,
                                                 line=self.line_number))
            elif (self.fields_values[index].return_type 
                  != self.return_type.fields_types[index]):
                message = 'Invalid type for field #{index} of '\
                          'the record literal at line {line}'
                errors.append(message.format(index=index + 1,
                                             line=self.line_number))
