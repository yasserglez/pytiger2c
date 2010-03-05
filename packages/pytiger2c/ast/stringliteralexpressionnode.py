# -*- coding: utf-8 -*-

"""
Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class StringLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{StringLiteralExpressionNode}.
        """
        super(StringLiteralExpressionNode, self).__init__()

