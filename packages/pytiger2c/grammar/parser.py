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

def p_error(token):
    message = "Unexpected token '{token}' at line {line} column {column}"
    line, column = token.lexer.lineno, compute_column(token)
    raise SyntacticError(message.format(token=token.type, line=line, column=column))

# NOTE: When naming a production we follow the following rule: 
# A "group" a group of items without an "special" character between them.
# A "list" a group of items separated by commas.
# A "sequence" (or "seq" for short) is a group of items separated by semicolons.

# The left part of the first production of the grammar (by default) 
# will be considered the starting symbol of the grammar. 
def p_program(symbols):
    "program : expr"

# Literals.
def p_expr_nil(symbols):
    "expr : NIL"

def p_expr_int(symbols):
    "expr : INTLIT"
    
def p_expr_str(symbols):
    "expr : STRLIT"
    
# Left values of an assignment. Variables, record fields and elements of arrays.
def p_expr_left_value(symbols):
    "expr : left_value"
    
# Creating a new array.
def p_expr_array(symbols):
    "expr : type_id LBRACKET expr RBRACKET OF expr"

# Creating a new record.
def p_expr_record(symbols):
    "expr : type_id LBRACE field_list RBRACE"
    
# Operations over expressions. 
def p_expr_unary_minus(symbols):
    "expr : MINUS expr"

def p_expr_bin_op(symbols):
    "expr : expr bin_op expr"

# A group of expressions separated by semicolons.
def p_expr_expr_seq(symbols):
    "expr : LPAREN expr_seq RPAREN"

# Assignment.
def p_expr_assign(symbols):
    "expr : left_value ASSIGN expr"

# Function call.
def p_expr_func(symbols):
    "expr : ID LPAREN expr_list RPAREN"

# Flow control structures.
def p_expr_if(symbols):
    "expr : IF expr THEN expr"

def p_expr_if_else(symbols):
    "expr : IF expr THEN expr ELSE expr"

def p_expr_while(symbols):
    "expr : WHILE expr DO expr"
    
def p_expr_for(symbols):
    "expr : FOR ID ASSIGN expr TO expr DO expr"

def p_expr_break(symbols):
    "expr : BREAK"

# The let block.
def p_expr_let(symbols):
    "expr : LET dec_group IN expr_seq END"
    
# An id for a type.
def p_type_id(symbols):
    "type_id : ID"

# What is a left value of an assignment expression? A variable.
def p_left_value_id(symbols):
    "left_value : ID"
    
# What is a left value of an assignment expression? A field of a record.    
def p_left_value_record(symbols):
    "left_value : left_value PERIOD ID"
    
# What is a left value of an assignment expression? An item from an array.    
def p_left_value_array(symbols):
    "left_value : left_value LBRACKET expr RBRACKET"

# A group of expressions separated by semicolons.
def p_expr_seq_single(symbols):
    "expr_seq : expr"

def p_expr_seq_multiple(symbols):
    "expr_seq : expr_seq SEMICOLON expr"
    
# A group of declarations. No "special" characters between declarations!
def p_dec_group_single(symbols):
    "dec_group : dec"

def p_dec_group_multiple(symbols):
    "dec_group : dec_group dec"

# A list of field names, the equals character and an expression 
# to assign values for each one of the fields of a record.
def p_field_list_single(symbols):
    "field_list : field_assign"

def p_field_list_multiple(symbols):
    "field_list : field_list COMMA field_assign"
    
def p_field_assign(symbols):
    "field_assign : ID EQ expr"

# A group of expressions separated by commas.
def p_expr_list_single(symbols):
    "expr_list : expr"

def p_expr_list_multiple(symbols):
    "expr_list : expr_list COMMA expr"

# What is a declaration? A type declaration.
def p_dec_type(symbols):
    "dec : type_dec"

# What is a declaration? A variable declaration.
def p_dec_var(symbols):
    "dec : var_dec"

# What is a declaration? A function declaration.
def p_dec_func(symbols):
    "dec : func_dec"

# Type declarations.
def p_type_dec(symbols):
    "type_dec : TYPE type_id EQ type"

# What is a valid type? An alias for a previously defined type.
def p_type_alias(symbols):
    "type : type_id"

# What is a valid type? The definition of the fields of a record.
def p_type_record(symbols):
    "type : LBRACE field_types RBRACE"

# What is a valid type? An array definition.
def p_type_array(symbols):
    "type : ARRAY OF type_id"

# A list of field types declaration separated by commas.
def p_field_types_single(symbols):
    "field_types : field_type"

def p_field_types_multiple(symbols):
    "field_types : field_types COMMA field_type"

# Declaration of the type of a field. An identifier for the
# field followed by a colon and the type of the field.
def p_field_type(symbols):
    "field_type : ID COLON type_id"

# Variable declaration.
def p_var_dec_without_type(symbols):
    "var_dec : VAR ID ASSIGN expr"

def p_var_dec_with_type(symbols):
    "var_dec : VAR ID COLON type_id ASSIGN expr"
    
# Function declaration.
def p_func_dec_without_return(symbols):
    "func_dec : FUNCTION ID LPAREN field_types RPAREN EQ expr"

def p_func_dec_with_return(symbols):
    "func_dec : FUNCTION ID LPAREN field_types RPAREN COLON type_id EQ expr"

# Binary operators.
def p_bin_op(symbols):
    """
    bin_op : PLUS
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
           | OR
    """ 


parser = yacc.yacc(debug=True, outputdir=cachedir, tabmodule='parser',
                   debugfile=os.path.join(cachedir, 'parser.txt'))
# Comment the previous lines and uncomment the following when we are sure
# the grammar is OK to enable running PLY in optimization mode.
# parser = yacc.yacc(optimize=True, outputdir=_cachedir, tabmodule='parser',
#                    debugfile=os.path.join(_cachedir, 'parser.txt'))
