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
        # Fill the types and alias dictionaries from the declaration lists.
        for declaration_node in self._declarations:
            try:
                scope.define_type(declaration_node.name, declaration_node.type)
            except ValueError:
                message = 'Trying to redefine the type {name} already ' \
                          'defined in this scope at line {line}'
                errors.append(message.format(name=declaration_node.name,
                                             line=declaration_node.line_number))
                return definitions
            definitions.add(declaration_node.name)
        # The resolution of the aliases takes place in the semantic 
        # check of the alias declaration node. 
        
        return definitions
    
    def check_aliases_semantics(self, scope, errors):
        """
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        Realiza la comprobación semántica de los alias definidos en este grupo.          
        
        Se reportarán errores si se producen errores en la comprobación 
        semántica de alguna de las declaraciones de alias contenidas en 
        este grupo.
        """
        self._scope  = scope
        errors_before = len(errors)
        for declaration in self.declarations:
            if isinstance(declaration, AliasTypeDeclarationNode):
                self.scope.current_member = declaration.name
                declaration.check_semantics(self.scope, errors)
            if errors_before != len(errors):
                return
        self.scope.current_member = None

    def check_semantics(self, scope, errors):
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
        """
        self._scope  = scope
        errors_before = len(errors)
        for declaration in self.declarations:
            if not isinstance(declaration, AliasTypeDeclarationNode):
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
        raise NotImplementedError()
