from .Item import Item, TipoItem
from .Automato import Automato
from .Estado import Estado
from .Transicao import Transicao
from string import ascii_uppercase

class Gramatica(Item):

    def __init__(self, nome):
        super(Gramatica, self).__init__(TipoItem.GR, nome)
        self.__producoes = {}  # Dicionario de producoes
        self.__texto = None
        self.__simbolo_inicial = None
        self.__n = set() #  conjunto de variáveis não-terminais
        self.__t = set() # conjunto de variáveis terminais

    # Adiciona uma nova producao ao dicionario
    def adicionaProducao(self, simbolo, producao):
        self.__producoes[simbolo] = producao

    # Retorna o dicionario inteiro
    def getProducoes(self):
        return self.__producoes

    # Modifica o simbolo inicial da gramatica regular
    def setSimboloInicial(self, simbolo):
        self.__simbolo_inicial = simbolo

    # Gera a estrutura gramatica a partir do texto escrito pelo usuario
    def parse(self, texto):
        #if not texto:
            #self.__erro = True
        self.__simbolo_inicial = None
        self.__texto = texto.replace(" ", "")
        lista_de_linhas = self.__texto.splitlines()
        self.estruturaGramatica(lista_de_linhas)

    # Verifica se a estrutura gramatica esta certa e gera ela
    def estruturaGramatica(self, linhas):
        tem_epsilon = False

        tmp_producoes = {}

        for linha in linhas:
            if len(linha) > 0:
                if not linha.find("->") == -1:
                    li = linha.split("->") # Separa entre o lado esquerdo e direito do "->"
                    if (len(li) == 2):
                        if len(li[0]) == 1 and li[0].isupper():
                            chave = li[0]
                            if (linhas.index(linha) == 0):
                                self.setSimboloInicial(li[0])
                            
                            producoes = []
                            prod = li[1].split("|") # separa as producoes

                            for p in prod:
                                if len(p) == 1:
                                    if p.islower() or p == "&" or self.is_int(p):
                                        producoes.append(p)
                                    
                                        if p != "&":
                                            self.__t.add(p)

                                        if p == "&":
                                            if linhas.index(linha) == 0:
                                                tem_epsilon = True
                                            else:
                                                return
                                    
                                    else:
                                        return
                                
                                if len(p) == 2:
                                    terminal = p[0]
                                    nao_terminal = p[1]

                                    if (nao_terminal == self.__simbolo_inicial and tem_epsilon):
                                        return

                                    if (terminal.islower() or self.is_int(terminal)) and nao_terminal.isupper():
                                        self.__t.add(terminal)
                                        self.__n.add(nao_terminal)
                                        producoes.append(p)

                                    else:
                                        return

                            tmp_producoes[chave] = producoes

                        else:
                            return # Simbolo antes de -> tem mais de uma letra ou nao eh maiuscula
                    
                    else:
                        return # Sem simbolo a esquerda ou direita de ->
                
                else:
                    return # Sem simbolo a esquerda ou direita de ->
        
        for n in self.__n:
            if n not in tmp_producoes:
                return

        self.__producoes = tmp_producoes


    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def conversaoEmAFND(self):
        af = Automato(self.get_nome() + " (convertido para AF)")

        estado_final = Estado(self.novoEstado(), 2)

        for estado, lista in self.__producoes.items():
            estado_partida = None
            if estado == self.__simbolo_inicial:
                estado_partida = Estado(estado, 0)
            else:
                estado_partida = Estado(estado, 1)
            
            af.addEstado(estado_partida)

            for p in lista:
                if len(p) == 1:
                    af.addTransicao(Transicao(estado_partida, p, estado_final))
                else:
                    if p[1] == self.__simbolo_inicial:
                        af.addTransicao(Transicao(estado_partida, p[0], Estado(p[1], 0)))
                    else:
                        af.addTransicao(Transicao(estado_partida, p[0], Estado(p[1], 1)))

        af.addEstado(estado_final)

        for t in self.__t:
            af.addSimbolo(t)

    
    def novoEstado(self):
        novo_estado = None
        for letra in ascii_uppercase:
            if letra not in self.__producoes:
                novo_estado = letra
                break

        return novo_estado
                