# -*- coding: utf-8 -*-

"""
Clase C{UnaryMinusOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode


class UnaryMinusOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{UnaryMinusOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{UnaryMinusOperatorNode}.
        """
        super(UnaryMinusOperatorNode, self).__init__()

