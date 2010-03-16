# -*- coding: utf-8 -*-

"""
Clase C{AssignmentNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class AssignmentNode(NonValuedExpressionNode):
    """
    Clase C{AssignmentNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{AssignmentNode}.
        """
        super(AssignmentNode, self).__init__()
