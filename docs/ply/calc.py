# -*- coding: utf-8 -*-

"""
Ejemplo de un evaluador de expresiones aritméticas con PLY.
"""

from ply import lex, yacc

# Reglas del lexer.

tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')

def t_NUMBER(token):
    r'\d+'
    token.value = int(token.value)
    return token

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore  = ' \t'


# Reglas del parser.

def p_expr_plus(symbs):
    r'expr : expr PLUS term'
    symbs[0] = symbs[1] + symbs[3]
    
def p_expr_minus(symbs):
    r'expr : expr MINUS term'
    symbs[0] = symbs[1] - symbs[3]
    
def p_expr_term(symbs):
    r'expr : term'
    symbs[0] = symbs[1]

def p_term_times(symbs):
    r'term : term TIMES factor'
    symbs[0] = symbs[1] * symbs[3]
    
def p_term_divide(symbs):
    r'term : term DIVIDE factor'
    symbs[0] = symbs[1] / symbs[3]
    
def p_term_factor(symbs):
    r'term : factor'
    symbs[0] = symbs[1]

def p_factor_number(symbs):
    r'factor : NUMBER'
    symbs[0] = symbs[1]
    
def p_factor_paren(symbs):
    r'factor : LPAREN expr RPAREN'
    symbs[0] = symbs[2]


def main():
    """
    Función principal del script.
    """
    lexer = lex.lex()
    parser = yacc.yacc()
    while True:
        try:
            expression = raw_input('expression: ')
        except EOFError:
            break
        if expression:
            value = parser.parse(expression, lexer=lexer)
            print 'value: ', value


if __name__ == '__main__':
    main()