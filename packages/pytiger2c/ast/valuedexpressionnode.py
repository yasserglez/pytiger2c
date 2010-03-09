# -*- coding: utf-8 -*-

"""
Clase C{ValuedExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.languagenode import LanguageNode


class ValuedExpressionNode(LanguageNode):
    """
    Clase C{ValuedExpressionNode} del árbol de sintáxis abstracta.
    
    Esta clase encabeza la jerarquía de clases que representan estructuras del
    lenguaje Tiger que tienen un valor de retorno. Todas las clases que deriven
    de C{ValuedExpressionNode} deben definir el valor de la propiedad C{return_type},
    según el tipo de retorno de la expresión, al terminar la ejecución del método
    C{check_semantics}. El valor retornado por la propiedad C{return_type}
    será una instancia de un descendiente de la clase C{TigerType} ó C{None} en 
    el caso excepcional en que la expresión no tenga ningún valor de retorno.
    """
    
    def _get_return_type(self):
        """Método para obtener el valor de la propiedad C{return_type}.
        """
        return self._return_type    
    
    return_type = property(_get_return_type)
    
    def __init__(self):
        """
        Inicializa la clase C{ValuedExpressionNode}.
        """
        super(ValuedExpressionNode, self).__init__()
        self._return_type = None
        
    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.      
        """
        return True
