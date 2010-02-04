# -*- coding: utf-8 -*-

"""
Análisis sintáctico utilizando PLY.
"""

import os

from pytiger2c.contrib.ply import yacc
from pytiger2c.grammar.common import cachedir, compute_column
from pytiger2c.grammar import lexer
from pytiger2c.errors import SyntacticError


# Get the token map defined in the lexer module.
tokens = lexer.tokens

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


parser = yacc.yacc(debug=True, outputdir=cachedir, tabmodule='parser',
                   debugfile=os.path.join(cachedir, 'parser.txt'))
# Comment the previous lines and uncomment the following when we are sure
# the grammar is OK to enable running PLY in optimization mode.
# parser = yacc.yacc(optimize=True, outputdir=_cachedir, tabmodule='parser',
#                    debugfile=os.path.join(_cachedir, 'parser.txt'))
