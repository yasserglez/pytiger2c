# -*- coding: utf-8 -*-

"""
Clase C{AccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class AccessNode(ValuedExpressionNode):
    """
    Clase C{AccessNode} del árbol de sintáxis abstracta.
    """
    
    def _get_read_only(self):
        """
        Método para obtener el valor de la propiedad C{read_only}.
        """
        return self._read_only
    
    read_only = property(_get_read_only)
    
    def __init__(self):
        """
        Inicializa la clase C{AccessNode}.
        """
        super(AccessNode, self).__init__()
        self._read_only = False
