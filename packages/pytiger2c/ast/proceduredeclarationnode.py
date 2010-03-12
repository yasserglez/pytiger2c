# -*- coding: utf-8 -*-

"""
Clase C{ProcedureDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode


class ProcedureDeclarationNode(CallableDeclarationNode):
    """
    Clase C{ProcedureDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ProcedureDeclarationNode}.
        """
        super(ProcedureDeclarationNode, self).__init__()
