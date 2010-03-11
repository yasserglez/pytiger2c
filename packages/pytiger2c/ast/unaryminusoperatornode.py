# -*- coding: utf-8 -*-

"""
Clase C{UnaryMinusOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.unaryoperatornode import UnaryOperatorNode
from pytiger2c.types.integertype import IntegerType


class UnaryMinusOperatorNode(UnaryOperatorNode):
    """
    Clase C{UnaryMinusOperatorNode} del árbol de sintáxis abstracta.
    
    Este nodo representa el operador menos unario C{-} del lenguaje Tiger. 
    Este operador se utiliza para cambiar el signo de expresiones que 
    devuelvan valores enteros. 
    """
    
    def __init__(self, expression):
        """
        Inicializa la clase C{UnaryMinusOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{__init__} en la clase C{UnaryOperatorNode}.        
        """
        super(UnaryMinusOperatorNode, self).__init__(expression)

    def check_semantics(self, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        El operador menos unario se aplica solamente a expresiones que devuelvan
        enteros y el tipo de retorno siempre será entero.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta 
        se comprueba que la expresión a la que se le va aplicar el operador menos 
        unario esté correcta semánticamente y que tenga valor de retorno entero. 
        El tipo del valor de retorno de la expresión representada por este nodo
        siempre será C{IntegerType}.
        """
        self.expression.check_semantics(errors)
        if self.expression.has_return_value():
            if self.expression.return_type != IntegerType():
                message = 'The expression of the unary minus operator at line {line} ' \
                          'does not return an integer value'
                errors.append(message.format(line=self.line_number))
        else:
            message = 'The expression of the unary minus operator at line {line} ' \
                      'does not return a value'
            errors.append(message.format(line=self.line_number))            
        self._return_type = IntegerType()
