# -*- coding: utf-8 -*-

"""
Clase C{RelationalLogicalOperatorNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.logicaloperatornode import LogicalOperatorNode
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.stringtype import StringType


class RelationalLogicalOperatorNode(LogicalOperatorNode):
    """
    Clase C{RelationalLogicalOperatorNode} del árbol de sintáxis abstracta.
    
    Esta clase implementa el método C{check_semantics} para los operadores
    logicos binarios relacionales. Estos operadores son los siguientes:
    menor que C{<}, menor igual que C{<=}, mayor que {>} y mayor igual 
    que C{>=}.
    """
    
    def __init__(self, left, right):
        """
        Inicializa la clase C{RelationalLogicalOperatorNode}.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{__init__}
        en la clase C{BinaryOperatorNode}.        
        """
        super(RelationalLogicalOperatorNode, self).__init__(left, right)
        self._code_operator = None

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por este método
        consulte la documentación del método C{check_semantics} en la clase 
        C{LanguageNode}.
        
        Los operadores cuyas clases del árbol de sintáxis abstracta derivan de esta
        deben recibir en ambos operandos números enteros o ambos cadenas de 
        caracteres. Siempre tienen tipo de retorno entero (1 para el resultado 
        verdadero, 0 para el falso).
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la expresión de la izquierda como la 
        expresión de la derecha. Luego se comprueba que ambas retornen valor y 
        que el tipo de retorno de ambas sea enteros o cadenas de caracteres.
        """
        self._scope = scope
        
        valid_types = (IntegerType(), StringType())
        
        errors_before = len(errors)
        
        self.right.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if self.right.has_return_value():
                if self.right.return_type not in valid_types: 
                    message = 'Invalid type of right operand in the binary ' \
                              'relational operator at line {line}'
                    errors.append(message.format(line=self.line_number))            
            else:
                message = 'Invalid use of binary relational operator with a ' \
                          'non-valued right expression at line {line}'
                errors.append(message.format(line=self.line_number))
        
        errors_before = len(errors)
            
        self.left.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            if self.left.has_return_value():
                if self.left.return_type not in valid_types: 
                    message = 'Invalid type of left operand in the binary ' \
                              'relational operator at line {line}'
                    errors.append(message.format(line=self.line_number))            
            else:
                message = 'Invalid use of binary relational operator with a ' \
                          'non-valued left expression at line {line}'
                errors.append(message.format(line=self.line_number))
                
            if self.right.return_type != self.left.return_type:
                message = 'Types of left and right operands of the binary ' \
                          'relational operator at line {line} does not match'
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
        else:
            stmt = '{result} = ({left} {op} {right});'
        stmt = stmt.format(result=result_var, 
                           op=self._code_operator,
                           left=self.left.code_name, 
                           right=self.right.code_name)
        generator.add_statement(stmt)
        self._code_name = result_var
