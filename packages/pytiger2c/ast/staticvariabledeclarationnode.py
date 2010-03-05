# -*- coding: utf-8 -*-

"""
Clase C{StaticVariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.variabledeclarationnode import VariableDeclarationNode


class StaticVariableDeclarationNode(VariableDeclarationNode):
    """
    Clase C{StaticVariableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{StaticVariableDeclarationNode}.
        """
        super(StaticVariableDeclarationNode, self).__init__()

