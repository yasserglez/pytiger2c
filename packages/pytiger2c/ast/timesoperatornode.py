# -*- coding: utf-8 -*-

"""
Clase C{TimesOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode


class TimesOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{TimesOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{TimesOperatorNode}.
        """
        super(TimesOperatorNode, self).__init__(left, right)

