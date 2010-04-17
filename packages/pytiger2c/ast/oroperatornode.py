# -*- coding: utf-8 -*-

"""
Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.binarylogicaloperatornode import BinaryLogicalOperatorNode
from pytiger2c.types.integertype import IntegerType


class OrOperatorNode(BinaryLogicalOperatorNode):
    """
    Clase C{OrOperatorNode} del árbol de sintáxis abstracta.
    
    Representa la operación lógica C{OR}, representada con el operador C{|}
    en Tiger, entre dos números enteros. Este operador retornará 1 en caso
    de que el resultado de evaluar la expresión sea verdadero, 0 en otro caso.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{OrOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.           
        """
        super(OrOperatorNode, self).__init__(left, right)

    def generate_code(self, generator):
        """
        Genera el código C correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        @type generator: C{CodeGenerator}
        @param generator: Clase auxiliar utilizada en la generación del 
            código C correspondiente a un programa Tiger.        
        
        @raise CodeGenerationError: Esta excepción se lanzará cuando se produzca
            algún error durante la generación del código correspondiente al nodo.
            La excepción contendrá información acerca del error.
        """
        self.scope.generate_code(generator)
        result_var = generator.define_local(IntegerType().code_type)
        self.left.generate_code(generator)
        generator.add_statement('if ({left}) {{'.format(left=self.left.code_name))
        generator.add_statement('{result} = 1; }}'.format(result=result_var))
        generator.add_statement('else {')
        self.right.generate_code(generator)
        generator.add_statement('if ({right}) {{'.format(right=self.right.code_name))
        generator.add_statement('{result} = 1; }}'.format(result=result_var))
        generator.add_statement('else {')
        generator.add_statement('{result} = 0; }}'.format(result=result_var))
        generator.add_statement('}')
        self._code_name = result_var
