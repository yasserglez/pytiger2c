# -*- coding: utf-8 -*-

"""
Clase C{IfThenStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class IfThenStatementNode(NonValuedExpressionNode):
    """
    Clase C{IfThenStatementNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{IfThenStatementNode}.
        """
        super(IfThenStatementNode, self).__init__()

