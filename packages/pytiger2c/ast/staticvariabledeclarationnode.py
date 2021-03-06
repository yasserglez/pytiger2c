# -*- coding: utf-8 -*-

"""
Clase C{StaticVariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.variabledeclarationnode import VariableDeclarationNode
from pytiger2c.types.niltype import NilType
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.variabletype import VariableType


class StaticVariableDeclarationNode(VariableDeclarationNode):
    """
    Clase C{StaticVariableDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de declaración de variables especificando explícitamente
    el tipo de esta del lenguaje Tiger. Esta estructura recibe una expresión cuyo 
    valor se le asignará a la variable, además del tipo que tendrá la misma.
    """
    
    def _get_type_name(self):
        """
        Método para obtener el valor de la propiedad C{type_name}
        """
        return self._type_name
    
    type_name = property(_get_type_name)    
    
    def __init__(self, name, value, type_name):
        """
        Inicializa la clase C{StaticVariableDeclarationNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.
        
        @type type_name: C{str}
        @param type_name: Nombre del tipo que se expresa explícitamente para
            esta variable
        """
        super(StaticVariableDeclarationNode, self).__init__(name, value)
        self._type_name = type_name

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de declaración de variables especificando explícitamente
        el tipo de esta recibe una expresión cuyo valor se le asignará a la 
        variable , además del tipo que tendrá la misma.
        
        En la comprobación semántica se comprueba semánticamente la expresión que
        se quiere asignar a la variable. Luego se comprueba que el tipo de la 
        variable esté definido en el ámbito de esta, que la expresión que se le
        asigna retorne valor, que este valor sea del mismo tipo que el especificado 
        o C{nil} y que en su ámbito local el nombre que se quiere asignar a esta
        variable no haya sido asignado a una función u otra variable. Se reportarán
        errores si se encuentran errores durante la comprobación semántica de la 
        expresión, si esta no retorna valor o este no es del mismo tipo que el de
        la variable o C{nil} y por último si el nombre de la variable ya ha sido 
        asignado a una función u otra variable en su ámbito local.
        
        En el proceso de comprobación semántica la propiedad C{type} toma valor y la
        variable es definida en su ámbito local.
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.value.check_semantics(self._scope, errors)
        
        if errors_before != len(errors):
            return
        
        try:
            tiger_type = self._scope.get_type_definition(self._type_name)
            self._type = VariableType(tiger_type)
        except KeyError:
            message = 'Undefined type of variable at line {line}'
            errors.append(message.format(line=self.line_number))
            
        if errors_before != len(errors):
            return
                
        if not self.value.has_return_value():
            message = 'Non valued expression assigned to a variable at line {line}'
            errors.append(message.format(line=self.line_number))
        elif self.value.return_type == NilType():
            if not isinstance(self.type, RecordType):
                message = 'Invalid assignment of nil to a non record at line {line}'
                errors.append(message.format(line=self.line_number))
        elif self.value.return_type != self.type:
            message = 'Invalid assignment type variable at line {line}'
            errors.append(message.format(line=self.line_number))
        
        if errors_before != len(errors):
            return
        
        try:
            self._scope.define_variable(self.name, self._type)
        except ValueError:
            message = 'Invalid variable name at line {line}'
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
        name = generator.add_node(self.name)
        type_name = generator.add_node(self.type_name)
        value = self.value.generate_dot(generator)
        generator.add_edge(me, name)
        generator.add_edge(me, type_name)
        generator.add_edge(me, value)
        return me
