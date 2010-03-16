# -*- coding: utf-8 -*-

"""
Clase C{OperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class OperatorNode(ValuedExpressionNode):
    """
    Clase C{OperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{OperatorNode}.
        """
        super(OperatorNode, self).__init__()
