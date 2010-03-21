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