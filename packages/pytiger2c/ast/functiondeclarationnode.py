# -*- coding: utf-8 -*-

"""
Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode
from pytiger2c.scope import Scope


class FunctionDeclarationNode(CallableDeclarationNode):
    """
    Clase C{FunctionDeclarationNode} del árbol de sintáxis abstracta.
    
    Este nodo representa la declaración de una función en el lenguaje
    Tiger. Una función se diferencia de un procedimiento en que la
    primera siempre tiene un valor de retorno.
    """
    
    def _get_return_typename(self):
        """
        Método para obtener el valor de la propiedad C{return_typename}.
        """
        return self._return_typename
        
    return_typename = property(_get_return_typename)    
       
    def __init__(self, name, parameters_names, parameters_typenames, body, return_typename):
        """
        Inicializa la clase C{FunctionDeclarationNode}.
        
        Para obtener información acerca de los parámetros recibidos por este 
        método consulte la documentación del método C{__init__} en la clase 
        C{CallableDeclarationNode}.
        
        @type return_typename: C{str}
        @param return_typename: Cadena de caracteres correspondiente al nombre
            del tipo del valor de retorno de la función.
        """
        super(FunctionDeclarationNode, self).__init__(name, parameters_names, 
                                                      parameters_typenames, body)
        self._return_typename = return_typename
        
    def check_header_semantics(self, scope, errors):
        """
        Este método realiza la comprobación semántica de la cabecera específica
        para la declaración de funciones. Para más información consulte la
        documentación método C{check_header_semantics} en la clase 
        C{CallableDeclarationNode}.  
        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.        
        """
        super(FunctionDeclarationNode, self).check_header_semantics(scope, errors)
        try:
            self.type.return_type = scope.get_type_definition(self._return_typename)
            self.type.defined = True
        except KeyError:
            message = 'Undefined return type {type} of the ' \
                      'function {name} defined at line {line}'
            message = message.format(name=self.name, type=self.return_typename, 
                                     line=self.line_number)
            errors.append(message)

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La comprobación semántica de este nodo del árbol de sintáxis abstracta 
        está dividida en dos partes: la comprobación semántica de la cabecera a 
        través del método C{check_header_semantics} y la comprobación semántica 
        del cuerpo a través del método C{check_semantics}.
        
        En este método se crea un nuevo ámbito que tendrá como padre el ámbito en
        el que se está definiendo la función y contendrá las definiciones de las
        variables correspondientes a los parámetros recibidos por el procedimiento.
        Luego, se comprueba semánticamente el cuerpo de la función, el cual 
        debe tener valor de retorno.
        """
        # Create and populate the scope with the parameters.
        self._scope = Scope(scope)
        for parameter_name, parameter_type in zip(self.parameters_names, 
                                                  self.type.parameters_types):
            self.scope.define_variable(parameter_name, parameter_type)
        
        # Check semantics of the body.        
        self.body.check_semantics(self.scope, errors)
        if not self.body.has_return_value():
            message = 'The body of the function {name} defined at ' \
                      'line {line} does not return a value'
            errors.append(message.format(name=self.name, line=self.line_number))
        else:
            if self.type.return_type != self.body.return_type:
                message = 'The return type of the body of the function {name} defined ' \
                          'at line {line} does not match the declared type {type}'
                message = message.format(name=self.name,
                                         type=self.return_typename,
                                         line=self.line_number)
                errors.append(message)
