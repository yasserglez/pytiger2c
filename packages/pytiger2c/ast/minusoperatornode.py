# -*- coding: utf-8 -*-

"""
Clase C{MinusOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode


class MinusOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{MinusOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{MinusOperatorNode}.
        """
        super(MinusOperatorNode, self).__init__()

