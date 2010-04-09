# -*- coding: utf-8 -*-

"""
Clase C{TypeDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode


class TypeDeclarationNode(DeclarationNode):
    """
    Clase C{TypeDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa las distintas declaraciones de tipos presentes en el lenguaje de
    Tige. De esta clase heredan las declaraciones de records, arrays y alias 
    como tipos válidos de Tiger.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}.
        """
        return self._name
    
    def _set_name(self, name):
        """
        Método para cambiar el valor de la propiedad C{name}.
        """
        self._name = name
    
    name = property(_get_name, _set_name)
    
    def _get_type(self):
        """
        Método para obtener el valor de la propiedad C{type}.
        """
        return self._type
    
    type = property(_get_type)
    
    
    def __init__(self, name):
        """
        Inicializa la clase C{TypeDeclarationNode}.
        
        @type name: C{str}
        @param name: Nombre que se le asignará a este nuevo tipo.
        """
        super(TypeDeclarationNode, self).__init__()
        self._name = name
        self._type = None
