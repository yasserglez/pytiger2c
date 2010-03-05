# -*- coding: utf-8 -*-

"""
Clase C{ValuedExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.languagenode import LanguageNode


class ValuedExpressionNode(LanguageNode):
    """
    Clase C{ValuedExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{ValuedExpressionNode}.
        """
        super(ValuedExpressionNode, self).__init__()

