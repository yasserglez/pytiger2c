# -*- coding: utf-8 -*-

"""
Clase C{RecordDeclarationNode} del árbol de sintáxis abstracta.
"""

from pytiger2c.ast.typedeclarationnode import TypeDeclarationNode
from pytiger2c.types.recordtype import RecordType


class RecordDeclarationNode(TypeDeclarationNode):
    """
    Clase C{RecordDeclarationNode} del árbol de sintáxis abstracta.
    """
    
    def __init__(self, name, fields_names, fields_typenames):
        """
        Inicializa la clase C{RecordDeclarationNode}.
        
        @type fields_names: C{list}
        @param fields_names: Lista con los nombres de los campos del C{record}, por pocisión.
        
        @type fields_typenames: C{list}
        @param fields_typenames: Lista con los nombres de los tipos de los campos, por pocisión.
        
        Para obtener información acerca del resto de los parámetros recibidos 
        por el método consulte la documentación del método C{__init__}
        en la clase C{TypeDeclarationNode}.
        """
        super(RecordDeclarationNode, self).__init__(name)
        self._type = RecordType(fields_names, fields_typenames)
        
    def check_semantics(self, scope, errors):
        """
        Para obtener información acerca de los parámetros recibidos por
        el método consulte la documentación del método C{check_semantics}
        en la clase C{LanguageNode}.
        
        La comprobación semántica correspondiente a este nodo se realiza
        completamente a nivel del C{TypeDeclarationGroupNode} en que fue
        declarado. Pues es el C{TypeDeclarationGroupNode} el que comprueba
        que están definidos los tipos de los campos de este C{record}, que el 
        nombre está disponible y además lo definie en su ámbito local.
        """
