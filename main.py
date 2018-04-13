from lexico import Lexico
from simbolo import CONST_TOKENS
codigo = """<=
bool
>=
    <>cont
    >c
    > =
    int
    < cont >=="""
lex = Lexico(codigo)
#lex.mostrar_tabla_simbolos()
while True:
    s = lex.siguiente_componente_lexico()
    if s:
        
        print("Lexema: {}".format(s.Lexema).ljust(20),end="")
        print("Token: {} ({})".format(s.Token, CONST_TOKENS[s.Token]).rjust(15))
    else:
        break
