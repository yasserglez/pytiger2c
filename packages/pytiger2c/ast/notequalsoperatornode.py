# -*- coding: utf-8 -*-

"""
Clase C{NotEqualsOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.equalitylogicaloperatornode import EqualityLogicalOperatorNode


class NotEqualsOperatorNode(EqualityLogicalOperatorNode):
    """
    Clase C{NotEqualsOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NotEqualsOperatorNode}.
        """
        super(NotEqualsOperatorNode, self).__init__()

