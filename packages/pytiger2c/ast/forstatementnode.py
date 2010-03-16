# -*- coding: utf-8 -*-

"""
Clase C{ForStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class ForStatementNode(NonValuedExpressionNode):
    """
    Clase C{ForStatementNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ForStatementNode}.
        """
        super(ForStatementNode, self).__init__()
