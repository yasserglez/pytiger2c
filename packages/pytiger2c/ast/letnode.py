# -*- coding: utf-8 -*-

"""
Clase C{LetNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.valuedexpressionnode import ValuedExpressionNode
from pytiger2c.scope import Scope, FakeScope


class LetNode(ValuedExpressionNode):
    """
    Clase C{LetNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{let-in-end} del lenguaje Tiger. La expresión 
    C{let-in-end} recibe una lista de declaraciones que se expresan detrás
    del token C{let} de tal forma que esas declaraciones estarán disponibles
    en el ámbito de ejecución de la secuencia de expresiones que se expresan
    detrás del token C{in}.
    
    La expresión C{let-in-end} retorna valor si la secuencia de expresiones
    retorna valor y su tipo de retorno es el mismo que la secuencia de 
    expresiones.
    """
    
    def __init__(self, type_declaration_groups, function_declaration_groups, 
                 members_declarations, expr_seq):
        """
        Inicializa la clase C{LetNode}.
        
        @type type_declaration_groups: C{list}
        @param type_declaration_groups: Lista de los grupos de las declaraciones
            de tipos, que forman parte de la lista de declaraciones.
            
        @type function_declaration_groups: C{list}
        @param function_declaration_groups: Lista de los grupos de las declaraciones
            de funciones, que forman parte de la lista de declaraciones.
        
        @type members_declarations: C{list}
        @param members_declarations: Lista de las declaraciones de variables 
            que forman parte de la lista de declaraciones.
            
        @type expr_seq: C{ExpressionSequenceNode}
        @param expr_seq: Sequencia de expresiones que forman parte del cuerpo
            de la expresión C{let-in-end}. 
        """
        super(LetNode, self).__init__()
        self._type_declaration_groups = type_declaration_groups
        self._function_declaration_groups = function_declaration_groups
        self._members_declarations = members_declarations
        self._expr_seq = expr_seq

    def has_return_value(self):
        """
        Ver documentación del método C{has_return_value} en C{LanguageNode}.      
        """
        return self._return_type != None 


    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión C{let-in-end} recibe una lista de declaraciones que se 
        expresan detrás del token C{let} de tal forma que esas declaraciones estarán
        disponibles en el ámbito de ejecución de la secuencia de expresiones que se 
        expresan detrás del token C{in}.
        
        La expresión C{let-in-end} retorna valor si la secuencia de expresiones 
        retorna valor y su tipo de retorno es el mismo que la secuencia de expresiones.
        
        En la comprobación semántica de esta estructura se comprueban semánticamente
        primero los grupos de declaraciones de tipos, luego las declaraciones de 
        funciones y variables y por último se comprueban semánticamente la secuencia
        de expresiones. Se reporatarán errores si se encuetran errores en alguna de
        estas comprobaciones semánticas. 
        
        En el proceso de comprobación semántica se determina si el nodo tiene valor
        de retorno, en cuyo caso tomará valor la propiedad C{return_type}
        """
        self._scope = Scope(scope) 
        all_types = set()
        local_types = []
        all_functions = set()
        local_functions = [] 
        
        for type_declaration_group in self._type_declaration_groups:
            group_types = type_declaration_group.collect_definitions(self._scope, 
                                                                     errors)
            local_types.append(group_types)
            all_types = all_types.union(group_types)
            
        for index, type_declaration_group in enumerate(self._type_declaration_groups):
            local_scope = FakeScope(self.scope, 
                                    all_types.difference(local_types[index]), 
                                    set())
            type_declaration_group.check_semantics(local_scope, errors)
            
        for func_declaration_group in self._function_declaration_groups:
            group_func = func_declaration_group.collect_definitions(self.scope,
                                                                    errors)
            local_functions.append(group_func)
            all_functions = all_functions.union(group_func)
        
        for variable_declaration in self._members_declarations:
            variable_declaration.check_semantics(self.scope, errors)
        
        for index, func_declaration_group in enumerate(self._function_declaration_groups):
            local_scope = FakeScope(self.scope,
                                    set(), 
                                    all_functions.difference(local_functions[index]))
            func_declaration_group.check_semantics(local_scope, errors)
            
        self._expr_seq.check_semantics(self.scope, errors)
        
        if self._expr_seq.has_return_value():
            self._return_type = self._expr_seq.return_type
        else:
            self._return_type = None      
    
