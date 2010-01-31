# -*- coding: utf-8 -*-

"""
Definición de las reglas de la gramática.
"""

import os

from pytiger2c.contrib.ply import lex, yacc


# Begin lexer rules.

tokens = ('NUMBER', 'PLUS')

def t_NUMBER(token):
    r'\d+'

t_PLUS = r'\+'

t_ignore  = ' \t'


# Begin parser rules.

def p_expr_plus(symbols):
    r'expr : expr PLUS NUMBER'
    symbols[0] = symbols[1] + symbols[3]
    
def p_expr_number(symbols):
    r'expr : NUMBER'
    symbols[0] = symbols[1]    


# Creating lexer and parser instances.

_cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache'))

lexer = lex.lex(debug=True, outputdir=_cachedir, lextab='lexer')
parser = yacc.yacc(debug=True, outputdir=_cachedir, tabmodule='parser', 
                   debugfile=os.path.join(_cachedir, 'parser.txt'))

# Comment the previous lines and uncomment the following when we are sure
# the grammar is OK to enable running PLY in optimization mode.
# lexer = lex.lex(optimize=True, outputdir=_cachedir, lextab='lexer')
# parser = yacc.yacc(optimize=True, outputdir=_cachedir, tabmodule='parser',
#                    debugfile=os.path.join(_cachedir, 'parser.txt'))