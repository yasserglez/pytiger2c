# -*- coding: utf-8 -*-

"""
Clase C{FunctionDeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationgroupnode import DeclarationGroupNode


class FunctionDeclarationGroupNode(DeclarationGroupNode):
    """
    Clase C{FunctionDeclarationGroupNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{FunctionDeclarationGroupNode}.
        """
        super(FunctionDeclarationGroupNode, self).__init__()
    
    def collect_definitions(self, scope, errors):
        """        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.
        
        Realiza la comprobación semántica de las cabeceras de las funciones
        definidas en el grupo y además define en el ámbito dado las funciones
        del grupo.
        
        Se reportarán errores si se produce alguno durante la comprobación 
        semántica de las cabeceras de las funciones o si no puede ser
        definida una función.
        
        @rtype: C{set}
        @return: Conjunto con los nombres de las funciones definidas en este grupo.
        """
        definitions = set()
        for declaration_node in self._declarations:
            try:
                declaration_node.check_header_semantics(scope, errors)
                scope.define_function(declaration_node.name, declaration_node.type)
            except ValueError:
                message = 'The name of the function {name} at line {line} ' \
                          'is already defined in this scope'
                errors.append(message.format(name=declaration_node.name,
                                             line=declaration_node.line_number))
                return definitions
            else:
                definitions.add(declaration_node.name)
        return definitions

    def check_semantics(self, scope, errors, used_types = None):
        """
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Un grupo de declaraciones de funciones del lenguaje Tiger se forma por
        declaraciones de funciones que aparecen uno a continuación de otros.
        Funciones mutuamente recursivas deben estar definidas en el mismo grupo 
        de declaraciones de funciones. De modo que no es valido declarar 
        funciones mutuamente recursivos con una declaración de variable o 
        tipo entre estas.
        
        En la comprobación de este nodo del árbol de sintáxis abstracta se 
        comprueban semánticamente todas la declaraciones contenidas en este.
        
        Se reportarán errores si se producen errores en la comprobación 
        semántica de alguna de las declaraciones contenidas en este grupo.
        
        @type used_types: C{list}
        @param used_types: Lista de los nombres de los tipos usados en
            el ámbito local.        
        """
        self._scope  = scope
        errors_before = len(errors)
        for declaration in self.declarations:
            self.scope.current_member = declaration.name
            declaration.check_semantics(self.scope, errors)
            if errors_before != len(errors):
                return
        self.scope.current_member = None
        
    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """
        for declaration in self.declarations:
            declaration.generate_code(generator)
