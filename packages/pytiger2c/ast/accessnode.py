# -*- coding: utf-8 -*-

"""
Clase C{AccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class AccessNode(ValuedExpressionNode):
    """
    Clase C{AccessNode} del árbol de sintáxis abstracta.
    
    Esta clase es la clase base para los nodos del árbol de sintáxis abstracta
    representando el acceso a una variable, un record o un array en el 
    lenguaje Tiger. Para más información consulte la documentación de las clases
    C{VariableAccessNode}, C{RecordAccessNode} y C{ArrayAccessNode}.
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
