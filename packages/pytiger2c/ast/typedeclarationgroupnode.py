# -*- coding: utf-8 -*-

"""
Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.declarationgroupnode import DeclarationGroupNode
from pytiger2c.ast.aliastypedeclarationnode import AliasTypeDeclarationNode


class TypeDeclarationGroupNode(DeclarationGroupNode):
    """
    Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
    
    Representa un grupo de declaraciones de tipos del lenguaje Tiger.
    
    Un grupo de declaraciones de tipos del lenguaje Tiger se forma por
    declaraciones de tipos que aparecen uno a continuación de otros. Los 
    tipos mutuamente recursivos deben estar definidos en un mismo grupo de 
    declaraciones de tipos, de modo que no es válido declarar tipos mutuamente 
    recursivos con una declaración de variable o función entre ellos ya 
    que conduce a situaciones ambiguas.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{TypeDeclarationGroupNode}.
        """
        super(TypeDeclarationGroupNode, self).__init__()
        
    def collect_definitions(self, scope, errors):
        """        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.
        
        Realiza la definición en el ámbito dado de los tipos definidos en este
        grupo de declaraciones. En el caso de los alias, se resuelve y se define
        el tipo concreto al que referencia.
        
        Se reportarán errores si se referencia a un tipo que no se encuentra 
        definido en el ámbito actual o si se declaran alias mutuamente 
        referenciados, en cuyo caso se forma un ciclo de definiciones.
        
        @rtype: C{set}
        @return: Conjunto con los nombres de los tipos definidos en este grupo.                
        """
        definitions = set()
        alias_dict = {}
        # Fill the types and alias dictionaries from the declaration lists.
        for declaration_node in self._declarations:
            if isinstance(declaration_node, AliasTypeDeclarationNode):
                if declaration_node.name in alias_dict:
                    message = 'Trying to redefine the type {name} already ' \
                              'defined in this scope at line {line}'
                    errors.append(message.format(name=declaration_node.name,
                                                 line=declaration_node.line_number))
                    return definitions
                else:                  
                    alias_dict[declaration_node.name] = declaration_node
            else:
                try:
                    scope.define_type(declaration_node.name, declaration_node.type)
                except ValueError:
                    message = 'Trying to redefine the type {name} already ' \
                              'defined in this scope at line {line}'
                    errors.append(message.format(name=declaration_node.name,
                                                 line=declaration_node.line_number))
                    return definitions
            definitions.add(declaration_node.name)
        
        # Resolve the alias types. From now on, aliases will be direct
        # references to the real types.
        for alias_name in alias_dict.keys():
            alias_errors = []
            if alias_name in alias_dict:
                self._resolve_alias(alias_name, scope, alias_dict, set(), alias_errors)
            if alias_errors:
                errors.extend(alias_errors)
                return definitions
        return definitions

    def check_semantics(self, scope, errors, local_types=None):
        """
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Un grupo de declaraciones de tipos del lenguaje Tiger se forma por
        declaraciones de tipos que aparecen uno a continuación de otro. Tipos 
        definidos mutuamente recursivos deben estar definidos en el mismo grupo 
        de declaraciones de tipos. Por tanto, no es valido declarar tipos
        mutuamente recursivos con una declaración de variable o función 
        entre estos.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta 
        se comprueban semánticamente todas la declaraciones contenidas en este.
        
        Se reportarán errores si se producen errores en la comprobación 
        semántica de alguna de las declaraciones contenidas en este grupo.
        
        @type local_types: C{set}
        @param local_types: Conjunto con los nombres de los tipos usados en
            el ámbito local creado por la estructura C{let} del lenguaje.
            Es necesario conocer los tipos declarados en otro grupos de 
            declaraciones de tipos dentro del mismo bloque de declaraciones
            del C{let} para poder reportar como un error semántico la definición
            de un tipo en función de otro tipo que está declarado con igual
            nombre en el ámbito local y en un ámbito superior.
        """
        self._scope  = scope
        errors_before = len(errors)
        for declaration in self.declarations:
            self.scope.current_member = declaration.name
            declaration.check_semantics(self.scope, errors)
            if errors_before != len(errors):
                return
        self.scope.current_member = None

    def _resolve_alias(self, alias_name, scope, alias_dict, referenced_aliases, errors):
        """
        Método encargado de definir los problemas relativos a las definiciones
        mutuamente recursivas de alias. Durante la ejecución de este método
        si es necesario resolver otro alias de modo recursivo, entonces este
        método añadirá al dicionario C{self._types} la definición de esta.
        
        @type alias_name: C{str}
        @param alias_name: Nombre del C{alias} que se pretende resolver.
        
        @type scope: C{Scope}
        @param scope: Ámbito en el que se quiere definir este alias.
        
        @type alias_dict: C{dict}
        @param alias_dict: Diccionario con los nodos del árbol de sintáxis 
            abstracta correspondientes a cada declaración de alias.
        
        @type referenced_aliases: C{set}
        @param referenced_aliases: Conjunto de los nombres de los alias que 
            dependen del alias que se pretende resolver, de modo que no
            se puede encontrar una referencia a ninguno de estos como
            parte de la definición del alias porque se crearía un ciclo. 
            
        @type errors: C{list}
        @param errors: Lista para añadir los errores que ocurran durante
            la resolución de los alias.
            
        @rtype: C{TigerType}
        @return: Tipo correspondiente al nombre del alias que se 
            pretende resolver.
        """
        declaration_node = alias_dict[alias_name]
        alias_typename = declaration_node.alias_typename
        tiger_type = None
        if alias_typename in alias_dict.keys():
            # The alias name must not be an backward_referenced alias.
            if alias_typename in referenced_aliases:
                message = 'Infinite recursive alias definition of {name} at line {line}'
                errors.append(message.format(name=alias_name, 
                                             line=declaration_node.line_number))
                return tiger_type 
            else:
                referenced_aliases.add(alias_name)
                tiger_type = self._resolve_alias(alias_typename, scope, alias_dict, 
                                                 referenced_aliases, errors)
        else:
            try:
                tiger_type = scope.get_type_definition(alias_typename)
            except KeyError:
                message = 'Undefined type {type} in declaration ' \
                          'of alias {name} at line {line}'
                errors.append(message.format(type=alias_typename, name=alias_name,
                                             line=declaration_node.line_number))
                return tiger_type
                
        del alias_dict[alias_name]
        try:
            scope.define_type(alias_name, tiger_type)
        except ValueError:
            message = 'Trying to redefine the type {name} already ' \
                      'defined in this scope at line {line}'
            errors.append(message.format(name=alias_name, 
                                         line=declaration_node.line_number))
        return tiger_type
