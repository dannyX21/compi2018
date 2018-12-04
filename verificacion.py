
matriz_suma = [
    [1, 0, 3, 0, 0],
    [0, 0, 0, 0, 0],
    [3, 0 , 3, 0, 0],
    [0, 0, 0, 5, 5],
    [0, 0, 0, 5, 5]
]

matriz_or = [
    [False, False, False, False, False],
    [False, True, False, False, False],
    [False, False, False, False, False],
    [False, False, False, False, False],
    [False, False, False, False, False],
]

def verificar(operando1, operando2, operador):
    if operador == '+':
        return matriz_suma[operando1-1][operando2-1]
    elif operador == '-':
        pass
    elif operador == '|':
        return matriz_or[operando1-1][operando2-1]

