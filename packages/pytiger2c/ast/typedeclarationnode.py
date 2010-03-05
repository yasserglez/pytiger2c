# -*- coding: utf-8 -*-

"""
Clase C{TypeDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode


class TypeDeclarationNode(DeclarationNode):
    """
    Clase C{TypeDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{TypeDeclarationNode}.
        """
        super(TypeDeclarationNode, self).__init__()

