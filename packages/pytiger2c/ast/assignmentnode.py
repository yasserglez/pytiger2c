# -*- coding: utf-8 -*-

"""
Clase C{AssignmentNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class AssignmentNode(NonValuedExpressionNode):
    """
    Clase C{AssignmentNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de asignación del lenguaje Tiger. La estructura 
    de asignación tiene una expresion (lvalue) de acceso a una variable, un 
    elemento de un C{array} o un campo de un C{record} y un valor que se le 
    asignará a este acceso.
    """
    
    def _get_lvalue(self):
        """
        Método para obtener el valor de la propiedad C{lvalue}.
        """
        return self._lvalue
    
    lvalue = property(_get_lvalue)
    
    def _get_expression(self):
        """
        Método para obtener el valor de la propiedad C{expression}.
        """
        return self._expression
    
    expression = property(_get_expression)
        
    
    def __init__(self, lvalue, expression):
        """
        Inicializa la clase C{AssignmentNode}.
        
        @type lvalue: C{AccessNode}.
        @param lvalue: Expresión a la que se le quiere asignar la expresión.
        
        @type expression: C{LanguageNode}
        @param expresion: Expresión
        """
        super(AssignmentNode, self).__init__()
        self._lvalue = lvalue
        self._expression = expression

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de asignación tiene una expresion (lvalue) de acceso a una
        variable, un elemento de un C{array} o un campo de un C{record} y un 
        valor que se le asignará a este acceso.
        
        En la comprobación semántica de este nodo del árbol se comprueban 
        semánticamente tanto el lvalue como la expresión, luego se comprueba
        que el lvalue como la expresión retornen valor y que el tipo de retorno
        de ambos sea el mismo. Además es necesario comprobar que el lvalue no 
        es de solo lectura, pues en condiciones del lenguaje no es posible 
        modificar el valor de una variable. Se reportarán errores si se encuentran
        errores durante la comprobación semántica del lvalue o de la expresión,
        si alguno de estos no retornan tipo, si los tipos no son iguales. 
        """
        self._scope = scope
        
        self.lvalue.check_semantics(self.scope, errors)
        
        self.expression.check_semantics(self.scope, errors)
        
        if self.lvalue.read_only:
            message = 'Invalid use of assignment, read only field at line {line}'
            errors.append(message.format(line=self.line_number))
        elif not self.lvalue.has_return_value():
            message = 'Invalid use of assignment, non typed field at line {line}'
            errors.append(message.format(line=self.line_number))
        elif not self.expression.has_return_value():
            message = 'Invalid use of assignment, non typed expression at line {line}'
            errors.append(message.format(line=self.line_number))
        elif self.lvalue.return_type != self.expression.return_type:
            message = 'Incompatibles types of assigment at line {line}'
            errors.append(message.format(line=self.line_number))