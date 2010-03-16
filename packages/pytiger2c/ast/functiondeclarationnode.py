# -*- coding: utf-8 -*-

"""
Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode


class FunctionDeclarationNode(CallableDeclarationNode):
    """
    Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{FunctionDeclarationNode}.
        """
        super(FunctionDeclarationNode, self).__init__()
