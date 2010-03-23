# -*- coding: utf-8 -*-

"""
Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode


class AliasTypeDeclarationNode(TypeDeclarationNode):
    """
    Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la estructura C{alias} del lenguaje Tiger. La estructura
    C{alias} de Tiger recibe el nombre del nuevo tipo que se definirá y
    el nombre del tipo al que se le realiza un alias. De tal forma que
    instanciarlos a ambos resulta una operación equivalente.
    """
    
    def _get_alias_typename(self):
        """
        Método para obtener el valor de la propiedad C{alias_typename}.
        """
        return self._alias_typename
    
    alias_typename = property(_get_alias_typename)
    
    def __init__(self, name, alias_typename):
        """
        Inicializa la clase C{AliasTypeDeclarationNode}.
        
        @type alias_typename: C{str}
        @param alias_typename: Nombre del tipo al que se le hace alias.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}. 
        """
        super(AliasTypeDeclarationNode, self).__init__(name)
        self._alias_typename = alias_typename

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        """