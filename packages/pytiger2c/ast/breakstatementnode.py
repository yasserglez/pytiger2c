# -*- coding: utf-8 -*-

"""
Clase C{BreakStatementNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode
from pytiger2c.ast.whilestatementnode import WhileStatementNode
from pytiger2c.ast.forstatementnode import ForStatementNode
from pytiger2c.ast.callabledeclarationnode import CallableDeclarationNode


class BreakStatementNode(NonValuedExpressionNode):
    """
    Clase C{BreakStatementNode} del árbol de sintáxis abstracta.
    
    Representa la expresión C{break} del lenguaje Tiger. La expresión C{break}
    termina la evaluación de las instrucciones C{while} y C{for}.
    """
    
    def __init__(self):
        """
        Inicializa la clase C{BreakStatementNode}.
        """
        super(BreakStatementNode, self).__init__()

    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La expresión C{break} termina la evaluación de la instrucción C{while} o
        C{for} donde está contenida, dentro de la misma función o procedimiento.
        Cualquier otro uso de la expresión C{break} es inválido. 

        En la comprobación semántica de este nodo del árbol de sintáxis abstracta 
        se recorre el árbol hacia la raíz buscando una instrucción C{while} o C{for}
        que se debe encontrar antes de una declaración de función o procedimiento.
        Se reportarán errores semánticos si se llega a la raíz del árbol y no se
        encuentra una instrucción C{while} o C{for} o si se encuentra una declaración
        de función o procedimiento antes de encontrar una instrucción C{while} o C{for}.
        """
        self._scope = scope
        
        stop_nodes = (WhileStatementNode, ForStatementNode, CallableDeclarationNode)
        current_node = self.parent_node
        while current_node != None and not isinstance(current_node, stop_nodes):
            # Find the first WhileStatementNode, ForStatementNode or CallableDeclarationNode
            # from the parent of the break node until the root of the AST is found.
            current_node = current_node.parent_node
        if current_node == None:
            message = 'break used out of a while or for statement at line {line}'
            errors.append(message.format(line=self.line_number))
        elif isinstance(current_node, CallableDeclarationNode):
            message = 'Invalid usage of the break statement at line {line}'
            errors.append(message.format(line=self.line_number))
