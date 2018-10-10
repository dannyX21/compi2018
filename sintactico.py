from lexico import Lexico
from simbolo import CONST_TOKENS, TOKENS, TIPO_DATO, ZONA_DE_CODIGO

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
    elif token_esperado <= 255:
        print("ln# {}: Se esperaba: '{}'".format(num_linea(),chr(token_esperado)))
    else:
        print("ln# {}: Se esperaba: '{}'".format(num_linea(),
        CONST_TOKENS[token_esperado]))

def PROGRAMA():
    if DEFINIR_VARIABLES():
        if DEFINIR_FUNCIONES():
            if PRINCIPAL():
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def PRINCIPAL():
    if verifica_terminal('MAIN'):
        compara(TOKENS['MAIN'])
        if not lex.fin_definicion_variables_globales:
            lex.fin_definicion_palabras_reservadas = len(lex.tablaSimb)

        lex.zona_de_codigo = ZONA_DE_CODIGO['CUERPO_PRINCIPAL']
        compara('(')
        if PARAMETROS_FORMALES():
            compara(')')
            if BLOQUE():
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def DEFINIR_VARIABLES():
    VARIABLES()
    return True

def VARIABLES():
    if VARIABLE():
        if VARIABLES_PRIMA():
            return True
        else:
            return False
    else:
        return False

def VARIABLES_PRIMA():
    if VARIABLE():
        if VARIABLES_PRIMA():
            return True
        else:
            return False
    else:
        return True

def VARIABLE():
    if TIPO():
        if IDENTIFICADORES():
            compara(';')
            return True
        else:
            return False
    else:
        return False

def TIPO():
    if any(map(lambda x: verifica_terminal(x), ['INT', 'BOOL', 'FLOAT', 'CHAR', 'STRING', 'VOID'])):
        lex.tipo_de_dato_actual = TIPO_DATO[complex_actual.Lexema]
        compara(complex_actual.Token)
        return True
    else:
        return False

def IDENTIFICADORES():
    if IDENTIFICADOR():
        if IDENTIFICADORES_PRIMA():
            return True
        else:
            return False
    else:
        return False

def IDENTIFICADORES_PRIMA():
    if verifica_terminal(','):
        compara(',')
        if IDENTIFICADOR():
            if IDENTIFICADORES_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def IDENTIFICADOR():
    if verifica_terminal('ID'):
        compara(TOKENS['ID'])
        if ES_ARREGLO():
            return True
        else:
            return False
    else:
        return False

def ES_ARREGLO():
    if verifica_terminal('['):
        compara('[')
        compara(TOKENS['NUM'])
        compara(']')
    return True

def DEFINIR_FUNCIONES():
    FUNCIONES()
    return True

def FUNCIONES():
    if FUNCION():
        if FUNCIONES_PRIMA():
            return True
        else:
            return False
    else:
        return False

def FUNCIONES_PRIMA():
    if FUNCION():
        if FUNCIONES_PRIMA():
            return True
        else:
            return False
    else:
        return True

def FUNCION():
    if verifica_terminal('FUNCTION'):
        compara(TOKENS['FUNCTION'])
        if not lex.fin_definicion_variables_globales:
            lex.fin_definicion_variables_globales = len(lex.tablaSimb)
        if TIPO():
            compara(TOKENS['ID'])
            compara('(')
            lex.zona_de_codigo = ZONA_DE_CODIGO['DEF_VARIABLES_LOCALES']
            lex.inicio_definicion_variables_locales = len(lex.tablaSimb)            
            if PARAMETROS_FORMALES():
                compara(')')
                if DEFINIR_VARIABLES():
                    lex.zona_de_codigo = ZONA_DE_CODIGO['CUERPO_FUNCION_LOCAL']
                    lex.fin_definicion_variables_locales = len(lex.tablaSimb)
                    if CUERPO_FUNCION():
                        lex.zona_de_codigo = ZONA_DE_CODIGO['DEF_VARIABLES_GLOBALES']
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def PARAMETROS_FORMALES():
    PARAMETROS()
    return True

def PARAMETROS():
    if PARAMETRO():
        if PARAMETROS_PRIMA():
            return True
        else:
            return False
    else:
        return False

def PARAMETROS_PRIMA():
    if verifica_terminal(','):
        compara(',')
        if PARAMETRO():
            if PARAMETROS_PRIMA():
                return True
            else:
                return False
        else:
            return False
    else:
        return True

def PARAMETRO():
    if TIPO():
        compara(TOKENS['ID'])
        return True
    else:
        return False

def CUERPO_FUNCION():
    if BLOQUE():
        return True
    else:
        return False

def BLOQUE():
    if verifica_terminal('{'):
        compara('{')
        if ORDENES():
            compara('}')
            return True
        else:
            return False
    else:
        return False

def ORDENES():
    if ORDEN():
        if ORDENES_PRIMA():
            return True
        else:
            return False
    else:
        return False

def ORDENES_PRIMA():
    if ORDEN():
        if ORDENES_PRIMA():
            return True
        else:
            return False
    else:
        return True

def ORDEN():    #Debe aceptar 'E'?!?!?!
    if ASIGNACION() or DECISION() or ITERACION() or ENTRADA_SALIDA() or BLOQUE() or RETORNO():
        return True
    else:
        return False

def ASIGNACION():
    if DESTINO():
        compara(TOKENS['IGU'])
        if FUENTE():
            compara(';')
            return True
        else:
            return False
    else:
        return False

def FUENTE():
    if EXPRESION():
        return True
    else:
        return False

def DECISION():
    if verifica_terminal('IF'):
        compara(TOKENS['IF'])
        compara('(')
        if EXPRESION():
            compara(')')
            compara(TOKENS['THEN'])
            if ORDEN():
                if TIENE_ELSE():
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def TIENE_ELSE():
    if verifica_terminal('ELSE'):
        compara(TOKENS['ELSE'])
        if ORDEN():
            return True
        else:
            return False
    else:
        return True

def ITERACION():
    if verifica_terminal('FOR'):
        compara(TOKENS['FOR'])
        compara(TOKENS['ID'])
        compara(TOKENS['IGU'])
        compara(TOKENS['NUM'])
        compara(TOKENS['TO'])
        compara(TOKENS['NUM'])
        if ORDEN():
            return True
        else:
            return False
    elif verifica_terminal('WHILE'):
        compara(TOKENS['WHILE'])
        compara('(')
        if EXPRESION_LOGICA():
            compara(')')
            compara(TOKENS['DO'])
            if ORDEN():
                return True
            else:
                return False
        else:
            return False
    elif verifica_terminal('DO'):
        compara(TOKENS['DO'])
        if ORDEN():
            compara(TOKENS['WHILE'])
            compara('(')
            if EXPRESION_LOGICA():
                compara(')')
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def ENTRADA_SALIDA():
    if verifica_terminal('READ'):
        compara(TOKENS['READ'])
        compara('(')
        if DESTINO():
            compara(')')
            compara(';')
            return True
        else:
            return False
    elif verifica_terminal('WRITE'):
        compara(TOKENS['WRITE'])
        compara('(')
        if EXPRESION():
            compara(')')
            compara(';')
            return True
        else:
            return False
    else:
        return False

def RETORNO():
    if verifica_terminal('RETURN'):
        compara(TOKENS['RETURN'])
        if EXPRESION():
            compara(';')
            return True
        else:
            return False
    else:
        return False

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
if not PROGRAMA():
    print("Ln# {}: Se encontraron errores.".format(lex.num_linea))
else:
    print("\nCompilacion exitosa!")

print("\nTabla de Simbolos:")
print("Token\tTipo\tLexema")
for complex in lex.tablaSimb:
    print("{}\t{}\t{}".format(CONST_TOKENS[complex.Token], complex.Tipo, complex.Lexema))

print("\n")
if lex.error.total > 0:
    print("Se encontraron: {} errores.".format(lex.error.total))
    for e in lex.error.errores:
        print(e)


