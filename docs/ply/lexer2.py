def t_NUMBER(token):
    r'\d+'
    token.value = int(token.value)
    return token