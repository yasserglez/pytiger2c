# -*- coding: utf-8 -*-

"""
Clase C{BinaryOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.operatornode import OperatorNode


class BinaryOperatorNode(OperatorNode):
    """
    Clase C{BinaryOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{BinaryOperatorNode}.
        """
        super(BinaryOperatorNode, self).__init__()

