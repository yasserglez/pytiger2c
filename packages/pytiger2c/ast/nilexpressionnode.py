# -*- coding: utf-8 -*-

"""
Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.niltype import NilType


class NilExpressionNode(ValuedExpressionNode):
    """
    Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
    
    Representa la palabra reservada nil del lenguaje Tiger. El valor
    de retorno de esta expresión siempre será nil.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NilExpressionNode}.
        """
        super(NilExpressionNode, self).__init__()
        
    def check_semantics(self, error_list):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        """
        # Set the return type of the expression.
        self._return_type = NilType()

