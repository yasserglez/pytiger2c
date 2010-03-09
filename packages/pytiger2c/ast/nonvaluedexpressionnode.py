# -*- coding: utf-8 -*-

"""
Clase C{NonValuedExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.languagenode import LanguageNode


class NonValuedExpressionNode(LanguageNode):
    """
    Clase C{NonValuedExpressionNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NonValuedExpressionNode}.
        """
        super(NonValuedExpressionNode, self).__init__()
        
    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.      
        """
        return False
