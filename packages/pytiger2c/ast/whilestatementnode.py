# -*- coding: utf-8 -*-

"""
Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class WhileStatementNode(NonValuedExpressionNode):
    """
    Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{WhileStatementNode}.
        """
        super(WhileStatementNode, self).__init__()

