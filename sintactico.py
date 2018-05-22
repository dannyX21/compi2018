from lexico import Lexico
from simbolo import CONST_TOKENS, TOKENS

def siguiente_componente_lexico():
    return lex.siguiente_componente_lexico()

def num_linea():
    return lex.num_linea

def compara(token_esperado):
    global complex_actual
    if type(token_esperado) == str:
        token_esperado = ord(token_esperado)
    if complex_actual and complex_actual.Token == token_esperado:
        complex_actual = siguiente_componente_lexico()
    elif token_esperado.Token <= 255:
        print("ln# {}: Se esperaba: '{}'".format(num_linea(),
        chr(token_esperado)))
    else:
        print("ln# {}: Se esperaba: '{}'".format(num_linea(),
        CONST_TOKENS[token_esperado]))

def EXPRESION():
    if verifica_terminal('('):
        compara('(')
        if EXPRESION():
            compara(')')
            return True
        else:
            return False
    elif EXPRESION_LOGICA():
        return True
    else:
        return False

# EXPRESION_LOGICA = TERMINO_LOGICO EXPRESION_LOGICA_PRIMA
# EXPRESION_LOGICA_PRIMA = oplog TERMINO_LOGICO EXPRESION_LOGICA_PRIMA | E

def EXPRESION_LOGICA():
    if TERMINO_LOGICO():
        if EXPRESION_LOGICA_PRIMA():
            return True
        else:
            return False
    else:
        return False

def EXPRESION_LOGICA_PRIMA():
    if(is_OPLOG(complex_actual)):
        compara(complex_actual.Token)
        if TERMINO_LOGICO():
            if EXPRESION_LOGICA_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def is_OPLOG(complex):
    return True if verifica_terminal('&') or verifica_terminal('|') else False

def is_OPREL(complex):
    op_rels = ['MAY','MAI','IGU','DIF','MEI','MEN']
    for op in op_rels:
        if verifica_terminal(op):
            return True
    return False

def is_OPSUMRES(complex):
    return verifica_terminal('+') or verifica_terminal('-')

def is_OPMULDIV(complex):
    op_muldiv = "*/%\\"
    for op in op_muldiv:
        if verifica_terminal(op):
            return True
    return False

def TERMINO_LOGICO():
    if verifica_terminal('!'):
        compara('!')
        compara('(')
        if EXPRESION_LOGICA() or EXPRESION_RELACIONAL():
            compara(')')
            return True
        else:
            return False
    elif EXPRESION_RELACIONAL():
        return True
    else:
        return False
def EXPRESION_RELACIONAL():
    if EXPRESION_ARITMETICA():
        if EXPRESION_RELACIONAL_PRIMA():
            return True
        else:
            return False
    else:
        return False

def EXPRESION_RELACIONAL_PRIMA():
    if is_OPREL(complex_actual):
        compara(complex_actual.Token)
        if EXPRESION_ARITMETICA():
            if EXPRESION_RELACIONAL_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def EXPRESION_ARITMETICA():
    if TERMINO_ARITMETICO():
        if EXPRESION_ARITMETICA_PRIMA():
            return True
        else:
            return False
    else:
        return False

def EXPRESION_ARITMETICA_PRIMA():
    if is_OPSUMRES(complex_actual):
        compara(complex_actual.Token)
        if TERMINO_ARITMETICO():
            if EXPRESION_ARITMETICA_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def TERMINO_ARITMETICO():
    if FACTOR_ARIMETICO():
        if TERMINO_ARITMETICO_PRIMA():
            return True
        else:
            return False
    else:
        return False

def TERMINO_ARITMETICO_PRIMA():
    if is_OPMULDIV(complex_actual):
        compara(complex_actual.Token)
        if FACTOR_ARIMETICO():
            if TERMINO_ARITMETICO_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def FACTOR_ARIMETICO():
    if verifica_terminal('('):
        compara('(')
        if EXPRESION_ARITMETICA():
            compara(')')
            return True
        else:
            return False
    elif OPERANDO():
        return True
    else:
        return False

def OPERANDO():
    if verifica_terminal('NUM') or verifica_terminal('NUMF') or verifica_terminal('CONST_CHAR') or verifica_terminal('CONST_STRING') or verifica_terminal('TRUE') or verifica_terminal('FALSE'):
        compara(complex_actual.Token)
        return True
    elif verifica_terminal('('):
        compara('(')
        if EXPRESION_ARITMETICA():
            compara(')')
            return True
    elif DESTINO() or INVOCAR_FUNCION():
        return True
    else:
        return False

def INVOCAR_FUNCION():
    if verifica_terminal('CALL'):
        compara(TOKENS['CALL'])
        compara(TOKENS['ID'])
        compara('(')
        if ACTUALES():
            compara(')')
            return True
        else:
            return False
    else:
        return False

def ACTUALES():
    if ACTUAL():
        if ACTUALES_PRIMA():
            return True
        else:
            return False
    else:
        return False

def ACTUALES_PRIMA():
    if verifica_terminal(','):
        compara(',')
        if ACTUAL():
            if ACTUALES_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def ACTUAL():
    EXPRESION()
    return True

def DESTINO():
    if verifica_terminal('ID'):
        compara(TOKENS['ID'])
        if ELEMENTO_ARREGLO():
            return True
        else:
            return False
    else:
        return False

def ELEMENTO_ARREGLO():
    if verifica_terminal('['):
        compara('[')
        if EXPRESION():
            compara(']')
            return True
        else:
            return False
    else:
        return True

def verifica_terminal(token):
    if complex_actual:
        if len(token) == 1 and ord(token) < 256:
            return complex_actual.Token == ord(token)
        else:
            return complex_actual.Token == TOKENS[token]
    else:
        return False

codigo = ""
with open('codigo.txt','r') as f:
    codigo = f.read()

ln = 1
for linea in codigo.split('\n'):
    print("{}: {}".format(ln, linea))
    ln += 1
lex = Lexico(codigo)
complex_actual = siguiente_componente_lexico()
if not EXPRESION():
    print("Ln# {}: Error Sintactico: Se esperaba una expresion.".format(lex.num_linea))
else:
    print("Compilacion exitosa!")
