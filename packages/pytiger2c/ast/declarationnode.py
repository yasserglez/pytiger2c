# -*- coding: utf-8 -*-

"""
Clase C{DeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class DeclarationNode(NonValuedExpressionNode):
    """
    Clase C{DeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{DeclarationNode}.
        """
        super(DeclarationNode, self).__init__()
