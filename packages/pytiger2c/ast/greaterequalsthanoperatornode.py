# -*- coding: utf-8 -*-

"""
Clase C{GreaterEqualsThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.relationallogicaloperatornode import RelationalLogicalOperatorNode


class GreaterEqualsThanOperatorNode(RelationalLogicalOperatorNode):
    """
    Clase C{GreaterEqualsThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{GreaterEqualsThanOperatorNode}.
        """
        super(GreaterEqualsThanOperatorNode, self).__init__()

