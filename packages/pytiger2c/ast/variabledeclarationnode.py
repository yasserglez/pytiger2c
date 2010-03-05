# -*- coding: utf-8 -*-

"""
Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode


class VariableDeclarationNode(DeclarationNode):
    """
    Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{VariableDeclarationNode}.
        """
        super(VariableDeclarationNode, self).__init__()

