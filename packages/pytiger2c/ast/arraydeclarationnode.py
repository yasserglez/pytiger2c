# -*- coding: utf-8 -*-

"""
Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.arraytype import ArrayType


class ArrayDeclarationNode(TypeDeclarationNode):
    """
    Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, name, values_typename):
        """
        Inicializa la clase C{ArrayDeclarationNode}.
        
        @type values_typename: C{str}
        @param values_typename: Nombre del tipo que tendrán los valores del array.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}. 
        """
        super(ArrayDeclarationNode, self).__init__(name)
        self._type = ArrayType(values_typename) 
