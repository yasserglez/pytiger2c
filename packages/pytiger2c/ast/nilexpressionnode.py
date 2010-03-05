# -*- coding: utf-8 -*-

"""
Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class NilExpressionNode(ValuedExpressionNode):
    """
    Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NilExpressionNode}.
        """
        super(NilExpressionNode, self).__init__()

