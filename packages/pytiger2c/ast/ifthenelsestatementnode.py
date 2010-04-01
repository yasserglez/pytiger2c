# -*- coding: utf-8 -*-

"""
Clase C{IfThenElseStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class IfThenElseStatementNode(ValuedExpressionNode):
    """
    Clase C{IfThenElseStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{if-then-else} del lenguaje Tiger. La expresión 
    C{if-then-else} permite la ejecución condicional fragmentos de código. 
    Primeramente se evalúa la expresión seguida de la instrucción C{if}, que debe 
    retornar un número entero; si su valor es diferente de cero entonces se 
    ejecutará la expresión seguida de la instrucción C{then} y este será el valor 
    de retorno de la expresión, en caso contrario se ejecutará la expresión 
    seguida de la instrucción C{else} y este será el valor de retorno de la 
    expresión. Por tanto, la expresión seguida de la instrucción C{then} y 
    la expresión seguida de la instrucción C{else} deben tener el mismo tipo 
    de retorno o ambas no tener valor de retorno.
    """
    
    def _get_condition(self):
        """
        Método para obtener el valor de la propiedad C{condition}.
        """
        return self._condition
        
    condition = property(_get_condition)
    
    def _get_then_expression(self):
        """
        Método para obtener el valor de la propiedad C{then_expression}.
        """
        return self._then_expression
        
    then_expression = property(_get_then_expression)
    
    def _get_else_expression(self):
        """
        Método para obtener el valor de la propiedad C{else_expression}.
        """
        return self._else_expression
        
    else_expression = property(_get_else_expression)    
    
    def __init__(self, condition, then_expression, else_expression):
        """
        Inicializa la clase C{IfThenElseStatementNode}.
        
        @type condition: C{LanguageNode}
        @param condition: Expresión que se debe evaluar para decidir si se debe
            ejecutar la expresión seguida de la instrucción C{then} o la expresión
            seguida de la instrucción C{else}.
        
        @type then_expression: C{LanguageNode}
        @param then_expression: Expresión que se ejeccutará si el valor de
            retorno de la condición fue distinto de cero.
            
        @type else_expression: C{LanguageNode}
        @param else_expression: Expresión que se ejeccutará si el valor de
            retorno de la condición fue cero.          
        """
        super(IfThenElseStatementNode, self).__init__()
        self._condition = condition
        self._then_expression = then_expression
        self._else_expression = else_expression

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión seguida de la instrucción C{if}, cuyo nodo del árbol de 
        sintáxis abstracta está almacenado en la propiedad C{condition}, deberá 
        tener valor de retorno entero. Las expresiones seguidas de las 
        instrucciones C{then} y C{else} deben tener el mismo tipo de retorno
        o no tener valor de retorno ambas. El tipo del valor de retorno de la 
        expresión C{if-then-else} será el mismo que el de estas expresiones o
        no retornará valor si estas no lo hacen. 
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta 
        primeramente se comprueba que la expresión seguida de la instrucción C{if}
        esté correcta semánticamente, que tenga valor de retorno y que sea de tipo 
        C{IntegerType}. Luego, se comprueba que las expresiones seguidas de las 
        instrucciones C{then} y C{else} estén correctas semánticamente y que el 
        tipo de su valor de retorno sea el mismo o ambas no tengan valor de retorno.
        Para finalizar especifica el tipo de retorno que tendrá la expresión, 
        el cual coincidirá con el tipo de las expresiones.
        """
        self._scope = scope
        
        # Check semantics of the condition expression.
        self.condition.check_semantics(scope, errors)
        if not self.condition.has_return_value():
            message = 'The condition of the if-then-else statement at line {line} ' \
                       'does not return a value'
            errors.append(message.format(line=self.line_number))
        elif self.condition.return_type != IntegerType():
            message = 'The condition of the if-then-else statement at line {line} ' \
                      'does not return an integer value'
            errors.append(message.format(line=self.line_number))
            
        # Check semantics of the then and else expressions.
        errors_before = len(errors)
        
        self.then_expression.check_semantics(scope, errors)
        self.else_expression.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            then_returns = self.then_expression.has_return_value()
            else_returns = self.else_expression.has_return_value()
            if then_returns and else_returns:
                if self.then_expression.return_type != self.else_expression.return_type:
                    # Check the special case of nil and records. 
                    valid_different_types = (RecordType, NilType)
                    record_and_nil = (isinstance(self.then_expression.return_type, valid_different_types) and 
                                      isinstance(self.else_expression.return_type, valid_different_types))
                    if not record_and_nil:                    
                        message = 'The return type of the expressions of the if-then-else ' \
                                  'statement at line {line} is not the same'
                        errors.append(message.format(line=self.line_number))
            elif then_returns or else_returns:
                message = 'One of the expressions of the if-then-else statement at ' \
                          'line {line} returns but the other does not'
                errors.append(message.format(line=self.line_number))
                        
            # Set the return type of the expression (if any).
            if then_returns and else_returns:
                self._return_type = self.then_expression.return_type

    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.
        
        La expresión C{if-then-else} no tiene valor de retorno cuando las expresiones
        seguidas de las instrucciones C{then} y C{else} no tiene valor de retorno.
        Debido a esto, este nodo debe redefinir el método C{has_return_value} para
        cambiar la implementación provista por la clase C{ValuedExpressionNode} que
        siempre retorna C{True}.   
        """
        return self.then_expression.has_return_value()
