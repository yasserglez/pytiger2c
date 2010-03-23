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
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        @rtype: C{set}
        @return: Conjunto con los nombres de las funciones que se definen en 
            este grupo.
        
        Realiza la definición en el ámbito dado de las funciones definidos en 
        este grupo de declaraciones. 
        
        Se reportarán errores si no puede ser definida una función.        
        """
        result = set()
        for declaration_node in self._declarations:
            name = declaration_node.name
            try:
                scope.define_function(name, declaration_node.type)
            except ValueError:
                message = 'Function or variable with name {type_name}'\
                          ' already defined in the local scope'
                errors.append(message.format(type_name = name))
            result.add(name)
        
        return result

    def check_semantics(self, scope, errors, used_types = None):
        """
        @type used_types: C{list}
        @param used_types: Lista de los nombres de los tipos usados en
            el ámbito local.
        
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
        """
        self._scope  = scope
        for declaration in self.declarations:
            declaration.check_semantics(self.scope, errors)
