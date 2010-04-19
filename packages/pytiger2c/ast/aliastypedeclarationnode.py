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
        
        Este método realiza la comprobación semántica de la definición de
        un alias. Primeramente, el método obtendrá del ámbito la instancia
        correspondiente al tipo que referencia el alias. Si este tipo
        no es un alias, actualizará la definición del alias en el ámbito
        padre del ámbito falso recibido como argumento para referenciar 
        a la instancia del tipo real. Si este alias se define en función de
        otro se resolverá este en función de un tipo real y se procederá
        como se describió anteriormente.
        
        Durante este proceso de comprobación semántica se detectará
        si se forma un ciclo durante la definición de una secuencia de
        alias, reportándose este hecho como un error semántico. Igualmente
        se reportará un error si un alias se define en función de un
        tipo que no se encuentra definido anteriormente.
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
        
        # Let's resolve the aliases until a real type is found.
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
        alias_typename = generator.add_node(self.alias_typename)
        generator.add_edge(me, name)
        generator.add_edge(me, alias_typename)
        return me

    def generate_code(self, generator):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.

        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_code}
        de la clase C{LanguageNode}.
        """