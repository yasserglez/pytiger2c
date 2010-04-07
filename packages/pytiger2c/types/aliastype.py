# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando el tipo alias.
"""

from pytiger2c.types.tigertype import TigerType


class AliasType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando el tipo alias, 
    un alias es representado por este tipo durante la resolución del tipo
    concreto al que hace referencia durante chequeo semántico del nodo 
    donde fue definido.
    """
    
    def _get_alias_typename(self):
        """
        Método para obtener el valor de la propiedad C{alias_typename}.
        """
        return self._alias_typename
    
    alias_typename = property(_get_alias_typename)
    
    def __init__(self, alias_typename):
        """
        Inicializa la clase representando el tipo alias.
        
        @type alias_typename: C{str}
        @param alias_typename: Nombre del tipo al que hace referencia este
            alias.
        """
        super(AliasType, self).__init__()
        self._alias_typename =  alias_typename
