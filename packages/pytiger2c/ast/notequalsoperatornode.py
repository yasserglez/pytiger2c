# -*- coding: utf-8 -*-

"""
Clase C{NotEqualsOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class NotEqualsOperatorNode(LogicalOperatorNode):
    """
    Clase C{NotEqualsOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NotEqualsOperatorNode}.
        """
        super(NotEqualsOperatorNode, self).__init__()

