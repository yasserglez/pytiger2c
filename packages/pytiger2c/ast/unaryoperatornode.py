# -*- coding: utf-8 -*-

"""
Clase C{UnaryOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.operatornode import OperatorNode


class UnaryOperatorNode(OperatorNode):
    """
    Clase C{UnaryOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{UnaryOperatorNode}.
        """
        super(UnaryOperatorNode, self).__init__()

