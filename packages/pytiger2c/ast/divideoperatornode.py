# -*- coding: utf-8 -*-

"""
Clase C{DivideOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.arithmeticoperatornode import ArithmeticOperatorNode
from pytiger2c.types.integertype import IntegerType


class DivideOperatorNode(ArithmeticOperatorNode):
    """
    Clase C{DivideOperatorNode} del árbol de sintáxis abstracta.
    
    Representa el operador de división C{/} entre dos números enteros 
    del lenguaje Tiger.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{DivideOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{__init__} en la clase C{BinaryOperatorNode}.
        """
        super(DivideOperatorNode, self).__init__(left, right)
        self._operator = '/'
    
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método 
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        El operador de división realiza la división entre los el valor de la expresión
        que se encuentra a la izquierda entre el valor de la derecha.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la expresión de la izquierda como la 
        expresión de la derecha. Luego se comprueba que ambas retornen valor y 
        que el valor de retorno de ambas sea entero. 
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.right.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.right.has_return_value():
                message = 'Invalid use of divide operator with a non-valued right expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.right.return_type != IntegerType():
                message = 'Invalid use of divide operator with a non-integer right value at line {line}'
                errors.append(message.format(line=self.line_number))
                
        errors_before = len(errors)
        
        self.left.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.left.has_return_value():
                message = 'Invalid use of divide operator with a non-valued left expression at line {line}'
                errors.append(message.format(line=self.line_number)) 
            elif self.left.return_type != IntegerType():
                message = 'Invalid use of divide operator with a non-integer left value at line {line}'
                errors.append(message.format(line=self.line_number))
            
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
        self.right.generate_code(generator)
        self.left.generate_code(generator)
        #Check if zero division
        statement = 'if({var} == 0){{pytiger2c_error("{msg}.");}}'
        statement = statement.format(var = self.right.code_name, 
                                     msg = "Integer divison by zero")       
        generator.add_statement(statement)
        int_code_type = IntegerType().code_type
        local_var = generator.define_local(int_code_type)
        statement = '{var} = {left} {operator} {right};'
        statement = statement.format(var = local_var, left = self.left.code_name, 
                                     operator = self._operator, 
                                     right = self.right.code_name)
        generator.add_statement(statement)
        self._code_name = local_var