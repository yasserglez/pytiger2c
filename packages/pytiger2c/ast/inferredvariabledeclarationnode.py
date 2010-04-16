# -*- coding: utf-8 -*-

"""
Clase C{InferredVariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.variabledeclarationnode import VariableDeclarationNode
from pytiger2c.types.niltype import NilType
from pytiger2c.types.variabletype import VariableType


class InferredVariableDeclarationNode(VariableDeclarationNode):
    """
    Clase C{InferredVariableDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de declaración de variables sin expresar
    explícitamente el tipo de esta del lenguaje Tiger. Esta estructura 
    recibe una expresión cuyo valor se le asignará a la variable y el 
    tipo de la variable se infiere del tipo de esta expresión.
    """

    def __init__(self, name, value):
        """
        Inicializa la clase C{InferredVariableDeclarationNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.
        """
        super(InferredVariableDeclarationNode, self).__init__(name, value)

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de declaración de variables sin especificar explícitamente
        el tipo de esta recibe una expresión cuyo valor se le asignará a la 
        variable y el tipo de la variable se infiere del tipo de esta expresión.
        
        En la comprobación semántica se comprueba semánticamente la expresión que
        se quiere asignar a la variable. Luego se comprueba que esta expresión
        retorne valor, que este valor no sea C{nil} y que en su ámbito local
        el nombre que se quiere asignar a la variable no haya sido asignado a
        una función u otra variable. Se reportarán errores si se encuentran errores
        durante la comprobación semántica de la expresión, si esta no retorna valor
        o este es nil y por último si el nombre de la variable ya ha sido asignado a
        una función u otra variable en su ámbito local.
        
        En el proceso de comprobación semántica la propiedad C{type} toma valor y la
        variable es definida en su ámbito local.
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.value.check_semantics(self.scope, errors)
        
        if errors_before == len(errors):
            if not self.value.has_return_value():
                message = 'Non-valued expression assigned to a variable at line {line}'
                errors.append(message.format(line=self.line_number))
            elif self.value.return_type == NilType():
                message = 'Invalid nil assignment to a variable at line {line}'
                errors.append(message.format(line=self.line_number))
            else:
                self._type = VariableType(self.value.return_type)
            
            try:
                self.scope.define_variable(self.name, self._type)
            except ValueError:
                message = 'Could not hide a variable defined in the same scope at line {line}'
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
        value = self.value.generate_dot(generator)
        generator.add_edge(me, name)
        generator.add_edge(me, value)
        return me
