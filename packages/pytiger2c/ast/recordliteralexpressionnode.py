# -*- coding: utf-8 -*-

"""
Clase C{RecordLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class RecordLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{RecordLiteralExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{RecordLiteralExpressionNode}.
        """
        super(RecordLiteralExpressionNode, self).__init__()

