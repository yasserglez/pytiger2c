# -*- coding: utf-8 -*-

"""
Clase C{RecordDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.recordtype import RecordType


class RecordDeclarationNode(TypeDeclarationNode):
    """
    Clase C{RecordDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, name, fields_names, fields_typenames):
        """
        Inicializa la clase C{RecordDeclarationNode}.
        
        @type fields_names: C{list}
        @param fields_names: Lista con los nombres de los campos del record, por posición.
        
        @type fields_typenames: C{list}
        @param fields_typenames: Lista con los nombres de los tipos de los campos, por posición.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}.
        """
        super(RecordDeclarationNode, self).__init__(name)
        self._type = RecordType(fields_names, fields_typenames)
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxis 
        abstracta se comprueba que los tipos de los campos del record
        se encuentren definidos en el ámbito local.
        
        Se reportarán errores semánticos si alguno de los tipos de los campos
        no se encuentran definidos en el ámbito local, o en caso de que estén
        definidos en el ámbito local, pero en otro grupo de declaraciones, en
        cuyo caso se considera una declaración de tipos mutuamente recursivos
        en distintos grupos de declaraciones de tipos.
        
        Durante la comprobación semántica se define totalmente el valor de la
        propiedad C{type}.
        """
        self._scope = scope
        
        fields_types = []
        for index, field_typename in enumerate(self.type.fields_typenames):
            try:
                field_type = self.scope.get_type_definition(field_typename)
            except KeyError:
                message = 'Undefined type {type} of the field #{index} ' \
                          'of the record {name} at line {line}'
                errors.append(message.format(type=field_typename, index=index + 1, 
                                             name=self.name, line=self.line_number))
            else:
                fields_types.append(field_type)
        self.type.fields_types = fields_types
        self.type.defined = True
