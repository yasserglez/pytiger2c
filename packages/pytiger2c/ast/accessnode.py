# -*- coding: utf-8 -*-

"""
Clase C{AccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class AccessNode(ValuedExpressionNode):
    """
    Clase C{AccessNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{AccessNode}.
        """
        super(AccessNode, self).__init__()

