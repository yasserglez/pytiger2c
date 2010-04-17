# -*- coding: utf-8 -*-

"""
Clase C{ArithmeticOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binaryoperatornode import BinaryOperatorNode
from pytiger2c.types.integertype import IntegerType


class ArithmeticOperatorNode(BinaryOperatorNode):
    """
    Clase C{ArithmeticOperatorNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{ArithmeticOperatorNode}.
        """
        super(ArithmeticOperatorNode, self).__init__(left, right)
        self._operator = ''

    
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        self.right.generate_code(generator)
        self.left.generate_code(generator)
        int_code_type = IntegerType().code_type
        local_var = generator.define_local(int_code_type)
        statement = '{var} = {left} {operator} {right};'.format(var = local_var,
                                                                left = self.left.code_name,
                                                                operator = self._operator,
                                                                right = self.right.code_name)
        generator.add_statement(statement)
        self._code_name = local_var