# -*- coding: utf-8 -*-

"""
Clase C{BreakStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class BreakStatementNode(NonValuedExpressionNode):
    """
    Clase C{BreakStatementNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{BreakStatementNode}.
        """
        super(BreakStatementNode, self).__init__()

