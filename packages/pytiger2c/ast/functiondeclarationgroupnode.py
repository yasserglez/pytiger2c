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
        @return: Conjunto con los nombres de los tipos que se definen en este
            grupo.
        
        Realiza la definición en el ámbito dado de los tipos definidos en este
        grupo de declaraciones. En el caso de los alias, se resuelve y se define
        el tipo concreto al que referencia.
        
        Se reportarán errores si se referencia a un tipo que no se encuentra 
        definido en el ámbito actual o si se declaran alias mutuamente 
        referenciadas, en cuyo caso se forma un ciclo de definiciones.        
        """
        result = set()
        alias = {}
        # Fill the types and alias dicts from the declarations lists
        for declaration_node in self._declarations:
            name = declaration_node.name
            if isinstance(declaration_node, AliasTypeDeclarationNode):
                if name in alias:
                    message = 'Type {type_name} already defined in the '\
                              'local scope'
                    errors.append(message.format(type_name = name))
                else:                  
                    alias[name] = declaration_node.alias_typename
            else:
                try:
                    scope.define_type(name, declaration_node.type)
                except ValueError:
                    message = 'Type {type_name} already defined in the local scope'
                    errors.append(message.format(type_name = name))
            result.add(name)
        
        # Resolve the alias type. From now on, the alias is as any type.
        for alias_name in alias.keys():
            if alias_name in alias:
                self._resolve_alias(alias_name, scope, alias, [], errors)
        
        return result
        

    def check_semantics(self, scope, errors, used_types = None):
        """
        @type used_types: C{list}
        @param used_types: Lista de los nombres de los tipos usados en
            el ámbito local.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Un grupo de declaraciones de tipos del lenguaje Tiger se forma por
        declaraciones de tipos que aparecen uno a continuación de otros.Tipos 
        definidos mutuamente recursivos deben estar definidos en el mismo grupo 
        de declaraciones de tipos. De modo que no es valido declarar tipos 
        mutuamente recursivos con una declaración de variable o función entre 
        estos.
        
        En la comprobación de este nodo del árbol de sintáxis abstracta se 
        comprueban semánticamente todas la declaraciones contenidas en este.
        
        Se reportarán errores si se producen errores en la comprobación 
        semántica de alguna de las declaraciones contenidas en este grupo.
        """
        self._scope  = scope
        for declaration in self.declarations:
            declaration.check_semantics(self.scope, errors)
