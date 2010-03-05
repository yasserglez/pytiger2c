# -*- coding: utf-8 -*-

"""
Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode


class ArrayDeclarationNode(TypeDeclarationNode):
    """
    Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ArrayDeclarationNode}.
        """
        super(ArrayDeclarationNode, self).__init__()

