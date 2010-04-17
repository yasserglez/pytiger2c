# -*- coding: utf-8 -*-

"""
Clase C{EqualityLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.stringtype import StringType
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class EqualityLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{EqualityLogicalOperatorNode} del árbol de sintáxis abstracta.
    
    Esta clase implementa el método C{check_semantics} para los operadores
    logicos binarios de igualadd y desigualdad. Estos operadores son los 
    siguientes: igual que C{=}, no igual que C{<>}.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{EqualityLogicalOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.          
        """
        super(EqualityLogicalOperatorNode, self).__init__(left, right)
        self._code_operator = None

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        Los operadores cuyas clases del árbol de sintáxis abstracta derivan de esta
        deben recibir en ambos operandos expresiones con valor de retorno y el tipo
        de estas debe ser el mismo. Siempre tienen tipo de retorno entero (1 para 
        el resultado verdadero, 0 para el falso).
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la expresión de la izquierda como la 
        expresión de la derecha. Luego se comprueba que ambas retornen valor y 
        que el tipo de retorno de ambas sea el mismo.
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.right.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.right.has_return_value():
                message = 'Invalid use of equality or inequality logical operator ' \
                          'with a non-valued right expression at line {line}'
                errors.append(message.format(line=self.line_number))
            
        self.left.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if not self.left.has_return_value():
                message = 'Invalid use of equality or inequality logical operator ' \
                          'with a non-valued left expression at line {line}'
                errors.append(message.format(line=self.line_number))
        
        if errors_before == len(errors):
            if self.right.return_type != self.left.return_type:
                # Check the special case of nil and records. nil can be assigned
                # to any record type, then r <> nil and r = nil are legal.
                valid_different_types = (RecordType, NilType)
                record_and_nil = (isinstance(self.right.return_type, valid_different_types) and 
                                  isinstance(self.left.return_type, valid_different_types))
                if not record_and_nil:
                    message = 'Types of left and right operands of the equality or ' \
                              'inequality logical operator at line {line} does not match'
                    errors.append(message.format(line=self.line_number))
        
        self._return_type = IntegerType()

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
        self.left.generate_code(generator)
        self.right.generate_code(generator)
        result_var = generator.define_local(IntegerType().code_type)
        if isinstance(self.left.return_type, StringType):
            stmt = '{result} = (pytiger2c_strcmp({left}, {right}) {op} 0);'
        elif isinstance(self.left, NilType):
            stmt = '{result} = ((({left_type}) {left}) {op} {right});'
        elif isinstance(self.right, NilType):
            stmt = '{result} = ({left} {op} (({right_type}) {right}));'
        else:
            stmt = '{result} = ({left} {op} {right});'
        stmt = stmt.format(result=result_var, 
                           op=self._code_operator,
                           left=self.left.code_name, 
                           right=self.right.code_name,
                           left_type=self.left.return_type.code_type,
                           right_type=self.right.return_type.code_type)
        generator.add_statement(stmt)
        self._code_name = result_var
