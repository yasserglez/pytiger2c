# -*- coding: utf-8 -*-

"""
Análisis sintáctico utilizando PLY.
"""

import os
import itertools

from pytiger2c.contrib.ply import yacc
from pytiger2c.grammar.common import compute_column
from pytiger2c.grammar.lexer import lexer, tokens
from pytiger2c.errors import SyntacticError
from pytiger2c.ast import *


# Precedence rules.
precedence = (
    # The following fixes the shift/reduce conflict caused by rules ending with 
    # the non-terminal expr and the rules for binary operators.
    ('nonassoc', 'OF', 'THEN', 'DO'),
    # The token ELSE has higher priority to fix the dangling-else shift/reduce 
    # conflict. If an ELSE if found it should be shifted instead of reducing the
    # if-then without the else clause.
    ('nonassoc', 'ELSE'),
    # The following fixes the shift/reduce conflict between shifting the
    # [ token in the p_expr_array production (array declaration) or reducing 
    # the p_lvalue_id production.
    ('nonassoc', 'LVALUE_ID'),
    ('nonassoc', 'LBRACKET'),
    # Operator precedence.
    ('nonassoc', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
)

def p_error(token):
    if token:
        message = "Unexpected token '{token}' at line {line} column {column}"
        line, column = lexer.lineno, compute_column(token)
        raise SyntacticError(message.format(token=token.type, line=line, column=column))
    else:
        message = "Unexpected end of the input file"
        raise SyntacticError(message)

# NOTE: When naming a production we follow the following rule: 
# A "group" a group of items without an "special" character between them.
# A "list" a group of items separated by commas.
# A "sequence" ("seq" for short) is a group of items separated by semicolons.

# The left part of the first production of the grammar (by default) 
# will be considered the starting symbol of the grammar. 
def p_program(symbols):
    "program : expr"
    if lexer.current_state() != 'INITIAL':
        message = "A comment was opened but not closed"
        raise SyntacticError(message)
    else:
        symbols[0] = symbols[1]
        symbols[0].parent_node = None

# Literals.
def p_expr_nil(symbols):
    "expr : NIL"
    symbols[0] = NilExpressionNode()
    symbols[0].line_number = symbols.lineno(1)

def p_expr_int(symbols):
    "expr : INTLIT"
    symbols[0] = IntegerLiteralExpressionNode(int(symbols[1]))
    symbols[0].line_number = symbols.lineno(1)

def p_expr_str(symbols):
    "expr : STRLIT"
    symbols[0] = StringLiteralExpressionNode(symbols[1])
    symbols[0].line_number = symbols.lineno(1)
    
# Left values of an assignment. Variables, record fields and elements of arrays.
def p_expr_lvalue(symbols):
    "expr : lvalue"
    symbols[0] = symbols[1]
    
# Creating a new array.
def p_expr_array(symbols):
    "expr : ID LBRACKET expr RBRACKET OF expr"
    symbols[0] = ArrayLiteralExpressionNode(symbols[1], symbols[3], symbols[6])
    symbols[0].line_number = symbols.lineno(1)
    symbols[3].parent_node = symbols[0]
    symbols[6].parent_node = symbols[0] 

# Creating a new record.
def p_expr_record(symbols):
    "expr : ID LBRACE field_list RBRACE"
    symbols[0] = RecordLiteralExpressionNode(symbols[1], symbols[3][0], symbols[3][1]) 
    symbols[0].line_number = symbols.lineno(1)
    
# Unary minus. 
def p_expr_unary_minus(symbols):
    "expr : MINUS expr %prec UMINUS"
    symbols[0] = UnaryMinusOperatorNode(symbols[2])
    symbols[0].line_number = symbols.lineno(1)
    symbols[2].parent_node = symbols[0]

# Binary operators.
def p_expr_bin_op(symbols):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr TIMES expr
         | expr DIVIDE expr 
         | expr EQ expr
         | expr NE expr 
         | expr LT expr
         | expr LE expr
         | expr GT expr
         | expr GE expr
         | expr AND expr
         | expr OR expr
    """
    if symbols[2] == "+":
        symbols[0] = PlusOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "-":
        symbols[0] = MinusOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "*":
        symbols[0] = TimesOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "/":
        symbols[0] = DivideOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "=":
        symbols[0] = EqualsOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "<>":
        symbols[0] = NotEqualsOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "<":
        symbols[0] = LessThanOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "<=":
        symbols[0] = LessEqualsThanOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == ">":
        symbols[0] = GreaterThanOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == ">=":
        symbols[0] = GreaterEqualsThanOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "&":
        symbols[0] = AndOperatorNode(symbols[1], symbols[3])
    elif symbols[2] == "|":
        symbols[0] = OrOperatorNode(symbols[1], symbols[3])
    symbols[0].line_number = symbols.lineno(2)
    symbols[1].parent_node = symbols[0]
    symbols[3].parent_node = symbols[0]

# A group of expressions enclosed by parenthesis separated by semicolons.
def p_expr_expr_seq(symbols):
    "expr : LPAREN expr_seq RPAREN"
    symbols[0] = symbols[2]
    symbols[0].line_number = symbols.lineno(1)

# Assignment.
def p_expr_assign(symbols):
    "expr : lvalue ASSIGN expr"
    symbols[0] = AssignmentNode(symbols[1], symbols[3])
    symbols[0].line_number = symbols.lineno(2)
    symbols[1].parent_node = symbols[0]
    symbols[3].parent_node = symbols[0]    

# Function call.
def p_expr_func(symbols):
    "expr : ID LPAREN expr_list RPAREN"
    symbols[0] = FunctionCallNode(symbols[1], symbols[3])
    symbols[0].line_number = symbols.lineno(1)
    for node in symbols[3]: 
        node.parent_node = symbols[0]    

# Flow control structures.
def p_expr_if(symbols):
    "expr : IF expr THEN expr"
    symbols[0] = IfThenStatementNode(symbols[2], symbols[4])
    symbols[0].line_number = symbols.lineno(1)
    symbols[2].parent_node = symbols[0]
    symbols[4].parent_node = symbols[0]       

def p_expr_if_else(symbols):
    "expr : IF expr THEN expr ELSE expr"
    symbols[0] = IfThenElseStatementNode(symbols[2], symbols[4], symbols[6])
    symbols[0].line_number = symbols.lineno(1)
    symbols[2].parent_node = symbols[0]
    symbols[4].parent_node = symbols[0]
    symbols[6].parent_node = symbols[0]        

def p_expr_while(symbols):
    "expr : WHILE expr DO expr"
    symbols[0] = WhileStatementNode(symbols[2], symbols[4])
    symbols[0].line_number = symbols.lineno(1)
    symbols[2].parent_node = symbols[0]
    symbols[4].parent_node = symbols[0]    
    
def p_expr_for(symbols):
    "expr : FOR ID ASSIGN expr TO expr DO expr"
    symbols[0] = ForStatementNode(symbols[2], symbols[4], symbols[6], symbols[8])
    symbols[0].line_number = symbols.lineno(1)
    symbols[4].parent_node = symbols[0]
    symbols[6].parent_node = symbols[0]
    symbols[8].parent_node = symbols[0]

def p_expr_break(symbols):
    "expr : BREAK"
    symbols[0] = BreakStatementNode()
    symbols[0].line_number = symbols.lineno(1)

# The let block.
def p_expr_let(symbols):
    "expr : LET dec_group IN expr_seq END"    
    symbols[0] = LetNode(symbols[2][0], symbols[2][1], symbols[2][2], symbols[4])
    symbols[0].line_number = symbols.lineno(1)
    for node in itertools.chain(symbols[2][0], symbols[2][1], symbols[2][2]):
        node.parent_node = symbols[0]
    symbols[4].parent_node = symbols[0]
    
# What is a left value of an assignment expression?
def p_lvalue_id(symbols):
    "lvalue : ID %prec LVALUE_ID"
    symbols[0] = VariableAccessNode(symbols[1])
    symbols[0].line_number = symbols.lineno(1)
    
def p_lvalue_record(symbols):
    "lvalue : lvalue PERIOD ID"
    symbols[0] = RecordAccessNode(symbols[1], symbols[3])
    symbols[0].line_number = symbols.lineno(2)
    symbols[1].parent_node = symbols[0] 
    
def p_lvalue_array(symbols):
    "lvalue : ID LBRACKET expr RBRACKET"
    variable = VariableAccessNode(symbols[1])
    symbols[0] = ArrayAccessNode(variable, symbols[3])
    symbols[0].line_number = symbols.lineno(2)
    variable.parent_node = symbols[0]
    symbols[3].parent_node = symbols[0]
    
def p_lvalue_array_lvalue(symbols):
    "lvalue : lvalue LBRACKET expr RBRACKET"
    symbols[0] = ArrayAccessNode(symbols[1], symbols[3])
    symbols[0].line_number = symbols.lineno(2)
    symbols[1].parent_node = symbols[0]
    symbols[3].parent_node = symbols[0]
    
# A group of expressions separated by semicolons.
def p_expr_seq_empty(symbols):
    "expr_seq : "
    symbols[0] = ExpressionSequenceNode()
    
def p_expr_seq_multiple(symbols):
    "expr_seq : expr_seq SEMICOLON expr"
    symbols[0] = symbols[1]
    symbols[0].expressions.append(symbols[3])
    symbols[3].parent_node = symbols[0] 

def p_expr_seq_single(symbols):
    "expr_seq : expr"
    symbols[0] = ExpressionSequenceNode()
    symbols[0].expressions.append(symbols[1])
    symbols[1].parent_node = symbols[0]
    
# A group of declarations. No "special" characters between declarations!

# A let expression with nothing between the in and end is valid.
def p_dec_group_empty(symbols):
    "dec_group : "
    symbols[0] = ([], [], []) 
    
def p_dec_group_multiple(symbols):
    "dec_group : dec_group dec"
    symbols[0] = symbols[1]
    symbols[0][0].extend(symbols[2][0])
    symbols[0][1].extend(symbols[2][1])
    symbols[0][2].extend(symbols[2][2])
    
# A list of field names, the equals character and an expression 
# to assign values for each one of the fields of a record.
def p_field_list_empty(symbols):
    "field_list : "
    symbols[0] = ([], [])

def p_field_list_single(symbols):
    "field_list : field_assign"
    symbols[0] = ([symbols[1][0]], [symbols[1][1]])

def p_field_list_multiple(symbols):
    "field_list : field_list COMMA field_assign"
    symbols[0] = symbols[1]
    symbols[0][0].append(symbols[3][0])
    symbols[0][1].append(symbols[3][1])
    
def p_field_assign(symbols):
    "field_assign : ID EQ expr"
    symbols[0] = (symbols[1], symbols[3])

# A group of expressions separated by commas.
def p_expr_list_empty(symbols):
    "expr_list : "
    symbols[0] = []
    
def p_expr_list_multiple(symbols):
    "expr_list : expr_list COMMA expr"
    symbols[0] = symbols[1]
    symbols[0].append(symbols[3])
    
def p_expr_list_single(symbols):
    "expr_list : expr"
    symbols[0] = []
    symbols[0].append(symbols[1])   

# What is a declaration? A block of continuous type declarations. 
# Mutually recursive type declarations must be defined without any 
# variable or function declaration in between.
def p_dec_type_dec_group(symbols):
    "dec : type_dec_group"
    symbols[0] = ([symbols[1]], [], [])

# What is a declaration? A variable declaration.
def p_dec_var(symbols):
    "dec : var_dec"
    symbols[0] = ([], [], [symbols[1]])

# What is a declaration? A block of continuous functions declarations. 
# Mutually recursive function declarations must be defined without any 
# variable or type declaration in between. 
def p_dec_func_dec_group(symbols):
    "dec : func_dec_group"
    symbols[0] = ([], [symbols[1]], [])

# What is a group of function declarations? A function declaration.
def p_func_dec_group_single(symbols):
    "func_dec_group : func_dec"
    symbols[0] = FunctionDeclarationGroupNode()
    symbols[0].declarations.append(symbols[1])
    symbols[1].parent_node = symbols[0]  
    
# What is a group of function declarations? A group of function 
# declarations followed by a function declaration.
def p_func_dec_group_multiple(symbols):
    "func_dec_group : func_dec_group func_dec"
    symbols[0] = symbols[1]
    symbols[0].declarations.append(symbols[2])
    symbols[2].parent_node = symbols[0]

# What is a group of type declarations? A type declaration.
def p_type_dec_group_single(symbols):
    "type_dec_group : type_dec"
    symbols[0] = TypeDeclarationGroupNode()
    symbols[0].declarations.append(symbols[1])
    symbols[1].parent_node = symbols[0]

# What is a group of type declarations? A group 
# of type declarations followed by a type declaration.
def p_type_dec_group_multiple(symbols):
    "type_dec_group : type_dec_group type_dec"
    symbols[0] = symbols[1]
    symbols[0].declarations.append(symbols[2])
    symbols[2].parent_node = symbols[0]

# Type declarations.
def p_type_dec(symbols):
    "type_dec : TYPE ID EQ type"
    symbols[0] = symbols[4]
    symbols[0].name = symbols[2]
    symbols[0].line_number = symbols.lineno(1)

# What is a valid type? An alias for a previously defined type.
def p_type_alias(symbols):
    "type : ID"
    symbols[0] = AliasTypeDeclarationNode(None, symbols[1])

# What is a valid type? The definition of the fields of a record.
def p_type_record(symbols):
    "type : LBRACE field_types RBRACE"
    symbols[0] = RecordDeclarationNode(None, symbols[2][0], symbols[2][1])
    
# What is a valid type? An array definition.
def p_type_array(symbols):
    "type : ARRAY OF ID"
    symbols[0] = ArrayDeclarationNode(None, symbols[3])

# A list of field types declaration separated by commas.
def p_field_types_empty(symbols):
    "field_types : "
    symbols[0] = ([], [])

def p_field_types_single(symbols):
    "field_types : field_type"
    symbols[0] = ([symbols[1][0]], [symbols[1][1]])

def p_field_types_multiple(symbols):
    "field_types : field_types COMMA field_type"
    symbols[0] = symbols[1]
    symbols[0][0].append(symbols[3][0])
    symbols[0][1].append(symbols[3][1])

# Declaration of the type of a field. An identifier for the
# field followed by a colon and the type of the field.
def p_field_type(symbols):
    "field_type : ID COLON ID"
    symbols[0] = (symbols[1], symbols[3])

# Variable declaration.
def p_var_dec_without_type(symbols):
    "var_dec : VAR ID ASSIGN expr"
    symbols[0] = InferredVariableDeclarationNode(symbols[2], symbols[4])
    symbols[0].line_number = symbols.lineno(1)
    symbols[4].parent_node = symbols[0]

def p_var_dec_with_type(symbols):
    "var_dec : VAR ID COLON ID ASSIGN expr"
    symbols[0] = StaticVariableDeclarationNode(symbols[2], symbols[6], symbols[4])
    symbols[0].line_number = symbols.lineno(1)
    symbols[6].parent_node = symbols[0]

# Function declaration.
def p_func_dec_without_return(symbols):
    "func_dec : FUNCTION ID LPAREN field_types RPAREN EQ expr"
    symbols[0] = ProcedureDeclarationNode(symbols[2], symbols[4][0], symbols[4][1], symbols[7])
    symbols[0].line_number = symbols.lineno(1)
    symbols[7].parent_node = symbols[0]

def p_func_dec_with_return(symbols):
    "func_dec : FUNCTION ID LPAREN field_types RPAREN COLON ID EQ expr"
    symbols[0] = FunctionDeclarationNode(symbols[2], symbols[4][0], symbols[4][1], symbols[9], symbols[7])
    symbols[0].line_number = symbols.lineno(1)
    symbols[9].parent_node = symbols[0]


_cachedir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache'))
# parser = yacc.yacc(debug=True, outputdir=_cachedir, tabmodule='parser',
#                    debugfile=os.path.join(_cachedir, 'parser.txt'))
# Comment the previous line and uncomment the following when
# the grammar is OK to enable running PLY in optimization mode.
parser = yacc.yacc(debug=False, write_tables=False, optimize=True, outputdir=_cachedir, 
                   tabmodule='parser', debugfile=os.path.join(_cachedir, 'parser.txt'))


# The following is used to debug the parser. It will parse input read from 
# standard input or from a file specified on the command line. 
if __name__ == '__main__':
    # This code was taken from the body of the lex.runmain() function.
    import sys
    try:
        filename = sys.argv[1]
        with open(filename) as fd:
            data = fd.read()
    except IndexError:
        sys.stdout.write("Reading from standard input (type EOF to end):\n")
        data = sys.stdin.read()
    parser.parse(data, debug=True)
