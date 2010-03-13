# -*- coding: utf-8 -*-

"""
Clase C{BinaryLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class BinaryLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{BinaryLogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{BinaryLogicalOperatorNode}.
        """
        super(BinaryLogicalOperatorNode, self).__init__()

