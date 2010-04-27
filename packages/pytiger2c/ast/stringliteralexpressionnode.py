# -*- coding: utf-8 -*-

"""
Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.stringtype import StringType


class StringLiteralExpressionNode(ValuedExpressionNode):
    """
    Clase C{StringLiteralExpressionNode} del árbol de sintáxis abstracta.
    
    Representa un literal de cadena en el lenguaje Tiger. El valor de 
    retorno de esta éxpresión siempre será C{StringType}.
    """
    
    def _get_string(self):
        """
        Método para obtener el valor de la propiedad C{string}.
        """
        return self._string    
   
    string = property(_get_string)    
    
    def __init__(self, string):
        """
        Inicializa la clase C{StringLiteralExpressionNode}.

        @type string: C{str}
        @param string: Valor del literal de cadena.
        """
        super(StringLiteralExpressionNode, self).__init__()
        self._string = string
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Este nodo del árbol de sintáxis abstracta no requiere comprobación
        semántica, solamente se da valor al tipo de retorno del nodo que 
        siempre será C{StringType}.
        """
        self._scope = scope
        self._return_type = StringType()

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        string_code_type = StringType().code_type
        local_var = generator.define_local(string_code_type)
        statement = '{local_var} = pytiger2c_malloc(sizeof({type}));'
        statement = statement.format(local_var = local_var, 
                                     type = string_code_type[:-1])
        generator.add_statement(statement)
        statement = '{local_var}->data = "{value}";'
        statement = statement.format(local_var = local_var,
                                     value = self.string)
        generator.add_statement(statement)
        statement = '{local_var}->length = strlen("{value}");'
        statement = statement.format(local_var = local_var,
                                     value = self.string)
        generator.add_statement(statement)
        self._code_name = local_var
