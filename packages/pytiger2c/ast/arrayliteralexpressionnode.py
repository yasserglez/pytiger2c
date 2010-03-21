# -*- coding: utf-8 -*-

"""
Clase C{ArrayLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class ArrayLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{ArrayLiteralExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ArrayLiteralExpressionNode}.
        """
        super(ArrayLiteralExpressionNode, self).__init__()

