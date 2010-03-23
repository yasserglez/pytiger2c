# -*- coding: utf-8 -*-

"""
Clase C{ArrayAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode
from pytiger2c.types.arraytype import ArrayType
from pytiger2c.types.integertype import IntegerType


class ArrayAccessNode(AccessNode):
    """
    Clase C{ArrayAccessNode} del árbol de sintáxis abstracta.
    
    Representa el acceso a un array del lenguaje Tiger. El acceso a un
    array del lenguaje Tiger permite obtener el valor del elemento
    que se encuentra en una posición determinada o asignarle un nuevo valor a 
    este array en la misma posición. Esta estructura recibe la expresión que 
    representa el acceso al array y la expresión correspondiente a la 
    posición que se quiere acceder. 
    """
    
    def _get_array(self):
        """
        Método para obtener el valor de la propiedad array.
        """
        return self._array_expression
    
    array = property(_get_array)
    
    def _get_position(self):
        """
        Método para obtener el valor de la propiedad C{position}.
        """
        return self._position
    
    position = property(_get_position)
    
    def __init__(self, array_expression, position):
        """
        Inicializa la clase C{ArrayAccessNode}.
        
        @type array_expression: C{LanguageNode}
        @param array_expression: Expresión correspondiente al array que se 
            quiere acceder.
            
        @type position: C{LanguageNode}
        @param position: Expresión correspondiente a la posición del array
            que se quiere acceder.
        """
        super(ArrayAccessNode, self).__init__()
        self._array_expression = array_expression
        self._position = position

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de acceso a array del lenguaje Tiger permite obtener
        el valor de un array en una posición determinada o asignarle un nuevo 
        valor a este array en la misma posición. Esta estructura recibe la 
        expresión que representa el acceso a la instancia de array y la 
        expresión correspondiente a la posición que se quiere acceder. 
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se verifica que la expresión que se correspondiente al array retorne
        valor y que este sea del tipo array, luego se comprueba que la 
        expresión de la posición retorne valor y que este sea de tipo entero. 
        
        En el proceso de comprobación semántica toman valor las propiedades
        C{return_type} y C{read_only} 
        """
        self._scope = scope
        self.array.check_semantics(self.scope, errors)
            
        if self.array.has_return_value():
            array_type = self.array.return_type
            if isinstance(array_type, ArrayType):
                self._return_type = array_type.fields_types[0]
                self._read_only = self.array.read_only
            else:
                self._return_type = None
                message = 'Invalid array access on a non array type at line {line}'
                errors.append(message.format(line=self.line_number))
            self.position.check_semantics(self.scope, errors)
            if not self.position.has_return_value():
                message = 'The expression for the position in the array does ' \
                          'not have a return value at line {line}'
                errors.append(message.format(line=self.line_number))
            elif self.position.return_type != IntegerType():
                message = 'Invalid non integer position for array access at line {line}'
                errors.append(message.format(line=self.line_number))
            
        else:
            message = 'Invalid array access on a non valued expression at line {line}'
            errors.append(message.format(line=self.line_number))
