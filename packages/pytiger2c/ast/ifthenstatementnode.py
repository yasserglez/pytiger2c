# -*- coding: utf-8 -*-

"""
Clase C{IfThenStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.types.integertype import IntegerType


class IfThenStatementNode(NonValuedExpressionNode):
    """
    Clase C{IfThenStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{if-then} del lenguaje Tiger. La expresión C{if-then}
    permite la ejecución condicional de un fragmento de código. Primeramente se
    evalúa la expresión seguida de la instrucción C{if}, que debe retornar un 
    número entero; si su valor es diferente de cero entonces se ejecutará la 
    expresión seguida de la instrucción C{then} que no debe tener valor
    de retorno. 
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
    
    def __init__(self, condition, then_expression):
        """
        Inicializa la clase C{IfThenStatementNode}.
        
        @type condition: C{LanguageNode}
        @param condition: Expresión que se debe evaluar para decidir si se debe
            ejecutar la expresión seguida de la instrucción C{then}.
        
        @type then_expression: C{LanguageNode}
        @param then_expression: Expresión que se ejeccutará si el valor de
            retorno de la condición fue distinto de cero. Esta expresión
            no debe tener valor de retorno.
        """
        super(IfThenStatementNode, self).__init__()
        self._condition = condition
        self._then_expression = then_expression

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión seguida de la instrucción C{if}, cuyo nodo del árbol de 
        sintáxis abstracta está almacenado en la propiedad C{condition}, deberá 
        tener valor de retorno entero. La expresión seguida de la instrucción
        C{then} no debe tener valor de retorno.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta 
        primeramente se comprueba que la expresión seguida de la instrucción C{if}
        esté correcta semánticamente, que tenga valor de retorno y que sea de tipo 
        C{IntegerType}. Luego se comprueba que la expresión seguida de la 
        instrucción C{then} esté correcta semánticamente y que no tenga valor 
        de retorno.
        """
        self._scope = scope
        
        # Check semantics of the condition expression.
        self.condition.check_semantics(scope, errors)
        if not self.condition.has_return_value():
            message = 'The condition of the if-then statement at line {line} ' \
                       'does not return a value'
            errors.append(message.format(line=self.line_number))
        elif self.condition.return_type != IntegerType():
            message = 'The condition of the if-then statement at line {line} ' \
                      'does not return an integer value'
            errors.append(message.format(line=self.line_number))

        # Check semantics of the then expression.
        self.then_expression.check_semantics(scope, errors)
        if self.then_expression.has_return_value():
            message = 'The then expression of the if-then statement ' \
                      'at line {line} should not return a value'
            errors.append(message.format(line=self.line_number))

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        condition = self.condition.generate_dot(generator)
        then_expression = self.then_expression.generate_dot(generator)
        generator.add_edge(me, condition)
        generator.add_edge(me, then_expression)
        return me

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        
        self.condition.generate_code(generator)
        generator.add_statement('if({0})'.format(self.condition.code_name))
        generator.add_statement('{')
        self.then_expression.generate_code(generator)
        generator.add_statement('}')