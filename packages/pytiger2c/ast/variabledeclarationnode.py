# -*- coding: utf-8 -*-

"""
Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode
from pytiger2c.scope import Scope


class VariableDeclarationNode(DeclarationNode):
    """
    Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}
        """
        return self._name
    
    name = property(_get_name)
    
    def _get_value(self):
        """
        Método para obtener el valor de la propiedad C{value}
        """
        return self._value
    
    value = property(_get_value)
    
    def _get_type(self):
        """
        Método para obtener el valor de la propiedad C{type}
        """
        return self._type.type
    
    type = property(_get_type)
    
    def __init__(self, name, value):
        """
        Inicializa la clase C{VariableDeclarationNode}.
        
        @type name: C{str}
        @param name: Nombre de la variable.
        
        @type value: C{LanguageNode}
        @param value: C{LanguageNode} correspondiente al valor que se asigna 
            a la variable.
        """
        super(VariableDeclarationNode, self).__init__()
        self._name = name
        self._value = value
        self._type = None        

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        label = '{type} \\n {name}'
        label = label.format(type=self.__class__.__name__, name=self.name)
        me = generator.add_node(label)        
        value = self.value.generate_dot(generator)
        generator.add_edge(me, value)
        return me
