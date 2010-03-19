# -*- coding: utf-8 -*-

"""
Clase C{LetNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.scope import Scope


class LetNode(ValuedExpressionNode):
    """
    Clase C{LetNode} del árbol de sintáxis abstracta.
    
    TODO
    """
    
    def __init__(self, type_declaration_groups, members_declarations, expr_seq):
        """
        Inicializa la clase C{LetNode}.
        
        TODO
        """
        super(LetNode, self).__init__()
        self._type_declaration_groups = type_declaration_groups
        self._members_declarations = members_declarations
        self._expr_seq = expr_seq

    def check_semantics(self, scope, errors):
        """
        TODO
        
        TODO Mirar si tiene tipo de retorno y demás detalles. 
        """
        self._scope = Scope(scope) 
        used_types = []
        
        for type_declaration_group in self._type_declaration_groups:
            type_declaration_group.check_semantics(self.scope, errors, used_types)
            
        for member_declaration in self._members_declarations:
            member_declaration.check_semantics(self.scope, errors)
            
        self._expr_seq.check_semantics(self.scope, errors)
    
