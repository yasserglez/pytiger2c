# -*- coding: utf-8 -*-

"""
Análisis léxico-gráfico utilizando PLY.
"""

import os
import re

from pytiger2c.contrib.ply import lex
from pytiger2c.grammar.common import compute_column
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

# Nested comments are handled using an special COMMENT state.
states = (
    ('COMMENT', 'exclusive'),
)

# The action attached to this token pushes a COMMENT state into the state stack
# This has to be done in all lexer states because comments can be nested. 
def t_ANY_comment_begin(token):
    r'/\*'
    token.lexer.push_state('COMMENT')
    # Since nothing is returned, this token is discarded.
    
# If the lexer is in the COMMENT state and a comment is closed pop the
# current state from the state stack.
def t_COMMENT_comment_end(token):
    r'\*/'
    token.lexer.pop_state()
    # Since nothing is returned, this token is discarded.

# Ignore everything in the COMMENT state. We only need to match /* and */.
def t_COMMENT_error(token):
    token.lexer.skip(1)

# Completely ignored characters
t_ANY_ignore = ' \t'

# Error handling rule.
def t_error(token):
    message = "Illegal character '{char}' at line {line} column {column}"
    line, column = token.lexer.lineno, compute_column(token)
    raise SyntacticError(message.format(char=token.value[0], line=line, column=column))

# This rule is used to track newlines (\n\r, \r\n, and \r, and \n, freely intermixed).
# The ANY prefix is used to make this a valid token in all lexer states.
def t_ANY_newline(token):
    r'\r*\n(\r|\n)*'
    token.lexer.lineno += token.value.count('\n')
    # Since nothing is returned, this token is discarded.

# Identifiers and _reserved words.
def t_ID(token):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    # Check for _reserved words.
    token.type = _reserved_map.get(token.value, 'ID')
    return token

# Integer literals.
t_INTLIT = r'\d+'

# String literals.
def t_STRLIT(token):
    r'\"((\\[nt])|(\\")|(\\\\)|(\\\^[@A-Z[\]^_])|(\\[0-9]{3})|(\\\s+\\)|([^\\"]))*\"'
    # Converting the value of the token into a valid C literal string.
    def _escape(number):
        """
        Recibe un entero representando el número correspondiente a un caracter ASCII y
        devuelve la secuencia de caracteres necesaria para representar este caracter
        en un literal de cadena de C. La secuencia de caracteres consiste en un 
        backslash seguido de 3 dígitos octales.
        
        @type number: C{int}
        @param number: Entero representando el caracter ASCII.
        
        @rtype: C{str}
        @return: Representación válida del caracter en un literal de cadena de C.
        """
        if 0 <= number <= 255:
            return r'\{0}'.format(oct(number)[-3:])
        else:
            message = "Invalid string literal at line {line} column {column}"
            line, column = token.lexer.lineno, compute_column(token)
            raise SyntacticError(message.format(line=line, column=column))
    repl = lambda match: _escape(ord(match.group(1)) - 64)
    token.value = re.sub(r'\\^([@A-Z[\]^_])', repl, token.value)
    repl = lambda match: _escape(int(match.group(1)))
    token.value = re.sub(r'\\([0-9]{3})', repl, token.value)
    # Update the line counter here before stripping whitespaces.
    token.lexer.lineno += token.value.count('\n')
    # Strip whitespaces between \s.
    token.value = re.sub(r'\\\s+\\', '', token.value)
    # Strip the double quotes.
    token.value = token.value[1:-1]
    return token
    
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


_cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache'))
lexer = lex.lex(debug=True, outputdir=_cachedir, lextab='lexer')
# Comment the previous lines and uncomment the following when we are sure
# the grammar is OK to enable running PLY in optimization mode.
# lexer = lex.lex(optimize=True, outputdir=_cachedir, lextab='lexer')
