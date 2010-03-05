# -*- coding: utf-8 -*-

"""
Clase C{ExpressionSequenceNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class ExpressionSequenceNode(ValuedExpressionNode):
    """
    Clase C{ExpressionSequenceNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ExpressionSequenceNode}.
        """
        super(ExpressionSequenceNode, self).__init__()

