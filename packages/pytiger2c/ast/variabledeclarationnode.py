# -*- coding: utf-8 -*-

"""
Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationnode import DeclarationNode
from pytiger2c.types.integertype import IntegerType
from pytiger2c.types.stringtype import StringType
from pytiger2c.types.recordtype import RecordType
from pytiger2c.types.arraytype import ArrayType


class VariableDeclarationNode(DeclarationNode):
    """
    Clase C{VariableDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}
        """
        return self._name
    
    name = property(_get_name)
    
    def _get_value(self):
        """
        Método para obtener el valor de la propiedad C{value}
        """
        return self._value
    
    value = property(_get_value)
    
    def _get_type(self):
        """
        Método para obtener el valor de la propiedad C{type}
        """
        return self._type.type
    
    type = property(_get_type)
    
    def __init__(self, name, value):
        """
        Inicializa la clase C{VariableDeclarationNode}.
        
        @type name: C{str}
        @param name: Nombre de la variable.
        
        @type value: C{LanguageNode}
        @param value: C{LanguageNode} correspondiente al valor que se asigna 
            a la variable.
        """
        super(VariableDeclarationNode, self).__init__()
        self._name = name
        self._value = value
        self._type = None
    
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        self.scope.generate_code(generator)
        var_code = self.scope.get_variable_code(self.name)
        # Give a default value to the variables. This should be done before generating
        # code for the value of the variable because the value could be a function
        # call that returns the value of the variable being defined.
        if isinstance(self._type.type, IntegerType):
            generator.add_statement('{var} = 0;'.format(var=var_code))
        elif isinstance(self._type.type, (StringType, ArrayType)):
            stmt = '{var} = pytiger2c_malloc(sizeof({type}));'
            stmt = stmt.format(var=var_code, type=self._type.type.code_type[:-1])
            generator.add_statement(stmt)
            stmt = '{var}->data = NULL;'.format(var=var_code)
            generator.add_statement(stmt)
            stmt = '{var}->length = 0;'.format(var=var_code)
            generator.add_statement(stmt)
        elif isinstance(self._type.type, RecordType):
            generator.add_statement('{0} = NULL;'.format(var_code))
        self.value.generate_code(generator)
        stmt = '{var} = {value};'.format(var=var_code, value=self.value.code_name)
        generator.add_statement(stmt)
