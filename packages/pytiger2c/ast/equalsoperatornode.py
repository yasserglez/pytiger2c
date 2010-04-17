# -*- coding: utf-8 -*-

"""
Clase C{EqualsOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.equalitylogicaloperatornode import EqualityLogicalOperatorNode


class EqualsOperatorNode(EqualityLogicalOperatorNode):
    """
    Clase C{EqualsOperatorNode} del árbol de sintáxis abstracta.
    
    Representa el operador C{=} entre dos expresiones del lenguaje Tiger.    
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{EqualsOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.            
        """
        super(EqualsOperatorNode, self).__init__(left, right)
        self._code_operator = '=='
