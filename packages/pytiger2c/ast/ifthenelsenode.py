# -*- coding: utf-8 -*-

"""
Clase C{IfThenElseNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class IfThenElseNode(ValuedExpressionNode):
    """
    Clase C{IfThenElseNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{IfThenElseNode}.
        """
        super(IfThenElseNode, self).__init__()

