def p_expr_plus(symbs):
    r'expr : expr PLUS term'
    symbs[0] = symbs[1] + symbs[3]