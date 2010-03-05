# -*- coding: utf-8 -*-

"""
Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class IntegerLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{IntegerLiteralExpressionNode}.
        """
        super(IntegerLiteralExpressionNode, self).__init__()

