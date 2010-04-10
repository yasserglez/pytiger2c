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
    
    def _get_left(self):
        """
        Método para obtener el valor de la propiedad C{left}.
        """
        return self._left
    
    left = property(_get_left)
    
    def _get_right(self):
        """
        Método para obtener el valor de la propiedad C{right}.
        """
        return self._right
    
    right = property(_get_right)    
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{BinaryOperatorNode}.
        
        @type left: C{LanguageNode}
        @param left: Nodo del árbol de sintáxis abstracta correspondiente 
            a la expresión a la izquierda del operador.
            
        @type right: C{LanguageNode}
        @param right: Nodo del árbol de sintáxis abstracta correspondiente 
            a la expresión a la derecha del operador.
        """
        super(BinaryOperatorNode, self).__init__()
        self._left = left
        self._right = right

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        left = self.left.generate_dot(generator)
        right = self.right.generate_dot(generator)
        generator.add_edge(me, left)
        generator.add_edge(me, right)
        return me
