# -*- coding: utf-8 -*-

"""
Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode


class RecordAccessNode(AccessNode):
    """
    Clase C{RecordAccessNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{RecordAccessNode}.
        """
        super(RecordAccessNode, self).__init__()
