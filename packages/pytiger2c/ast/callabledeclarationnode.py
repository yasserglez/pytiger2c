# -*- coding: utf-8 -*-

"""
Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode


class CallableDeclarationNode(DeclarationNode):
    """
    Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{CallableDeclarationNode}.
        """
        super(CallableDeclarationNode, self).__init__()

