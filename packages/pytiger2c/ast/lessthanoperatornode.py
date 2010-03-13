# -*- coding: utf-8 -*-

"""
Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.relationallogicaloperatornode import RelationalLogicalOperatorNode


class LessThanOperatorNode(RelationalLogicalOperatorNode):
    """
    Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{LessThanOperatorNode}.
        """
        super(LessThanOperatorNode, self).__init__()

