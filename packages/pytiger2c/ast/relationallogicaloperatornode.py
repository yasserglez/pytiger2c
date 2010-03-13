# -*- coding: utf-8 -*-

"""
Clase C{RelationalLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class RelationalLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{RelationalLogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{RelationalLogicalOperatorNode}.
        """
        super(RelationalLogicalOperatorNode, self).__init__()

