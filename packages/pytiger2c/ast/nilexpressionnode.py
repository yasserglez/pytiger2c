# -*- coding: utf-8 -*-

"""
Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.niltype import NilType


class NilExpressionNode(ValuedExpressionNode):
    """
    Clase C{NilExpressionNode} del árbol de sintáxis abstracta.
    
    Representa la palabra reservada C{nil} del lenguaje Tiger. El valor
    de retorno de esta expresión siempre será C{nil}.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{NilExpressionNode}.
        """
        super(NilExpressionNode, self).__init__()
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Este nodo del árbol de sintáxis abstracta no requiere comprobación
        semántica, solamente se da valor al tipo de retorno del nodo que 
        siempre será C{NilType}.        
        """
        self._scope = scope
        self._return_type = NilType()

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        nil_code_type = NilType().code_type
        local_var = generator.define_local(nil_code_type)
        generator.add_statement('{0} = NULL;'.format(local_var))
        self._code_name = local_var
