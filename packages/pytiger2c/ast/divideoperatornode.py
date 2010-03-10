# -*- coding: utf-8 -*-

"""
Clase C{DivideOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode


class DivideOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{DivideOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{DivideOperatorNode}.
        """
        super(DivideOperatorNode, self).__init__(left, right)

