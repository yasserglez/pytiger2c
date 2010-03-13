# -*- coding: utf-8 -*-

"""
Clase C{EqualityLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class EqualityLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{EqualityLogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{EqualityLogicalOperatorNode}.
        """
        super(EqualityLogicalOperatorNode, self).__init__()

