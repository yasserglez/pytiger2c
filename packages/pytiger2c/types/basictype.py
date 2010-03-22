# -*- coding: utf-8 -*-

"""
Clase de la jerarquía de tipos de Tiger representando los tipos básicos
definidos en el lenguaje Tiger.
"""

from pytiger2c.types.tigertype import TigerType


class BasicType(TigerType):
    """
    Clase de la jerarquía de tipos de Tiger representando los tipos básicos
    definidos en el lenguaje Tiger.
    
    Esta clase representa los tipos definidos en la librería estándar de Tiger.
    Estos tipos son C{nil}, C{int} y C{string}.
    """
    
    def __init__(self):
        """
        Inicializa la clase representando los tipos básicos del Lenguaje Tiger.
        """
        super(BasicType, self).__init__(True)
    
    def __eq__(self, other):
        """
        Implementación por defecto de la comparación entre los tipos básicos del
        lenguaje Tiger.  
        Dos tipos básicos serán iguales si ambos son instancia de la misma clase.
        
        @type other: C{TigerType}
        @param other: Otro tipo de Tiger con el que efectuar la comparación.
        
        @rtype: C{bool}
        @return: Retorna C{True} si los ambos son iguales.
        """
        return isinstance(other, self.__class__)
    
    def __ne__(self, other):
        """
        Esta comparación se define como la negación del resultado obtenido por C{__eq__}.
        Ver documentación del método C{__eq__} para más información.
        
        @type other: C{TigerType}
        @param other: Otro tipo de Tiger con el que efectuar la comparación.
        
        @rtype: C{bool}
        @return: Retorna C{True} si los ambos no son iguales.        
        """
        return not self.__eq__(other)    
