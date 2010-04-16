# -*- coding: utf-8 -*-

"""
Clase C{FunctionCallNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.niltype import NilType


class FunctionCallNode(ValuedExpressionNode):
    """
    Clase C{FunctionCallNode} del árbol de sintáxis abstracta.
    
    Este nodo representa el llamado a una función o un procedimiento en el
    lenguaje Tiger. La función que se está llamando debe haber sido
    definida anteriormetne o ser una función de la biblioteca standard
    de Tiger. El tipo de retorno de un llamado a una función será 
    el mismo tipo de retorno de las funciones y no tendrá valor de retorno
    en el caso de los procedimientos.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}.
        """
        return self._name
    
    name = property(_get_name)
    
    def _get_parameters(self):
        """
        Método para obtener el valor de la propiedad C{parameters}.
        """
        return self._parameters
    
    parameters = property(_get_parameters)
    
    def __init__(self, name, parameters):
        """
        Inicializa la clase C{FunctionCallNode}.
        
        @type name: C{str}
        @param name: Cadena de caracteres correspondiente al nombre
            de la función que se está llamando.
        
        @type parameters: C{list}
        @param parameters: Lista de expresiones que darán valor a cada
            uno de los parámetros de la función.
        """
        super(FunctionCallNode, self).__init__()
        self._name = name
        self._parameters = parameters

    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.      
        """
        return self._return_type != None

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxix abstracta
        se comprueban semánticamente cada una de las expresiones de la lista de
        expresiones que dan valor a los parámetros de la función o procedimiento.
        Luego, se comprueba que la función o procedimiento que se está llamando
        exista y que el tipo de las expresiones de los parámetros coincida con
        los esperados por la definición de la función. Finalmente se asigna el
        tipo de retorno del nodo al tipo de retorno de la función o no tendrá 
        valor de retorno en el caso de llamados a procedimientos.        
        """
        self._scope = scope
        
        errors_before = len(errors)
        
        for expression in self._parameters:
            expression.check_semantics(self._scope, errors)

        try:
            function_type = self._scope.get_function_definition(self._name)
        except KeyError:
            message = 'Calling an undefined function {name} at line {line}'
            errors.append(message.format(name=self._name, line=self.line_number))
        except ValueError:
            message = 'The name {name} used at line {line} is not a function'
            errors.append(message.format(name=self._name, line=self.line_number))
        else:
            if len(self._parameters) == len(function_type.parameters_types):
                if errors_before == len(errors):
                    collection = zip(function_type.parameters_types, self._parameters)
                    for index, (param_type, param) in enumerate(collection):
                        if not param.has_return_value():
                            message = 'The expression used as argument #{index} ' \
                                      'of the function {name} at line {line} ' \
                                      'does not return a value'
                            message = message.format(name=self._name,
                                                     index=index + 1, 
                                                     line=self.line_number)
                            errors.append(message)
                        elif (param_type != param.return_type and 
                              not (isinstance(param_type, RecordType)
                                   and isinstance(param.return_type, NilType))):
                            message = 'Invalid type of the argument #{index} ' \
                                      'of the function {name} at line {line}'
                            message = message.format(name=self._name,
                                                     index=index + 1, 
                                                     line=self.line_number)
                            errors.append(message)
            else:
                message = 'Calling function {name} with a wrong ' \
                          'number of arguments at line {line}'
                errors.append(message.format(name=self._name, line=self.line_number))
            self._return_type = function_type.return_type                

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        name = generator.add_node(self.name)
        generator.add_edge(me, name)
        for parameter in self.parameters:
            parameter = parameter.generate_dot(generator)
            generator.add_edge(me, parameter)
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
        for parameter in self.parameters:
            parameter.generate_code(generator)
