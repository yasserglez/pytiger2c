# -*- coding: utf-8 -*-

"""
Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.types.integertype import IntegerType


class WhileStatementNode(NonValuedExpressionNode):
    """
    Clase C{WhileStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{while-do} del lenguaje Tiger. La expresión C{while-do}
    tiene una condición y una expresión, de forma que evalua la condición y si esta 
    es distinta de cero, entonces la expresión es ejecutada. 
    """
    
    def _get_condition(self):
        """
        Método para obtener el valor de la propiedad C{condition}.
        """
        return self._condition
        
    condition = property(_get_condition)
    
    def _get_expression(self):
        """
        Método para obtener el valor de la propiedad C{expression}.
        """
        return self._expression
        
    expression = property(_get_expression)
    
    def __init__(self, condition, expression):
        """
        Inicializa la clase C{WhileStatementNode}.
        
        @type condition: C{LanguageNode}
        @param condition: Nodo del árbol de sintáxis abstracta correspondiente a
            la condición que es evaluada, de forma que si su valor es distinto de 
            cero, la expresión es ejecutada.
            
        @type expression: C{LanguageNode}
        @param expression: Nodo del árbol de sintáxis abstracta correspondiente a 
            la expresión que es ejecutada, una vez que se verifica que la condición 
            anterior es distinta de cero.
        """
        super(WhileStatementNode, self).__init__()
        self._condition = condition
        self._expression = expression
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión C{while-do} recibe una condición y una expresión, 
        de forma que evalua la condición y si esta es distinta de cero, 
        entonces la expresión es ejecutada.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se comprueban semánticamente tanto la condición como la expresión contenidas
        en este. Luego se comprueba que la condición retorne valor, que el mismo sea 
        de tipo C{IntegerType} y que la expresión no retorne valor. Se reportarán
        errores semánticos si se encuentran errores durante la comprobación semántica
        de la condición o la expresión, si la condición no retorna valor, si este valor
        de retorno no es te tipo C{IntegerType} o si la expresión retorna algún valor.
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        self.condition.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            # The condition return type must be IntegerType
            if not self.condition.has_return_value():
                message = 'while used with a non-return condition at line {line}'
                errors.append(message.format(line=self.line_number))
            elif self.condition.return_type != IntegerType():
                message = 'Invalid type of condition of the while statement at line {line}'
                errors.append(message.format(line=self.line_number))

        errors_before = len(errors)
        
        self.expression.check_semantics(scope, errors)
        
        if errors_before == len(errors):
            # The expression must not return value
            if self.expression.has_return_value():
                message = 'while used with a expression with return value at line {line}'
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
        expression = self.expression.generate_dot(generator)
        generator.add_edge(me, condition)
        generator.add_edge(me, expression)
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
        condition_code_type = self.condition.return_type.code_type
        local_var = generator.define_local(condition_code_type)
        statement = '{var} = {cond};'.format(var = local_var, 
                                             cond = self.condition.code_name)
        generator.add_statement(statement)
        generator.add_statement('while({0})'.format(local_var))
        generator.add_statement('{{')
        self.expression.generate_code(generator)
        generator.add_statement('/* Condition code*/')
        self.condition.generate_code(generator)
        statement = '{var} = {cond};'.format(var = local_var,
                                             cond = self.condition.code_name)
        generator.add_statement(statement)
        generator.add_statement('}}')