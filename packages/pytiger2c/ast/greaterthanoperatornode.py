# -*- coding: utf-8 -*-

"""
Clase C{GreaterThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class GreaterThanOperatorNode(LogicalOperatorNode):
    """
    Clase C{GreaterThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{GreaterThanOperatorNode}.
        """
        super(GreaterThanOperatorNode, self).__init__()

