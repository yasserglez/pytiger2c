# -*- coding: utf-8 -*-

"""
Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binarylogicaloperatornode import BinaryLogicalOperatorNode


class OrOperatorNode(BinaryLogicalOperatorNode):
    """
    Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{OrOperatorNode}.
        """
        super(OrOperatorNode, self).__init__()

