# -*- coding: utf-8 -*-

"""
Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode
from pytiger2c.types.functiontype import FunctionType


class CallableDeclarationNode(DeclarationNode):
    """
    Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
    
    Clase base de los nodos C{FunctionDeclarationNode} y C{ProcedureDeclarationNode} 
    del árbol de sintáxis abstracta. Esta clase tiene como objetivo factorizar los 
    métodos y propiedades comunes de las clases representando declaraciones de 
    procedimientos y funciones.
    
    La comprobación semántica de los nodos del árbol de sintáxis abstracta 
    descendientes de este nodo está dividida en dos partes: la comprobación
    semántica de la cabecera a través del método C{check_header_semantics} y
    la comprobación semántica del cuerpo a través del método C{check_semantics}.
    Para más información consulte la documentación de estos métodos.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}.
        """
        return self._name
        
    name = property(_get_name)
    
    def _get_parameters_names(self):
        """
        Método para obtener el valor de la propiedad C{parameters_names}.
        """
        return self._parameters_names
    
    parameters_names = property(_get_parameters_names) 
    
    def _get_parameters_typenames(self):
        """
        Método para obtener el valor de la propiedad C{parameters_typenames}.
        """
        return self._parameters_typenames
    
    parameters_typenames = property(_get_parameters_typenames)    
    
    def _get_body(self):
        """
        Método para obtener el valor de la propiedad C{body}.
        """
        return self._body
        
    body = property(_get_body)
    
    def _get_type(self):
        """
        Método para obtener el valor de la propiedad C{type}.
        """
        return self._type
    
    type = property(_get_type)

    def __init__(self, name, parameters_names, parameters_typenames, body):
        """
        Inicializa la clase C{CallableDeclarationNode}.
        
        @type name: C{str}
        @param name: Nombre del procedimiento o función cuya definición
            es representada por el nodo.
            
        @type fields_names: C{list}
        @param fields_names: Lista con los nombres de los parámetros de la
            función o procedimiento, por posición.
        
        @type fields_typenames: C{list}
        @param fields_typenames: Lista con los nombres de los tipos de los 
            parámetros de la función o procedimiento, por posición. 
            
        @type body: C{LanguageNode}
        @param body: Nodo del árbol de sintáxis abstracta correspondiente
            al cuerpo del procedimiento o función.
        """
        super(CallableDeclarationNode, self).__init__()
        self._name = name
        self._parameters_names = parameters_names
        self._parameters_typenames = parameters_typenames
        self._body = body
        self._type = FunctionType(None, [], parameters_names)
        
    def check_header_semantics(self, scope, errors):
        """
        Este método realiza la comprobación semántica de la cabecera de la
        comunes a las funciones y procedimientos. Como resultado de esta 
        comprobación se reportará cualquier error relacionados con el nombre 
        de la función o procedimiento, los parámetros, los tipos de los 
        parámetros y además tomará valor la propiedad C{type} que contendrá 
        el tipo de la función o procedimiento que define este nodo.
        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.        
        """
        parameters_types = []
        for i, parameter_name in enumerate(self._parameters_typenames):
            try:
                tiger_type = scope.get_type_definition(parameter_name)
            except KeyError:
                message = 'The type {type} of the parameter #{index} of the ' \
                          'callable {name} defined at line {line} is not defined'
                message = message.format(type=parameter_name, index=i + 1,
                                         name=self.name, line=self.line_number)
                errors.append(message)
            else:
                parameters_types.append(tiger_type)
        if len(self._parameters_names) != len(set(self._parameters_names)):
            message = 'At least two parameters of the callable {name} ' \
                      'defined at line {line} have the same name'
            message = message.format(type=parameter_name, name=self.name, 
                                     line=self.line_number)
            errors.append(message)            
        self.type.parameters_types = parameters_types

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        generator.begin_function(self.type.code_name)
        self.scope.generate_code(generator)
        stmt = '{scope}->parent = {parent};'
        stmt = stmt.format(scope=self.scope.code_name, 
                           parent=self.scope.parent.code_name)
        generator.add_statement(stmt)        
        for index, var_name in enumerate(self.parameters_names):
            parameter_name = generator.get_function_parameter(index)
            var_name = self.scope.get_variable_code(var_name)
            stmt = '{var} = {param};'.format(var=var_name, param=parameter_name)
            generator.add_statement(stmt)
        self.body.generate_code(generator)
        if self.body.has_return_value():
            return_var = generator.define_local(self.body.return_type.code_type)
            stmt = '{return_var} = {body_var};'
            stmt = stmt.format(return_var=return_var, body_var=self.body.code_name)
            generator.add_statement(stmt)
        else:
            return_var = None
        generator.end_function(return_var)
