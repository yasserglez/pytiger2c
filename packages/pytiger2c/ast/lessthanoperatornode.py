# -*- coding: utf-8 -*-

"""
Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.relationallogicaloperatornode import RelationalLogicalOperatorNode


class LessThanOperatorNode(RelationalLogicalOperatorNode):
    """
    Clase C{LessThanOperatorNode} del árbol de sintáxis abstracta.
    
    Representa el operador de suma C{<} entre dos números enteros o dos
    cadenas de caracters del lenguaje Tiger.    
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{LessThanOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.           
        """
        super(LessThanOperatorNode, self).__init__(left, right)
