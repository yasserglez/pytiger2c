# -*- coding: utf-8 -*-

"""
Clase base de la jerarquía de los nodos del árbol de sintáxis abstracta.
"""


class LanguageNode(object):
    """
    Clase base de la jerarquía de los nodos del árbol de sintáxis abstracta.
    
    Todas las clases deben heredar de la clase base C{LanguageNode} e implementar 
    los métodos C{check_semantics} y C{generate_code} según corresponda a la estructura 
    del lenguaje que representa.
    """
    
    def _get_line_number(self):
        """
        Método para obtener el valor de la propiedad C{line_number}.
        """
        return self._line_number
    
    def _set_line_number(self, line_number):
        """
        Método para cambiar el valor de la propiedad C{line_number}.
        """
        self._line_number = line_number
    
    line_number = property(_get_line_number, _set_line_number)
    
    def __init__(self):
        """
        Inicializa el nodo del árbol de sintáxis abstracta.
        """
        super(LanguageNode, self).__init__()
        self._line_number = None
    
    def check_semantics(self, errors):
        """
        Comprueba que la estructura del lenguaje Tiger representada por el nodo 
        sea correcta semánticamente.

        @type errors: C{list}
        @param errors: Lista a la cual se deben añadir los mensajes de error de
            los errores semánticos encontrados durante la comprobación de la
            estructura del lenguaje representada por el nodo del árbol de 
            sintáxis abstracta.
        """
        raise NotImplementedError()
    
    def generate_code(self):
        """
        Genera el código correspondiente a la estructura del lenguaje Tiger
        representada por el nodo.
        
        @raise CodeGenerationError: Esta excepción se lanzará cuando se produzca
            algún error durante la generación del código correspondiente al nodo.,
            La excepción contendrá información acerca del error.
        """
        raise NotImplementedError()
