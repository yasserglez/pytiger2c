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
    
    def _get_code_type(self):
        """
        Método para obtener el valor de la propiedad C{code_type}.
        """
        return self._code_type
    
    def _set_code_type(self, value):
        """
        Método para cambiar el valor de la propiedad C{code_type}.
        """
        self._code_type = value
    
    code_type = property(_get_code_type, _set_code_type)

    def __init__(self):
        """
        Inicializa la clase base de la jerarquía.
        """
        super(TigerType, self).__init__()
        self._code_type = None
