# -*- coding: utf-8 -*-

"""
Clase C{AndOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binarylogicaloperatornode import BinaryLogicalOperatorNode


class AndOperatorNode(BinaryLogicalOperatorNode):
    """
    Clase C{AndOperatorNode} del árbol de sintáxis abstracta.
    
    Representa la operación lógica C{AND}, representada con el operador C{&}
    en Tiger, entre dos números enteros. Este operador retornará 1 en caso
    de que el resultado de evaluar la expresión sea verdadero, 0 en otro caso.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{AndOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.        
        """
        super(AndOperatorNode, self).__init__(left, right)
