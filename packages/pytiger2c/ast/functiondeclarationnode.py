# -*- coding: utf-8 -*-

"""
Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode
from pytiger2c.types.functiontype import FunctionType
from pytiger2c.scope import Scope


class FunctionDeclarationNode(CallableDeclarationNode):
    """
    Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
    
    Este nodo representa la declaración de una función en el lenguaje
    Tiger. Una función se diferencia de un procedimiento en que la
    primera siempre tiene un valor de retorno.
    """
    
    def _get_return_type(self):
        """
        Método para obtener el valor de la propiedad C{return_type}.
        """
        return self._return_type
        
    return_type = property(_get_return_type)      
    
    def __init__(self, name, parameters_names, parameters_typenames, body, return_type):
        """
        Inicializa la clase C{FunctionDeclarationNode}.
        
        Para obtener información acerca de los parámetros recibidos por este 
        método consulte la documentación del método C{__init__} en la clase 
        C{CallableDeclarationNode}.
        
        @type return_type: C{str}
        @param return_type: Cadena de caracteres correspondiente al nombre
            del tipo del valor de retorno de la función.
        """
        super(FunctionDeclarationNode, self).__init__(name, parameters_names, 
                                                      parameters_typenames, body)
        self._type = FunctionType(None, [], parameters_names)
        self._return_type = return_type

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxix abstracta
        se comprueba que los tipos declarados para los parámetros de la función
        esten definidos en el ámbito donde se está definiendo la función o en 
        algún ámbito superior y que los parámetros tengan nombres diferentes.
        Además, se crea un nuevo ámbito que tendrá como padre el ámbito en
        el que se está definiendo la función y contendrá las definiciones de las
        variables correspondientes a los parámetros recibidos por el procedimiento.
        
        Luego, se comprueba semánticamente el cuerpo de la función, el cual 
        debe tener valor de retorno y se añade la instancia de C{FunctionType}
        correspondiente a la función al ámbito, si no existe otro miembro
        miembro del ambiente con ese nombre definido anteriormente.
        """
        self._scope = Scope(scope)
        parameters_errors = []
        self._check_parameters_semantics(parameters_errors)
        if parameters_errors:
            errors.extend(parameters_errors)
        else:
            try:
                self._return_type = scope.get_type_definition(self._return_type)
            except KeyError:
                message = 'Undefined return type {type} of the ' \
                          'function {name} defined at line {line}'
                message = message.format(name=self.name,
                                         type=self.return_type, 
                                         line=self.line_number)
                errors.append(message)
            self.body.check_semantics(self.scope, errors)
            if not self.body.has_return_value():
                message = 'The body of the function {name} defined at ' \
                          'line {line} does not return a value'
                errors.append(message.format(name=self.name, line=self.line_number))
            else:
                if self.return_type != self.body.return_type:
                    message = 'The return type of the body of the function {name} defined ' \
                              'at line {line} does not match the declared type {type}'
                    message = message.format(name=self.name,
                                             type=self.return_type,
                                             line=self.line_number)
                    errors.append(message)   
                         
            self.type.parameters_types = self.parameters_types
            self.type.return_type = self.return_type
            self.defined = True
