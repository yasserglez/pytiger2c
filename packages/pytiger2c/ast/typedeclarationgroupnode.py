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
        self._types = {}
        self._alias = {}

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
        definidos mutuamente recursivos deben estar definidos en el mismo grupo de 
        declaraciones de tipos. De modo que no es valido declarar tipos mutuamente 
        recursivos con una declaración de variable o función entre estos.
        
        En la comprobación semántica de este nodo del árbol de sintáxis abstracta
        se realiza una primera pasada por los tipos que son declarados en este grupo
        recolectando sus nombres y los tipos a los que hace referencia. 
        
        Se comprueba luego durante una segunda pasada que todos los tipos referenciados
        estén definidos en este ámbito y se terminan de definir las instancias de
        C{TigerType} que van a representar a cada uno de estos tipos.
        
        Se reportarán errores si se referencia a un tipo que no se encuentra definido
        en el ámbito actual o si se detecta que en la definición de algún tipo se 
        oculta la definición de otro tipo con igual nombre y que es usado por algún
        otro grupo de declaraciones en el mismo ámbito local, pues en ambos casos 
        estaríamos ante una definición de tipos dependientes sin que los tipos de los
        que se depende se encuentren en su mismo grupo.
        """
        self._scope  = scope
        local_used = []
        
        # Fill the types and alias dicts from the declarations lists
        for declaration_node in self._declarations:
            name = declaration_node.name
            if name in used_types:
                message = 'Invalid type name {type_name} at line {line}, used before redefine it'
                errors.append(message.format(type_name = name, line=declaration_node.line_number))
            if name in self._alias or name in self._types:
                    message = 'Type {type_name} already defined in the local scope'
                    errors.append(message.format(type_name = name))    
            if isinstance(declaration_node, AliasTypeDeclarationNode):
                self._alias[name] = declaration_node.alias_typename
            else:
                declaration_node._scope = self.scope
                self._types[name] = declaration_node.type
        
        # Resolve the alias type. From now on, the alias is as any type.
        for alias_name in self._alias.keys():
            if alias_name in self._alias:
                try:
                    self._resolve_alias(alias_name, [])
                except ValueError:
                    message = 'Invalid alias declaration of {name}, mutually recursive'
                    errors.append(message.format(name = alias_name))
                except KeyError:
                    message = 'Undefined type needed to declare alias {name}'
                    errors.append(message.format(name = alias_name))        
        
        for type_name, tiger_type in self._types.items():
            # If the tiger type is not defined, the we define it.
            if not tiger_type.defined:
                fields_typenames = tiger_type.fields_typenames
                fields_types = []
                for field_typename in fields_typenames:
                    field = None
                    if field_typename in self._types:
                        field = self._types[field_typename]
                    else:
                        try:
                            field = self.scope.get_type_definition(field_typename)
                        except KeyError:
                            message = 'Undefined type {field_typename} in declaration of {type_name}'
                            errors.append(message.format(field_typename = field_typename, 
                                                         type_name = type_name))
                    fields_types.append(field)
                    local_used.append(field_typename)
                tiger_type.fields_types = fields_types
                tiger_type.defined = True
            # Once we fully define the type, let's define it into the scope.
            try:
                self.scope.define_type(type_name, tiger_type)
                local_used.append(type_name)
            except ValueError:
                message = 'Type {type_name} already defined in the local scope'
                errors.append(message.format(type_name = type_name))
        
        used_types.extend(local_used)


    def _resolve_alias(self, alias_name, backward_reference_names):
        """
        Método encargado de definir los problemas relativos a las definiciones
        mutuamente recursivas de C{alias}. Durante la ejecución de este método
        si es necesario resolver otro C{alias} de modo recursivo, entonces este
        método añadirá al dicionario C{self._types} la definición de esta.
        
        @type alias_name: C{str}
        @param alias_name: Nombre del C{alias} que se pretende resolver.
        
        @type backward_reference_names: C{list}
        @param backward_reference_names: Lista de los nombres de C{alias} que 
            dependen de el C{alias} que queremos resolver, de modo que no puede
            tener una referencia a ninguno de estos como definición.
            
        @rtype: C{TigerType]}
        @return: Tipo correspondiente al nombre del alias que se quiere resolver.
        
        @raise ValueError: Se lanza una excepción C{ValueError} si la definición 
            del C{alias} está en un ciclo de declaraciones de C{alias}.
            
        @raise KeyError: Se lanza una excepción C{KeyError} si no se encuentra el
            tipo al que hace referencia el C{alias}.
        """
        alias_type_name = self._alias[alias_name]
        tiger_type = None
        if alias_type_name in self._alias.keys():
            # The alias name must not be an backward_referenced alias
            if alias_type_name in backward_reference_names:
                raise ValueError('Infinite recursive alias definition of {name}'.format(name = alias_name))
            else:
                backward_reference_names.append(alias_name)
                tiger_type = self._resolve_alias(alias_type_name, backward_reference_names)
        elif alias_type_name in self._types.keys():
            tiger_type = self._types[alias_type_name]
        else:
            tiger_type = self.scope.get_type_definition(alias_type_name)
        
        del self._alias[alias_name]
        self._types[alias_name] = tiger_type
        return tiger_type      