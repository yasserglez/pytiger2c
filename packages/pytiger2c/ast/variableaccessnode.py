# -*- coding: utf-8 -*-

"""
Clase C{VariableAccessNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.accessnode import AccessNode


class VariableAccessNode(AccessNode):
    """
    Clase C{VariableAccessNode} del árbol de sintáxis abstracta.
    
    Representa la estructura de acceso a variable del lenguaje Tiger. La 
    estructura de acceso a variable del leguaje Tiger permite obtener el valor
    de una variable y asignare un nuevo valor a esta. Esta estructura recibe
    el nombre de la variable que representa.
    """
    
    def _get_name(self):
        """
        Método para obtener el valor de la propiedad C{name}.
        """
        return self._name
    
    name = property(_get_name)
    
    def __init__(self, name):
        """
        Inicializa la clase C{VariableAccessNode}.
        
        @type name: C{str}
        @param name: Nombre de la variable a la que representa.
        """
        super(VariableAccessNode, self).__init__()
        self._name = name
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La estructura de acceso a variable del leguaje Tiger permite obtener el 
        valor de una variable y asignare un nuevo valor a esta. Esta estructura 
        recibe el nombre de la variable que representa.
        
        En la comprobación semántica de este nodo del árbol se verifica que la
        variable esté definida en el ámbito que ocurre su acceso. Se reportarán
        errores si la variable no está definida en el ámbito local.
        
        En el proceso de comprobación semántica toma valor las propiedades
        C{return_type} y C{read_only} 
        """
        self._scope = scope
        try:
            definition = self.scope.get_variable_definition(self.name)
            self._return_type, self._read_only = definition.type, definition.read_only 
        except ValueError:
            message = 'The name {name} used at line {line} is not a variable'
            errors.append(message.format(name = self.name, line=self.line_number))
        except KeyError:
            message = 'Variable {name} at line {line} is not a defined'
            errors.append(message.format(name = self.name, line=self.line_number))

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
        return me
