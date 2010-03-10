# -*- coding: utf-8 -*-

"""
Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class OrOperatorNode(LogicalOperatorNode):
    """
    Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{OrOperatorNode}.
        """
        super(OrOperatorNode, self).__init__(left, right)

