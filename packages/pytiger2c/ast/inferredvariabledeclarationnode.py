# -*- coding: utf-8 -*-

"""
Clase C{InferredVariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.variabledeclarationnode import VariableDeclarationNode


class InferredVariableDeclarationNode(VariableDeclarationNode):
    """
    Clase C{InferredVariableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{InferredVariableDeclarationNode}.
        """
        super(InferredVariableDeclarationNode, self).__init__()
