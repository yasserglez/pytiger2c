# -*- coding: utf-8 -*-

"""
Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode


class AliasTypeDeclarationNode(TypeDeclarationNode):
    """
    Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{AliasTypeDeclarationNode}.
        """
        super(AliasTypeDeclarationNode, self).__init__()
