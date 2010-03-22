# -*- coding: utf-8 -*-

"""
Clase C{ProcedureDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode
from pytiger2c.types.functiontype import FunctionType
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

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxix abstracta
        se comprueba que los tipos declarados para los parámetros del procedimiento
        esten definidos en el ámbito donde se está definiendo la función o en 
        algún ámbito superior y que los parámetros tengan nombres diferentes.
        Además, se crea un nuevo ámbito que tendrá como padre el ámbito en
        el que se está definiendo la función y contendrá las definiciones de las
        variables correspondientes a los parámetros recibidos por el procedimiento.
        
        Luego, se comprueba semánticamente el cuerpo de la función, el cual no 
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
            self.body.check_semantics(self.scope, errors)
            if self.body.has_return_value():
                message = 'The body of the procedure {name} defined ' \
                          'at line {line} returns value'
                errors.append(message.format(name=self.name, line=self.line_number))
            try:
                function_type = FunctionType(None, self.parameters_types)
                scope.define_function(self.name, function_type)
            except ValueError:
                message = 'Procedure {name} defined at line {line} collapses ' \
                          'with a previously defined member of the scope'
                errors.append(message.format(name=self.name, line=self.line_number))
