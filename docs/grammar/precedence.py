precedence = (
    # The following fixes the shift/reduce conflict caused by rules ending with
    # the non-terminal expr and the rules for binary operators.
    ('nonassoc', 'OF', 'THEN', 'DO'),
    # The token ELSE has higher priority to fix the dangling-else shift/reduce
    # conflict. If an ELSE if found it should be shifted instead of reducing the
    # if-then without the else clause.
    ('nonassoc', 'ELSE'),
    # The following fixes the shift/reduce conflict between shifting the
    # [ token in the p_expr_array production (array literal) or reducing
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
