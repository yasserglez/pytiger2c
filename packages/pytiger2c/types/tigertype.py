# -*- coding: utf-8 -*-

"""
Clase base de la jerarquía de tipos de Tiger. 
"""

class TigerType(object):
    """
    Clase base de la jerarquía de tipos de Tiger.
    
    Todas las clases representando tipos válidos del lenguaje Tiger deben
    heredar de la clase base C{TigerType}. 
    """
    
    def _get_defined(self):
        """
        Método para obtener el valor de la propiedad C{defined}.
        """
        return self._defined
    
    def _set_defined(self, defined):
        """
        Método para cambiar el valor de la propiedad C{defined}.
        """
        self._defined = defined
    
    defined = property(_get_defined, _set_defined)

    def __init__(self, defined = False):
        """
        Inicializa la clase base de la jerarquía.
        """
        super(TigerType, self).__init__()
        self._defined = defined
        
    def __eq__(self, other):
        """
        Implementación por defecto de la comparación entre los tipos del lenguaje Tiger. 
        Dos tipos serán iguales si ambos son instancia de la misma clase. Es posible
        que clases descendientes de esta definan esta comparación de otra manera.
        
        @type other: C{TigerType}
        @param other: Otro tipo de Tiger con el que efectuar la comparación.
        """
        return isinstance(other, self.__class__)
        
    def __ne__(self, other):
        """
        Esta comparación se define como la negación del resultado obtenido por C{__eq__}.
        Ver documentación del método C{__eq__} para más información.
        
        @type other: C{TigerType}
        @param other: Otro tipo de Tiger con el que efectuar la comparación.        
        """
        return not self.__eq__(other)    
