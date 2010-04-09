# -*- coding: utf-8 -*-

"""
Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.aliastype import AliasType

class AliasTypeDeclarationNode(TypeDeclarationNode):
    """
    Clase C{AliasTypeDeclarationNode} del árbol de sintáxis abstracta.
    
    Representa la declaración de un alias de un tipo del lenguaje Tiger.
    Un alias define un nuevo nombre en el ámbito local para definirse
    a un tipo definido anteriorment en el mismo ámbito o en un ámbito
    superior. 
    """
    
    def _get_alias_typename(self):
        """
        Método para obtener el valor de la propiedad C{alias_typename}.
        """
        return self._alias_typename
    
    alias_typename = property(_get_alias_typename)
    
    def __init__(self, name, alias_typename):
        """
        Inicializa la clase C{AliasTypeDeclarationNode}.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}.         
        
        @type alias_typename: C{str}
        @param alias_typename: Nombre del tipo al que se le define el alias.
        """
        super(AliasTypeDeclarationNode, self).__init__(name)
        self._alias_typename = alias_typename
        self._type = AliasType(alias_typename)

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
	    """
        self._scope = scope
        alias_type = None
        
        erros_before = len(errors)
        try:
            alias_type = self._scope.get_type_definition(self._alias_typename)
        except KeyError:
            message = 'Undefined alias type {alias_type} in the ' \
                      'alias {name} declared at line {line}'
            errors.append(message.format(alias_type=self._alias_typename,
                                         name=self._name, 
                                         line=self.line_number))
        aliases_names = set()
        aliases_names.add(self._name)
        
        # Let's resolve the tiger alias until a real type is found.
        while isinstance(alias_type, AliasType):
            name = alias_type.alias_typename
            if name in aliases_names:
                message = 'Infinite recursive alias definition ' \
                          'of {name} at line {line}'
                errors.append(message.format(name=self._name,
                                             line=self._line_number))
                break
            else:
                try:
                    alias_type = self._scope.get_type_definition(name)
                except KeyError:
                    message = 'Undefined alias_type {alias_type} in ' \
                              'the alias {name} declaration at line {line}'
                    errors.append(message.format(alias_type=name, name=self._name, 
                                                 line=self.line_number))
                    break
                aliases_names.add(name)
        
        if erros_before != len(errors):
            return
        
        # Ugly hack! Modifying dictionary of the parent scope of the fake scope.
        for alias_name in aliases_names:
            self.scope.parent._types[alias_name] = alias_type
