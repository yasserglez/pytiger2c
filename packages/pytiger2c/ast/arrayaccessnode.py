# -*- coding: utf-8 -*-

"""
Clase C{ArrayAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode


class ArrayAccessNode(AccessNode):
    """
    Clase C{ArrayAccessNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ArrayAccessNode}.
        """
        super(ArrayAccessNode, self).__init__()
