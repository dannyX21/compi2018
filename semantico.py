from pila import Pila

class Semantico():
    def __init__(self):
        self.tmp_index = 0
        self.pila = Pila()
        self.codigo = []
        self.archivo = 'codigo.3ac'

    def gen_temp(self):
        tmp = "_tmp" + str(self.tmp_index)
        self.tmp_index += 1
        return tmp

    def push(self, item):
        self.pila.push(item)

    def pop(self):
        return self.pila.pop()

    def agregar_linea_3ac(self, linea):
        self.codigo.append(linea)

    def generar_archivo_3ac(self):
        with open(self.archivo, 'w') as f:
            for line in self.codigo:
                f.write('{}\n'.format(line))

