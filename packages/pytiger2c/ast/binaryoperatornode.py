# -*- coding: utf-8 -*-

"""
Clase C{BinaryOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.operatornode import OperatorNode


class BinaryOperatorNode(OperatorNode):
    """
    Clase C{BinaryOperatorNode} del árbol de sintáxis abstracta.
    
    Representa la clase base para los operadores que se realizan 
    entre dos expresiones. De esta clase heredan los operadores 
    aritméticos y lógicos.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{BinaryOperatorNode}.
        
        @type left: LanguageNode
        @param left: LanguageNode correspondiente a la expresión a la 
            izquierda del operador.
        @type right: LanguageNode
        @param right: LanguageNode correspondiente a la expresión a la
            derecha del operador.
        """
        self._left = left
        self._right = right
        super(BinaryOperatorNode, self).__init__()

