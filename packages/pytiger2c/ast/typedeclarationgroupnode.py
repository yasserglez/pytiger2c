# -*- coding: utf-8 -*-

"""
Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class TypeDeclarationGroupNode(NonValuedExpressionNode):
    """
    Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
    """
    def _get_declarations(self):
        """
        Método para obtener el valor de la propiedad C{declarations}.
        """
        return self._declarations
    
    declarations = property(_get_declarations)
    
    def __init__(self):
        """
        Inicializa la clase C{TypeDeclarationGroupNode}.
        """
        super(TypeDeclarationGroupNode, self).__init__()
        self._declarations = []

    def check_semantics(self, scope, errors, used_types = None):
        """
        """
        


