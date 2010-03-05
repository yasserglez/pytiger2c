# -*- coding: utf-8 -*-

"""
Clase C{LetNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class LetNode(ValuedExpressionNode):
    """
    Clase C{LetNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{LetNode}.
        """
        super(LetNode, self).__init__()

