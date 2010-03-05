# -*- coding: utf-8 -*-

"""
Clase C{VariableAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode


class VariableAccessNode(AccessNode):
    """
    Clase C{VariableAccessNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{VariableAccessNode}.
        """
        super(VariableAccessNode, self).__init__()

