# -*- coding: utf-8 -*-

"""
Clase C{GreaterEqualsThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class GreaterEqualsThanOperatorNode(LogicalOperatorNode):
    """
    Clase C{GreaterEqualsThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{GreaterEqualsThanOperatorNode}.
        """
        super(GreaterEqualsThanOperatorNode, self).__init__()

