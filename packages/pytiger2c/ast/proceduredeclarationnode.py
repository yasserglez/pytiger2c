# -*- coding: utf-8 -*-

"""
Clase C{ProcedureDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode
from pytiger2c.scope import Scope


class ProcedureDeclarationNode(CallableDeclarationNode):
    """
    Clase C{ProcedureDeclarationNode} del árbol de sintáxis abstracta.
    
    Este nodo representa la declaración de un procedimiento en en lenguaje
    Tiger. Un procedimiento es una función que no tiene valor de retorno
    y que sólo se llamará por sus efectos colaterales.
    """
    
    def __init__(self, name, parameters_names, parameters_typenames, body):
        """
        Inicializa la clase C{ProcedureDeclarationNode}.
        
        Para obtener información acerca de los parámetros recibidos por este 
        método consulte la documentación del método C{__init__} en la clase 
        C{CallableDeclarationNode}.        
        """
        super(ProcedureDeclarationNode, self).__init__(name, parameters_names, 
                                                       parameters_typenames, body)
        
    def check_header_semantics(self, scope, errors):
        """
        Este método realiza la comprobación semántica de la cabecera específica
        para la declaración de procedimientos. Para más información consulte la
        documentación método C{check_header_semantics} en la clase 
        C{CallableDeclarationNode}.  
        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.        
        """
        super(ProcedureDeclarationNode, self).check_header_semantics(scope, errors)
        self.type.defined = True
        
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
        Luego, se comprueba semánticamente el cuerpo del procedimiento, el cual no 
        debe tener valor de retorno.
        """
        errors_before = len(errors)
        
        # Create and populate the scope with the parameters.
        self._scope = Scope(scope)
        for parameter_name, parameter_type in zip(self.parameters_names, 
                                                  self.type.parameters_types):
            self.scope.define_variable(parameter_name, parameter_type)
            
        # Check semantics of the body.        
        self.body.check_semantics(self.scope, errors)
        
        if errors_before != len(errors):
            return
        
        if self.body.has_return_value():
            message = 'The body of the procedure {name} defined ' \
                      'at line {line} returns value'
            errors.append(message.format(name=self.name, line=self.line_number))
