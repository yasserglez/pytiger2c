# -*- coding: utf-8 -*-

"""
Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.ast.aliastypedeclarationnode import AliasTypeDeclarationNode


class TypeDeclarationGroupNode(NonValuedExpressionNode):
    """
    Clase C{TypeDeclarationGroupNode} del árbol de sintáxis abstracta.
    
    Representa un grupo de declaraciones de tipos del lenguaje Tiger.
    
    Un grupo de declaraciones de tipos del lenguaje Tiger se forma por
    declaraciones de tipos que aparecen uno a continuación de otros.Tipos 
    definidos mutuamente recursivos deben estar definidos en el mismo grupo de 
    declaraciones de tipos. De modo que no es valido declarar tipos mutuamente 
    recursivos con una declaración de variable o función entre estos. 
    """
    def _get_declarations(self):
        """
        Método para obtener el valor de la propiedad C{declarations}.
        """
        return self._declarations
    
    declarations = property(_get_declarations)
    
    def __init__(self):
        """
        Inicializa la clase C{TypeDeclarationGroupNode}.
        """
        super(TypeDeclarationGroupNode, self).__init__()
        self._declarations = []
        
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


    def _resolve_alias(self, alias_name, scope, alias_dict, 
                       backward_reference_names, errors):
        """
        Método encargado de definir los problemas relativos a las definiciones
        mutuamente recursivas de C{alias}. Durante la ejecución de este método
        si es necesario resolver otro C{alias} de modo recursivo, entonces este
        método añadirá al dicionario C{self._types} la definición de esta.
        
        @type alias_name: C{str}
        @param alias_name: Nombre del C{alias} que se pretende resolver.
        
        @type scope: C{Scope}
        @param scope: Ámbito en el que se quiere definir este alias.
        
        @type alias_dict: C{dict}
        @param alias_dict: Diccionario con los nombres de los alias y los tipos
            referenciados.
        
        @type backward_reference_names: C{list}
        @param backward_reference_names: Lista de los nombres de C{alias} que 
            dependen de el C{alias} que queremos resolver, de modo que no puede
            tener una referencia a ninguno de estos como definición.
            
        @type errors: C{list}
        @param errors: Lista para añadir los errores que ocurran durante la 
            resolución del tipo del C{alias}
            
        @rtype: C{TigerType]}
        @return: Tipo correspondiente al nombre del alias que se quiere resolver.
        """
        alias_type_name = alias_dict[alias_name]
        tiger_type = None
        if alias_type_name in alias_dict.keys():
            # The alias name must not be an backward_referenced alias
            if alias_type_name in backward_reference_names:
                message = 'Infinite recursive alias definition of {name}'
                errors.append(message.format(name = alias_name)) 
            else:
                backward_reference_names.append(alias_name)
                tiger_type = self._resolve_alias(alias_type_name, scope, 
                                                 alias_dict, 
                                                 backward_reference_names,
                                                 errors)
        else:
            try:
                tiger_type = scope.get_type_definition(alias_type_name)
            except KeyError:
                message = 'Undefined type {type} in declaration of alias'\
                          ' {name}'
                errors.append(message.format(type = alias_type_name,
                                             name = alias_name, 
                                             line = self.line_number))
                
        del alias_dict[alias_name]
        try:
            scope.define_type(alias_name, tiger_type)
        except ValueError:
            message = 'Invalid type name {name} already used in this scope'
            errors.append(message.format(name = alias_name, 
                                         line = self._line_number))
        return tiger_type      