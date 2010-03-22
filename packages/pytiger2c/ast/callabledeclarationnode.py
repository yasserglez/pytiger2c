# -*- coding: utf-8 -*-

"""
Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode


class CallableDeclarationNode(DeclarationNode):
    """
    Clase C{CallableDeclarationNode} del árbol de sintáxis abstracta.
    
    Clase base de los nodos C{FunctionDeclarationNode} y C{ProcedureDeclarationNode} 
    del árbol de sintáxis abstracta. Esta clase tiene como objetivo factorizar los 
    métodos y propiedades comunes de las clases representando declaraciones de 
    procedimientos y funciones.
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
    
    def _get_parameters_types(self):
        """
        Método para obtener el valor de la propiedad C{parameters_types}.
        """
        return self._parameters_types
    
    parameters_types = property(_get_parameters_types)    
    
    def _get_body(self):
        """
        Método para obtener el valor de la propiedad C{body}.
        """
        return self._body
        
    body = property(_get_body)    

    def __init__(self, name, parameters, body):
        """
        Inicializa la clase C{CallableDeclarationNode}.
        
        @type name: C{str}
        @param name: Nombre del procedimiento o función cuya definición
            es representada por el nodo.
            
        @type parameters: C{list}
        @param parameters: Lista de tuplas conteniendo el nombre y el 
            tipo de los parámetros del procedimiento o función.
            
        @type body: C{LanguageNode}
        @param body: Nodo del árbol de sintáxis abstracta correspondiente
            al cuerpo del procedimiento o función.
        """
        super(CallableDeclarationNode, self).__init__()
        self._name = name
        self._parameters_names, self._parameters_types = zip(*parameters)
        self._body = body

    def _check_parameters_semantics(self, errors):
        """
        Método auxiliar utilizado por los métodos C{check_semantics} de las clases
        C{ProcedureDeclarationNode} y C{FunctionDeclarationNode} para comprobar
        semánticamente los parámetros de la función o procedimiento definido.
        
        Se comprueba que los tipos declarados para los parámetros de la función
        o procedimiento esten definidos en el ámbito donde se está definiendo 
        la función o en algún ambiente superior y que los parámetros tengan 
        nombres diferentes. Los nombres de los tipos de los parámetros se
        sustituyen por las instancias de C{TigerType} correspondientes. Luego, 
        se añaden al ámbito las definiciones de las variables correspondientes 
        a los parámetros recibidos por el procedimiento.  
        
        @type errors: C{list}
        @param errors: Lista donde se deben añadir los mensajes de error que se
            detecten durante la comprobación semántica realizada por este método.
        """
        for i, parameter_name in enumerate(self.parameters_types):
            try:
                tiger_type = self.scope.get_type_definition(parameter_name)
            except KeyError:
                message = 'The type {type} of the parameter #{index} of the ' \
                          'callable {name} defined at line {line} is not defined'
                message = message.format(type=parameter_name, index=i + 1,
                                         name=self.name, line=self.line_number)
                errors.append(message)
            else:
                self._parameters_types[i] = tiger_type
        for parameter_name, parameter_type in zip(self.parameters_names, 
                                                  self.parameters_types):
            try:
                self.scope.define_variable(parameter_name, parameter_type)
            except ValueError:
                message = 'At least two parameters of the callable {name} ' \
                          'defined at line {line} have the same name'
                message = message.format(type=parameter_name, name=self.name, 
                                         line=self.line_number)
