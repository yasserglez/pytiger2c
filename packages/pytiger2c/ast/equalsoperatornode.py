# -*- coding: utf-8 -*-

"""
Clase C{EqualsOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class EqualsOperatorNode(LogicalOperatorNode):
    """
    Clase C{EqualsOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{EqualsOperatorNode}.
        """
        super(EqualsOperatorNode, self).__init__()

