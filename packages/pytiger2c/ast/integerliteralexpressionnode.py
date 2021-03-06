# -*- coding: utf-8 -*-

"""
Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.integertype import IntegerType


class IntegerLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{IntegerLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa un literal de un número entero en el lenguaje Tiger. El valor
    de retorno de esta expresión siempre será C{IntegerType}.
    """
    
    def _get_integer(self):
        """
        Método para obtener el valor de la propiedad C{integer}.
        """
        return self._integer    
    
    integer = property(_get_integer)
    
    def __init__(self, integer):
        """
        Inicializa la clase C{IntegerLiteralExpressionNode}.
        
        @type integer: C{int}
        @param integer: Valor del número entero literal.
        """
        super(IntegerLiteralExpressionNode, self).__init__()
        self._integer = integer

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Este nodo del árbol de sintáxis abstracta no requiere comprobación
        semántica, solamente se da valor al tipo de retorno del nodo que 
        siempre será C{IntegerType}.        
        """
        self._scope = scope
        self._return_type = IntegerType()

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        int_code_type = IntegerType().code_type
        local_var = generator.define_local(int_code_type)
        generator.add_statement('{0} = {1};'.format(local_var, self.integer))
        self._code_name = local_var
