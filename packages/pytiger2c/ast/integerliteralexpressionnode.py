# -*- coding: utf-8 -*-

"""
Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.integertype import IntegerType


class IntegerLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa un literal de un número entero en el lenguaje Tiger. El valor
    de retorno de esta expresión siempre será C{IntegerType}.
    """
    
    def _get_integer(self):
        """
        Método para obtener el valor de la propiedad C{integer}.
        """
        return self._integer
    
    integer = property(_get_integer)
    
    def __init__(self, integer):
        """
        Inicializa la clase C{IntegerLiteralExpressionNode}.
        
        @type integer: C{int}
        @param integer: Valor del número entero literal.
        """
        super(IntegerLiteralExpressionNode, self).__init__()
        self._integer = integer

    def check_semantics(self, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Este nodo del árbol de sintáxis abstracta no requiere comprobación
        semántica, solamente se da valor al tipo de retorno del nodo que 
        siempre será C{IntegerType}.        
        """
        # Set the return type of the expression.
        self._return_type = IntegerType()
