# -*- coding: utf-8 -*-

"""
Análisis léxico-gráfico utilizando PLY.
"""

from pytiger2c.contrib.ply import lex
from pytiger2c.grammar.common import cachedir, compute_column
from pytiger2c.errors import SyntacticError


_reserved = (
    'ARRAY', 'IF', 'THEN', 'ELSE', 'WHILE', 'FOR', 'TO', 'DO', 'LET',
    'IN', 'END', 'OF', 'BREAK', 'NIL', 'FUNCTION', 'VAR', 'TYPE',
)

# Build the dictionary used to map each _reserved word to the identifier 
# of the token corresponding the _reserved word.
_reserved_map = {}
for word in _reserved:
    _reserved_map[word.lower()] = word

tokens = _reserved + (
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
    line, column = token.lexer.lineno, compute_column(token)
    raise SyntacticError(message.format(char=token.value[0], line=line, column=column))

# This rule is used to track newlines (\n\r, \r\n, and \r, and \n, freely intermixed).
def t_newline(token):
    r'\r*\n(\r|\n)*'
    token.lexer.lineno += token.value.count('\n')
    # Since nothing is returned this token is discarded.

# Identifiers and _reserved words.
def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # Check for _reserved words.
    token.type = _reserved_map.get(token.value, 'ID')
    return token

# Integer literal.
t_INTLIT = r'\d+'

# String literal (ANSI-C strings).
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


lexer = lex.lex(debug=True, outputdir=cachedir, lextab='lexer')
# Comment the previous lines and uncomment the following when we are sure
# the grammar is OK to enable running PLY in optimization mode.
# lexer = lex.lex(optimize=True, outputdir=_cachedir, lextab='lexer')
