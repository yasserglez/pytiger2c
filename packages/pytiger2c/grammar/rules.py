# -*- coding: utf-8 -*-

"""
Definición de las reglas de la gramática.
"""

from pytiger2c.contrib.ply import lex, yacc
from pytiger2c.errors import SyntacticError
import os



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

#expr Productions
#Literals.
def p_expr_nil(symbols):
    r'expr : NIL'

def p_expr_int(symbols):
    r'expr : INTLIT'
    
def p_expr_str(symbols):
    r'expr : STRLIT'

#Array and Recors creations.
def p_expr_array(symbols):
    r'expr : type_id LBRACKET expr RBRACKET OF expr'

def p_expr_record(symbols):
    r'expr : type_id LBRACE field_list RBRACE'
    
#Variables, field, elements of an array.
def p_expr_lvalue(symbols):
    r'expr : lvalue'

#Operations 
def p_expr_negative(symbols):
    r'expr : MINUS expr'

def p_expr_bin_op(symbols):
    r'expr : expr bin_operator expr'

def p_expr_exprs(symbols):
    r'expr : LPAREN expr_seq RPAREN'

#Assigment
def p_expr_assign(symbols):
    r'expr : lvalue ASSIGN expr'

#Function Call
def p_expr_func(symbols):
    r'expr : ID LPAREN expr_list RPAREN'

#Control Structures
def p_expr_if(symbols):
    r'expr : IF expr THEN expr'

def p_expr_if_else(symbols):
    r'expr : IF expr THEN expr ELSE expr'

def p_expr_while(symbols):
    r'expr : WHILE expr DO expr'
    
def p_expr_for(symbols):
    r'expr : FOR ID ASSIGN expr TO expr DO expr'

def p_expr_break(symbols):
    r'expr : BREAK'

def p_expr_let(symbols):
    r'expr : LET declaration_list IN expr_seq END'
    
#type_id productions.
def p_type_id(symbols):
    r'type_id : ID'

#lvalue productions.
def p_lvalue_id(symbols):
    r'lvalue : ID'
    
def p_lvalue_record(symbols):
    r'lvalue : lvalue PERIOD ID'
    
def p_lvalue_array(symbols):
    r'lvalue : lvalue LBRACKET expr RBRACKET'

#expr_seq productions.
def p_expr_seq_expr(symbols):
    r'expr_seq : expr'

def p_expr_seq_expr_seq(symbols):
    r'expr_seq : expr_seq SEMICOLON expr'
    
#declaration_list productions.
def p_declaration_list_declaration(symbols):
    r'declaration_list : declaration'

def p_declaration_list_declaration_list(symbols):
    r'declaration_list : declaration_list declaration'

#field_list productions.
def p_field_list_field(symbols):
    r'field_list : ID EQ expr'

def p_field_list_field_list(symbols):
    r'field_list : field_list COMMA ID EQ expr'

#expr_list productions.
def p_expr_list_expr(symbols):
    r'expr_list : expr'

def p_expr_list_expr_list(symbols):
    r'expr_list : expr_list COMMA expr'

#declaration productions.
def p_declaration_type(symbols):
    r'declaration : type_declaration'

def p_declaration_var(symbols):
    r'declaration : variable_declaration'

def p_declaration_func(symbols):
    r'declaration : function_declaration'

#type_declaration productions.
def p_type_declaration(symbols):
    r'type_declaration : TYPE type_id EQ type'

#type productions.
def p_type_type_id(symbols):
    r'type : type_id'

def p_type_record(symbols):
    r'type : type_fields'

def p_type_array(symbols):
    r'type : ARRAY OF type_id'

#type_fields productions
def p_type_fields_type_field(symbols):
    r'type_fields : type_field'

def p_type_fields_type_fields(symbols):
    r'type_fields : type_fields COMMA type_field'

#type_field productions
def p_type_field(symbols):
    r'type_field : ID COLON type_id'

#variable_declaration productions
def p_variable_declaration_simple(symbols):
    r'variable_declaration : VAR ID ASSIGN expr'

def p_variable_declaration(symbols):
    r'variable_declaration : VAR ID COLON type_id ASSIGN expr'
    
#function_declaration productions.
def p_function_declaration_simple(symbols):
    r'function_declaration : FUNCTION ID LPAREN type_fields RPAREN EQ expr'

def p_function_declaration(symbols):
    r'function_declaration : FUNCTION ID LPAREN type_fields RPAREN COLON type_id EQ expr'

#bin_operator productions.
def p_bin_operator(symbols):
    """bin_operator : PLUS 
                    | MINUS 
                    | TIMES 
                    | DIVIDE 
                    | EQ 
                    | NE 
                    | LT 
                    | LE 
                    | GT 
                    | GE 
                    | AND 
                    | OR""" 




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