# -*- coding: utf-8 -*-

"""
Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binaryoperatornode import BinaryOperatorNode


class LogicalOperatorNode(BinaryOperatorNode):
    """
    Clase C{LogicalOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{LogicalOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.
        """
        super(LogicalOperatorNode, self).__init__(left, right)
