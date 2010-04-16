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
    
    def _get_code_name(self):
        """
        Método para obtener el valor de la propiedad C{code_name}.
        """
        return self._code_name
    
    code_name = property(_get_code_name)    

    def __init__(self):
        """
        Inicializa la clase base de la jerarquía.
        """
        super(TigerType, self).__init__()
        self._code_name = None
