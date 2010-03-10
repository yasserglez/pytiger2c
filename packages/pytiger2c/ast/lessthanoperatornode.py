# -*- coding: utf-8 -*-

"""
Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class LessThanOperatorNode(LogicalOperatorNode):
    """
    Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{LessThanOperatorNode}.
        """
        super(LessThanOperatorNode, self).__init__(left, right)

