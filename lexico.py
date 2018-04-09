from simbolo import Simbolo, TOKENS
import json

palabras_reservadas = ['bool','call','char','do','else','float','for',
'function','if','int','main','read','return','string','then','to','void',
'while','write','false','true']  #Lista de Palabras reservadas

class Lexico:
    def __init__(self, codigo):             #Constructor del Analizador Lexico.
        self.codigo = " " + codigo + " "    #codigo fuente a compilar.
        self.tablaSimb = []                 #tabla de Simbolos
        self.index = 0                      #indice del caracter actual
        self.inicioLex = 1                  #inicio del lexema actual
        self.Lexema = ""                    #Ultimo lexema encontrado
        self.num_linea = 1                  #numero de linea del codigo fuente
        self.estado = 0                     #estado actual en los automatas.
        self.cargar_palabras_reservadas()   #Cargar las palabras reservadas en
                                            #la tabla de simbolos.

    def insertar_simbolo(self, simbolo):    #inserta un nuevo simbolor en la TS.
        if simbolo:
            self.tablaSimb.append(simbolo)
        else:
            raise ValueError("Se esperaba un simbolo")

    def cargar_palabras_reservadas(self):   #Carga las palabras reservadas en TS
        for p in palabras_reservadas:
            self.insertar_simbolo(Simbolo(p, TOKENS[p.upper()]))
# -*- coding: utf-8 -*-
    def mostrar_tabla_simbolos(self):       #muestra el contenido de la TS.
        for s in self.tablaSimb:
            print(s)

    def buscar_lexema(self, lexema):        #busca un lexema en la TS.
            simb = [s for s in self.tablaSimb if lexema == s.Lexema]
            return simb[0] if len(simb)>0 else None

    def tablaSimb2JSON(self):               #regresa el contenido de TS en JSON
        return json.dumps([obj.__dict__ for obj in self.tablaSimb])

    def siguiente_caracter(self):           #regresa el siguiente caracter del
        self.index += 1                     #codigo fuente.
        try:
            return self.codigo[self.index]
        except IndexError:
            return '\0'

    def saltar_caracter(self):              #ignora el caracter actual, por eje-
        self.index += 1                     #mplo: tabs, espacios, enters, etc.
        self.inicioLex = self.index

    def leer_lexema(self):                  #regresa la cadena que se encuentra
        self.Lexema = self.codigo[self.inicioLex:self.index + 1]
        self.inicioLex = 0                  #entre inicioLex y el index.
        self.estado = 0
        self.avanza_inicio_lexema()
        return self.Lexema

    def regresa_caracter(self):             #Representa el (*) en un estado de
        self.index -= 1                     #aceptacion.

    def avanza_inicio_lexema(self):         #mueve el incioLex un caracter hacia
        self.inicioLex = self.index + 1     #adelante

    def siguiente_componente_lexico(self):  #regresa el siguiente simbolo encon-
        while(True):                        #trado en el codigo fuente.
            if self.estado == 0:
                c = self.siguiente_caracter()
                if c ==' ' or c =='\t' or c == '\n':
                    self.avanza_inicio_lexema()
                    if c == '\t' or c == '\n':
                        self.num_linea += 1
                    self.avanza_inicio_lexema()
                elif c == '\0':
                    return None
                elif c == '<':
                    self.estado = 1
                elif c == '=':
                    self.estado = 5
                elif c == '>':
                    self.estado = 6
                else:
                    self.estado = self.fallo()
            elif self.estado == 1:
                c = self.siguiente_caracter()
                if c == '=':
                    self.estado = 2
                elif c == '>':
                    self.estado = 3
                else:
                    self.estado = 4
            elif self.estado == 2:
                self.leer_lexema()
                return(Simbolo(self.Lexema,TOKENS['MEI']))
            elif self.estado == 3:
                self.leer_lexema()
                return(Simbolo(self.Lexema,TOKENS['DIF']))
            elif self.estado == 4:
                self.regresa_caracter()
                self.leer_lexema()
                return(Simbolo(self.Lexema,TOKENS['MEN']))
            elif self.estado == 5:
                self.leer_lexema()
                return(Simbolo(self.Lexema,TOKENS['IGU']))
            elif self.estado == 6:
                c = self.siguiente_caracter()
                if c == '=':
                    self.estado = 7
                else:
                    self.estado = 8
            elif self.estado == 7:
                self.leer_lexema()
                return Simbolo(self.Lexema, TOKENS['MAI'])
            elif self.estado == 8:
                self.regresa_caracter()
                self.leer_lexema()
                return Simbolo(self.Lexema, TOKENS['MAY'])
            else:
                return None
