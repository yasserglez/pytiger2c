# -*- coding: utf-8 -*-

"""
Elementos utilizados durante el análisis léxico-gráfico y sintáctico.
"""

import os


cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache'))


def compute_column(token):
    """
    Calcula el número de la columna del token recibido como parámetro contando
    hacia atrás en el flujo de entrada hasta encontrar el último salto de línea.
    
    @type token: C{LexToken}
    @param token: Token al que se le quiere calcular el número de columna. 
    
    @return: Número de la columna del token.
    @rtype: C{int}    
    """
    data = token.lexer.lexdata
    last_newline = data.rfind('\n', 0, token.lexpos)
    if last_newline < 0:
        last_newline = 0
    column = token.lexpos - last_newline
    return column
