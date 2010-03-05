# -*- coding: utf-8 -*-

"""
Clase C{LessEqualsThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class LessEqualsThanOperatorNode(LogicalOperatorNode):
    """
    Clase C{LessEqualsThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{LessEqualsThanOperatorNode}.
        """
        super(LessEqualsThanOperatorNode, self).__init__()

