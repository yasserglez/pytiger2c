# -*- coding: utf-8 -*-

"""
Clase C{FunctionCallNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class FunctionCallNode(ValuedExpressionNode):
    """
    Clase C{FunctionCallNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{FunctionCallNode}.
        """
        super(FunctionCallNode, self).__init__()
