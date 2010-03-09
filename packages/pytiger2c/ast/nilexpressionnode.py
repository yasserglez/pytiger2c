# -*- coding: utf-8 -*-

"""
Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.niltype import NilType


class NilExpressionNode(ValuedExpressionNode):
    """
    Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
    
    Representa la palabra reservada C{nil} del lenguaje Tiger. El valor
    de retorno de esta expresión siempre será C{nil}.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NilExpressionNode}.
        """
        super(NilExpressionNode, self).__init__()
        
    def check_semantics(self, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Este nodo del árbol de sintáxis abstracta no requiere comprobación
        semántica, solamente se da valor al tipo de retorno del nodo que 
        siempre será C{NilType}.        
        """
        # Set the return type of the expression.
        self._return_type = NilType()

