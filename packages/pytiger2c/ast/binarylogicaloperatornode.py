# -*- coding: utf-8 -*-

"""
Clase C{BinaryLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode
from pytiger2c.types.integertype import IntegerType


class BinaryLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{BinaryLogicalOperatorNode} del árbol de sintáxis abstracta.
    
    Esta clase implementa el método C{check_semantics} para los operadores
    binarios con argumentos enteros del lenguaje Tiger. Estos operadores 
    son los siguientes: el C{OR} binario C{|} y el C{AND} binario C{&}.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{BinaryLogicalOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.
        """
        super(BinaryLogicalOperatorNode, self).__init__(left, right)        

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        Los operadores cuyas clases del árbol de sintáxis abstracta derivan de esta
        deben recibir operandos enteros y siempre tendrán tipo de retorno entero
        (1 para el resultado verdadero, 0 para el falso).
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la expresión de la izquierda como la 
        expresión de la derecha. Luego se comprueba que ambas retornen valor y 
        que el tipo de retorno de ambas sea entero.
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.right.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.right.has_return_value():
                message = 'Invalid use of binary logical operator with a ' \
                          'non-valued right expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.right.return_type != IntegerType():
                message = 'Invalid use of binary logical operator with a ' \
                          'non-integer right value at line {line}'
                errors.append(message.format(line=self.line_number))
                
        errors_before = len(errors)
        
        self.left.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.left.has_return_value():
                message = 'Invalid use of binary logical operator with a ' \
                          'non-valued left expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.left.return_type != IntegerType():
                message = 'Invalid use of binary logical operator with a ' \
                          'non-integer left value at line {line}'
                errors.append(message.format(line=self.line_number))
            
        self._return_type = IntegerType()
