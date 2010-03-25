# -*- coding: utf-8 -*-

"""
Clase C{MinusOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode
from pytiger2c.types.integertype import IntegerType


class MinusOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{MinusOperatorNode} del árbol de sintáxis abstracta.
    
    Representa el operador de resta C{-} entre dos números enteros 
    del lenguaje Tiger.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{MinusOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{__init__} en la clase C{BinaryOperatorNode}.
        """
        super(MinusOperatorNode, self).__init__(left, right)
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        El operador resta realiza la diferencia entre los el valor de la expresión
        que se encuentra a la izquierda con el valor de la derecha.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la expresión de la izquierda como la 
        expresión de la derecha. Luego se comprueba que ambas retornen valor y 
        que el valor de retorno de ambas sea entero. 
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.right.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.right.has_return_value():
                message = 'Invalid use of minus operator with a non-valued right expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.right.return_type != IntegerType():
                message = 'Invalid use of minus operator with a non-integer right value at line {line}'
                errors.append(message.format(line=self.line_number))

        errors_before = len(errors)
        
        self.left.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.left.has_return_value():
                message = 'Invalid use of minus operator with a non-valued left expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.left.return_type != IntegerType():
                message = 'Invalid use of minus operator with a non-integer left value at line {line}'
                errors.append(message.format(line=self.line_number))
            
        self._return_type = IntegerType()
