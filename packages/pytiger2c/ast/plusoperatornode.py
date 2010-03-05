# -*- coding: utf-8 -*-

"""
Clase C{PlusOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode


class PlusOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{PlusOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{PlusOperatorNode}.
        """
        super(PlusOperatorNode, self).__init__()

