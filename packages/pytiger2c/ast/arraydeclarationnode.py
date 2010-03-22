# -*- coding: utf-8 -*-

"""
Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.arraytype import ArrayType


class ArrayDeclarationNode(TypeDeclarationNode):
    """
    Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de declaración de un tipo C{array} en el lenguaje 
    Tiger. La estructura de declaración de C{array} recibe un nombre que es el 
    que representará a estos C{array} concretos y el nombre del tipo que van a 
    tener los valores.    
    """
    
    def __init__(self, name, values_typename):
        """
        Inicializa la clase C{ArrayDeclarationNode}.
        
        @type values_typename: C{str}
        @param values_typename: Nombre del tipo que tendrán los valores del 
            C{array}.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}. 
        """
        super(ArrayDeclarationNode, self).__init__(name)
        self._type = ArrayType(values_typename) 

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La comprobación semántica correspondiente a este nodo se realiza
        completamente a nivel del C{TypeDeclarationGroupNode} en que fue
        declarado. Pues es el C{TypeDeclarationGroupNode} el que comprueba
        que está definido el tipo de los valores de este C{array}, que el 
        nombre está disponible y además lo definie en su ámbito local.
        """

