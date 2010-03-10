# -*- coding: utf-8 -*-

"""
Clase C{ArithmeticOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binaryoperatornode import BinaryOperatorNode


class ArithmeticOperatorNode(BinaryOperatorNode):
    """
    Clase C{ArithmeticOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ArithmeticOperatorNode}.
        """
        super(ArithmeticOperatorNode, self).__init__()

