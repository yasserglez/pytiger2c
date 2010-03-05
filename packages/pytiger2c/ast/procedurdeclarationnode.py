# -*- coding: utf-8 -*-

"""
Clase C{ProcedurDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode


class ProcedurDeclarationNode(CallableDeclarationNode):
    """
    Clase C{ProcedurDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ProcedurDeclarationNode}.
        """
        super(ProcedurDeclarationNode, self).__init__()

