# -*- coding: utf-8 -*-

"""
Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.operatornode import OperatorNode


class LogicalOperatorNode(OperatorNode):
    """
    Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{LogicalOperatorNode}.
        """
        super(LogicalOperatorNode, self).__init__()

