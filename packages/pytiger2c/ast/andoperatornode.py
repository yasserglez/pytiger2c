# -*- coding: utf-8 -*-

"""
Clase C{AndOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode


class AndOperatorNode(LogicalOperatorNode):
    """
    Clase C{AndOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{AndOperatorNode}.
        """
        super(AndOperatorNode, self).__init__()

