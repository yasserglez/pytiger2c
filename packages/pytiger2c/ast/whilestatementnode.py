# -*- coding: utf-8 -*-

"""
Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.ast import languagenode
from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.integertype import IntegerType


class WhileStatementNode(NonValuedExpressionNode):
    """
    Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{while-do} del lenguaje Tiger. La expresión C{while-do}
    tiene una condición y una expresión, de forma que evalua la condición y si esta 
    es distinta de cero, entonces la expresión es ejecutada. 
    """
    
    def __init__(self, condition, expression):
        """
        Inicializa la clase C{WhileStatementNode}.
        
        @type condition: LanguageNode
        @param condition: LanguageNode correspondiente a la condición que es evaluada, 
            de forma que si su valor es distinto de cero, la expresión es ejecutada.
        @type expression: LanguageNode
        @param expression: LanguageNode correspondiente a la expresión que es ejecutada,
            una vez que se verifica que la condición anterior es distinta de cero
        """
        self._condition = condition
        self._expression = expression
        super(WhileStatementNode, self).__init__()
        
    def check_semantics(self, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión C{while-do} recibe una condición y una expresión, 
        de forma que evalua la condición y si esta es distinta de cero, 
        entonces la expresión es ejecutada.
        
        En la comprobación semántica de este nodo del árbol de sintáxix abstracta
        se comprueban semánticamente tanto la condición como la expresión contenidas
        en este. Luego se comprueba que la condición retorne valor, que el mismo sea 
        de tipo C{IntegerType} y que la expresión no retorne valor. Se reportarán
        errores semánticos si se encuentran errores durante la comprobación semántica
        de la condición o la expresión, si la condición no retorna valor, si este valor
        de retorno no es te tipo C{IntegerType} o si la expresión retorna algún valor.
        """
        self._condition.check_semantics(errors)
        # The condition return type must be IntegerType
        if not self._condition.has_return_value():
            message = 'while used with a non-return condition at line {line}'
            errors.append(message.format(line=self.line_number))
        elif not isinstance(self._condition.return_type, IntegerType):
            message = 'Invalid type of condition of the while statement at line {line}'
            errors.append(message.format(line=self.line_number))
        self._expression.check_semantics(errors)
        # The expression must not return value
        if self._expression.has_return_value():
            message = 'while used with a expression with return value at line {line}'
            errors.append(message.format(line=self.line_number))