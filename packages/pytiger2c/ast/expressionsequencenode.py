# -*- coding: utf-8 -*-

"""
Clase C{ExpressionSequenceNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode


class ExpressionSequenceNode(ValuedExpressionNode):
    """
    Clase C{ExpressionSequenceNode} del árbol de sintáxis abstracta.
    
    Este nodo representa una secuencia de expresiones del lenguaje Tiger separadas
    por el caracter punto y coma que se ejecutan en el orden en que estas aparecen.
    Esta secuencia de expresiones puede ser vacía. El valor de retorno de una 
    secuencia de expresiones será el valor de la última expresión de la secuencia
    si esta existe y no tendrá valor de retorno en caso de que sea una secuencia
    de expresiones vacía.
    """
    
    def _get_expressions(self):
        """
        Método para obtener el valor de la propiedad C{expressions}.
        """
        return self._expressions
        
    expressions = property(_get_expressions)
        
    def __init__(self):
        """
        Inicializa la clase C{ExpressionSequenceNode}.
        """
        super(ExpressionSequenceNode, self).__init__()
        self._expressions = []

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxix abstracta
        se comprueban semánticamente cada una de las expresiones de la secuencia
        y posteriormente se asigna el tipo de retorno de la expresión que será
        el de la última expresión de la secuencia. Si el nodo representa una
        secuencia de expresiones vacía entonces no tendrá valor de retorno.         
        """
        self._scope = scope
        
        errors_before_last = None
        
        # Check semantics of the expressions in the sequence.
        for expression in self._expressions:
            errors_before_last = len(errors)
            expression.check_semantics(scope, errors)

        if errors_before_last == len(errors):
            try:
                if self._expressions[-1].has_return_value():
                    self._return_type = self._expressions[-1].return_type
            except IndexError:
                # Ignore this exception, the node does not have a return value.
                pass
        
    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.
        
        Una secuencia de expresiones no tiene valor de retorno cuando es una
        secuencia vacía o cuando la última expresión de la secuencia no 
        tiene valor de retorno. Debido a esto, este nodo debe redefinir el 
        método C{has_return_value} para cambiar la implementación provista 
        por la clase C{ValuedExpressionNode} que siempre retorna C{True}.   
        """
        try:
            return self._expressions[-1].has_return_value()
        except IndexError:
            return False        
