# -*- coding: utf-8 -*-

"""
Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.stringtype import StringType


class StringLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa un literal de cadena en el lenguaje Tiger. El valor de 
    retorno de esta éxpresión siempre será C{StringType}.
    """
    
    def _get_string(self):
        """
        Método para obtener el valor de la propiedad C{string}.
        """
        return self._string
    
    string = property(_get_string, None, 'Valor del literal de cadena')    
    
    def __init__(self, string):
        """
        Inicializa la clase C{StringLiteralExpressionNode}.

        @type string: C{str}
        @param string: Valor del literal de cadena.
        """
        super(StringLiteralExpressionNode, self).__init__()
        self._string = string
        
    def check_semantics(self, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        """
        # Set the return type of the expression.
        self._return_type = StringType()
