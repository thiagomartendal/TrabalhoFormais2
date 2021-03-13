from .Item import Item, TipoItem
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

    def getSimboloInicial(self):
        return self.__simbolo_inicial

    def getT(self):
        return self.__t
    
    def getN(self):
        return self.__n
    
    def setT(self, t):
        self.__t = t
    
    def setN(self, n):
        self.__n = n

    def setProducoes(self, prod):
        self.__producoes = prod

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
        self.__tem_epsilon = False

        tmp_producoes = {}
        primeira_producao = []
        chave_anterior = None
        volta_inicio = False

        for linha in linhas:
            if len(linha) > 0:
                if not linha.find("->") == -1:
                    li = linha.split("->") # Separa entre o lado esquerdo e direito do "->"
                    if (len(li) == 2):
                        if li[0].isupper():
                            chave = li[0]
                            if (chave == chave_anterior):
                                return # chaves iguais
                            chave_anterior = chave

                            if (linhas.index(linha) == 0):
                                self.setSimboloInicial(chave)

                            if (linhas.index(linha) == 1) and self.__simbolo_inicial[-1:] == '0' and self.__simbolo_inicial[:-1] != chave:
                                return # S' tem que ter S na proxima linha
                            
                            producoes = []
                            prod = li[1].split("|") # separa as producoes

                            if (linhas.index(linha) == 0):
                                primeira_producao = prod
                            
                            if (linhas.index(linha) == 1 and self.__tem_epsilon and self.__simbolo_inicial[-1:] == '0'):
                                if primeira_producao[:-1] != prod:
                                    return # S' e S nao sao iguais

                            for p in prod:
                                if len(p) == 1:
                                    if p.islower() or p == "&" or self.is_int(p):
                                        producoes.append(p)
                                    
                                        if p != "&":
                                            self.__t.add(p)

                                        if p == "&":
                                            if linhas.index(linha) == 0:
                                                self.__tem_epsilon = True
                                            else:
                                                return # possui epsilon e nao eh inicial
                                    
                                    else:
                                        return
                                
                                if len(p) >= 2:
                                    terminal = p[0]
                                    nao_terminal = p[1:]

                                    if (nao_terminal == self.__simbolo_inicial and self.__tem_epsilon):
                                        return

                                    if self.__simbolo_inicial[-1:] == '0' and nao_terminal == self.__simbolo_inicial[:-1]:
                                        volta_inicio = True

                                    if (terminal.islower() or self.is_int(terminal)) and nao_terminal.isupper():
                                        self.__t.add(terminal)
                                        self.__n.add(nao_terminal)
                                        producoes.append(p)

                                    else:
                                        return

                            tmp_producoes[chave] = producoes

                        else:
                            return # Simbolo nao eh maiuscula
                    
                    else:
                        return # Sem simbolo a esquerda ou direita de ->
                
                else:
                    return # Sem simbolo a esquerda ou direita de ->
        
        if (not volta_inicio) and self.__simbolo_inicial[-1:] == '0':
            return

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
        from .Automato import Automato
        tmp_producoes = self.__producoes
        simbolo_inicial = self.__simbolo_inicial

        if len(self.__simbolo_inicial) == 2:
            tmp_producoes[self.__simbolo_inicial[0]] = tmp_producoes[self.__simbolo_inicial]
            tmp_producoes.pop(self.__simbolo_inicial)
            simbolo_inicial = self.__simbolo_inicial[0]

        af = Automato(self.get_nome() + " (convertido para AF)")

        estado_final = Estado(self.novoEstado(), 2)

        listat = []
        for t in self.__t:
            listat.append(t)
        listat.sort()

        for estado in tmp_producoes.keys():
            estado_partida = None
            if estado == simbolo_inicial:
                if self.__tem_epsilon:
                    estado_partida = Estado(estado, 3)
                else:
                    estado_partida = Estado(estado, 0)
            else:
                estado_partida = Estado(estado, 1)
            
            af.addEstado(estado_partida)

        af.addEstado(estado_final)

        for estado, lista in tmp_producoes.items():
            estado_partida = af.procurarEstado(estado)

            for t in listat:
                transicao = Transicao(estado_partida, t, [])
                for p in lista:
                    if p == "&":
                        continue
                    if len(p) == 1 and p == t:
                        transicao.addEstadoChegada(estado_final)
                    elif len(p) == 2 and p[0] == t:
                        estad = af.procurarEstado(p[1])
                        transicao.addEstadoChegada(estad)
                if len(transicao.getEstadosChegada()) != 0:
                    af.addTransicao(transicao)
        

        for t in listat:
            af.addSimbolo(t)

        return af

    
    def novoEstado(self):
        novo_estado = None
        for letra in ascii_uppercase:
            if letra not in self.__producoes:
                novo_estado = letra
                break

        return novo_estado
                