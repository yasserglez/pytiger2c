# -*- coding: utf-8 -*-

"""
Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binaryoperatornode import BinaryOperatorNode


class LogicalOperatorNode(BinaryOperatorNode):
    """
    Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{LogicalOperatorNode}.
        """
        super(LogicalOperatorNode, self).__init__()

