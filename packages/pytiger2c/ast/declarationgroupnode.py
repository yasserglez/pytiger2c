# -*- coding: utf-8 -*-

"""
Clase C{DeclarationGroupNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.nonvaluedexpressionnode import NonValuedExpressionNode


class DeclarationGroupNode(NonValuedExpressionNode):
    """
    Clase C{DeclarationGroupNode} del árbol de sintáxis abstracta.
    
    Este nodo del árbol de sintáxis abstracta es la clase base de los
    nodos C{TypeDeclarationGroupNode} y C{FunctionDeclarationGroupNode},
    los cuales representan un grupo de declaraciones consecutivas de tipos 
    o funciones respectivamente. En nodos tienen el objetivo de garantizar
    durante la comprobación semántica que no se hagan declaraciones de 
    variables entre declaraciones de tipos o funciones mutuamente recursivas
    ya que si esto sucede se producen situaciones ambiguas.
    """
    
    def _get_declarations(self):
        """
        Método para obtener el valor de la propiedad C{declarations}.
        """
        return self._declarations
    
    declarations = property(_get_declarations)
    
    def __init__(self):
        """
        Inicializa la clase C{DeclarationGroupNode}.
        """
        super(DeclarationGroupNode, self).__init__()
        self._declarations = []
        
    def collect_definitions(self, scope, errors):
        """        
        Para obtener información acerca de los parámetros recibidos por 
        el método consulte la documentación del método C{check_semantics} 
        en la clase C{LanguageNode}.
        
        Este método define, recoge y devuelve las declaraciones de tipos o 
        funciones (según sea el caso) hechas en el grupo de declaraciones 
        representado por este nodo de sintáxis abstracta. Estos conjuntos de 
        declaraciones se utilizan en la comprobación semántica de la estructura
        C{let-in-end}, donde está contenido el grupo de declaraciones, para 
        garantizar que no se hagan definiciones de tipos o funciones mutuamente 
        recursivos iterrumpidos por declaraciones de variables.
        
        @rtype: C{set}
        @return: Conjunto con los nombres de los tipos o funciones 
            definidos en este grupo.
        """
        raise NotImplementedError()

    def generate_dot(self, generator):
        """
        Genera un grafo en formato Graphviz DOT correspondiente al árbol de 
        sintáxis abstracta del programa Tiger del cual este nodo es raíz.
        
        Para obtener información acerca de los parámetros recibidos por
        este método consulte la documentación del método C{generate_dot}
        de la clase C{LanguageNode}.
        """
        me = generator.add_node(str(self.__class__.__name__))
        for declaration in self.declarations:
            declaration = declaration.generate_dot(generator)
            generator.add_edge(me, declaration)
        return me
