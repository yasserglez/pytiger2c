# -*- coding: utf-8 -*-

"""
Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.arraytype import ArrayType


class ArrayDeclarationNode(TypeDeclarationNode):
    """
    Clase C{ArrayDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de declaración de un tipo array en el lenguaje 
    Tiger. La estructura de declaración de array recibe un nombre que es el 
    que representará a estos array concretos y el nombre del tipo que van a 
    tener los valores.    
    """
    
    def _get_values_typename(self):
        """
        Método para obtener el valor de la propiedad C{values_typename}.
        """
        return self._values_typename
    
    values_typename = property(_get_values_typename)    
    
    def __init__(self, name, values_typename):
        """
        Inicializa la clase C{ArrayDeclarationNode}.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}.
        
        @type values_typename: C{str}
        @param values_typename: Nombre del tipo que tendrán los valores del array.        
        """
        super(ArrayDeclarationNode, self).__init__(name)
        self._values_typename = values_typename
        self._type = ArrayType(self._values_typename) 

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        En la comprobación semántica de este nodo del árbol de sintáxis 
        abstracta se comprueba que el tipo de los valores del array
        se encuentre definido en el ámbito local.
        
        Se reportarán errores semánticos si el tipo de los valores del array
        no se encuentra definido en el ámbito local, o en caso de que esté 
        definido en el ámbito local, pero en otro grupo de declaraciones, en
        cuyo caso se considera una declaración de tipos mutuamente recursivos
        en distintos grupos de declaraciones de tipos.
        
        Durante la comprobación semántica se define totalmente el valor de la
        propiedad C{type}.
        """
        self._scope = scope
        type = None
        type_name = self.type.fields_typenames[0]
        
        try:
            type = self.scope.get_type_definition(type_name)
        except KeyError:
            message = 'Undefined type {type} in the array {name} ' \
                      'declaration at line {line}'
            errors.append(message.format(type=type_name, name=self.name, 
                                         line=self.line_number))

        self.type.fields_types = [type]

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
        values_typename = generator.add_node(self.values_typename)
        generator.add_edge(me, name)
        generator.add_edge(me, values_typename)
        return me
