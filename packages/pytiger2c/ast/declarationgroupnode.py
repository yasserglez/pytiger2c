# -*- coding: utf-8 -*-

"""
Clase C{DeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class DeclarationGroupNode(NonValuedExpressionNode):
    """
    Clase C{DeclarationGroupNode} del árbol de sintáxis abstracta.
    """
    def _get_declarations(self):
        """
        Método para obtener el valor de la propiedad C{declarations}.
        """
        return self._declarations
    
    declarations = property(_get_declarations)
    
    def __init__(self):
        """
        Inicializa la clase C{DeclarationGroupNode}.
        """
        super(DeclarationGroupNode, self).__init__()
        self._declarations = []
        
    def collect_definitions(self, scope, errors):
        """        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        @rtype: C{set}
        @return: Conjunto con los nombres de los tipos o funciones que se 
            definen en este  grupo.
        """
        raise NotImplementedError()
