# -*- coding: utf-8 -*-

"""
Definición de las reglas de la gramática.
"""

import os

from pytiger2c.contrib.ply import lex, yacc
from pytiger2c.errors import SyntacticError
from pytiger2c.ast import *


def _compute_column(token):
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
    column = (token.lexpos - last_newline) + 1
    return column


# Begin lexer rules.

reserved = (
    'ARRAY', 'IF', 'THEN', 'ELSE', 'WHILE', 'FOR', 'TO', 'DO', 'LET',
    'IN', 'END', 'OF', 'BREAK', 'NIL', 'FUNCTION', 'VAR', 'TYPE',
)

# Build the dictionary used to map each reserved word to the identifier 
# of the token corresponding the reserved word.
reserved_map = {}
for word in reserved:
    reserved_map[word.lower()] = word

tokens = reserved + (
    # Literals: identifier, integer constant, string constant
    'ID', 'INTLIT', 'STRLIT',
    
    # Operators: + - * / = <> < <= > >= & | :=  
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR', 'ASSIGN',
    
    # Delimeters: . , : ; ( ) [ ] { }
    'PERIOD', 'COMMA', 'COLON', 'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
)

# Completely ignored characters
t_ignore = ' \t'

# Error handling rule.
def t_error(token):
    message = "Illegal character '{char}' at line {line} column {column}"
    line, column = token.lexer.lineno, _compute_column(token)
    raise SyntacticError(message.format(char=token.value[0], line=line, column=column))

# This rule is used to track newlines (\n\r, \r\n, and \r, and \n, freely intermixed).
def t_newline(token):
    r'\r*\n(\r|\n)*'
    token.lexer.lineno += token.value.count('\n')
    # Since nothing is returned this token is discarded.

# Identifiers and reserved words.
def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # Check for reserved words.
    token.type = reserved_map.get(token.value, 'ID')
    return token

# Integer literal.
t_INTLIT = r'\d+'

# String literal. ANSI-C strings: enclosed by ", with support for the following escapes:
# \a, \b, \f, \n, \r, \t, \v, \num (the character which code is num in octal, num is composed of
# exactly three octal characters), \xnum (the character which code is num in hexadecimal (upper
# case or lower case or mixed), num is composed of exactly 2 hexadecimal characters), 
# \\ (single backslash), \" (double quote). If \character is found and no rule above applies, 
# this is an error. All the other characters are plain characters and are to be included in 
# the string.
t_STRLIT = r'\"((\\[abfnrtv])|(\\[0-7][0-7][0-7])|(\\x[0-9a-fA-F][0-9a-fA-F])|(\\\\)|(\\")|([^\\"]))*\"'

# Operators.
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'='
t_NE = r'<>'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_AND = r'&'
t_OR = r'\|'
t_ASSIGN = r':='

# Delimiters.
t_PERIOD = r'\.'
t_COMMA = r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


# Begin parser rules.

def p_error(symbols):
    # TODO: Finish error handling!
    raise SyntacticError()

def p_program(symbols):
    r'program : expr'

def p_expr(symbols):
    r'expr :'
    

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