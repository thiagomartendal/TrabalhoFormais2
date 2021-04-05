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
        self.__tem_epsilon = False
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

    def reconhecerErros(self, texto):
        texto = texto.replace(" ", "")
        linhas = texto.splitlines()
        cabecasProducao = []
        for i in range(len(linhas)):
            if "->" not in linhas[i]:
                return (False, (i+1), linhas[i], "A cabeça de produção não declara o copo com ->.")
            cabecaCorpo = linhas[i].split("->")
            if cabecaCorpo[0] == '':
                return (False, (i+1), linhas[i], "A cabeça da produção não foi definida.")
            cabecasProducao.append(cabecaCorpo[0])
            if cabecaCorpo[1] == '':
                return (False, (i+1), linhas[i], "O corpo da produção não foi definido.")
            corpo = cabecaCorpo[1].split("|")
            for pateCorpo in corpo:
                if pateCorpo == '':
                    return (False, (i+1), linhas[i], "O corpo da produção tem uma indefinição a esquerda ou a direita de |.")
        return (True, 0, "", "")

    # Gera a estrutura gramatica a partir do texto escrito pelo usuario
    def parse(self, texto):
        #if not texto:
            #self.__erro = True
        self.__simbolo_inicial = None
        self.__texto = texto.replace(" ", "")
        lista_de_linhas = self.__texto.splitlines()
        return self.estruturaGramatica(lista_de_linhas)

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
                                return (False, linhas.index(linha)+1, linha, "Não pode possuir simbolos antes de -> iguais.") # Não pode possuir simbolos antes de -> iguais
                            chave_anterior = chave

                            if (linhas.index(linha) == 0):
                                self.setSimboloInicial(chave)

                            if (linhas.index(linha) == 1) and self.__simbolo_inicial[-1:] == '0' and self.__simbolo_inicial[:-1] != chave:
                                return (False, (linhas.index(linha)+1), linha, "Caso o símbolo inicial tenha 0 no final, o próximo simbolo tem que ser igual ao símbolo inicial menos o 0.")
                                # Caso simbolo inicial tenha 0 no final, proximo simbolo tem que ser igual ao simbolo inicial menos o 0

                            producoes = []
                            prod = li[1].split("|") # separa as producoes

                            if (linhas.index(linha) == 0):
                                primeira_producao = prod

                            if (linhas.index(linha) == 1 and self.__tem_epsilon and self.__simbolo_inicial[-1:] == '0'):
                                if primeira_producao[:-1] != prod:
                                    return (False, (linhas.index(linha)+1), linha, "Quando houver simbolo inicial com 0, a produção da primeira linha tem que ser igual a segunda sem o epsilon.")
                                    # Quando houver simbolo inicial com 0, a produção da primeira linha tem que ser igual a segunda sem o epsilon

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
                                                return (False, (linhas.index(linha)+1), linha, "O corpo da produção possui epsilon e não é inicial.") # possui epsilon e nao eh inicial
                                                # Não pode possuir epsilon fora da primeira linha

                                    else:
                                        return (False, linhas.index(linha)+1, linha, "Quando o símbolo for único, não deve possuir símbolo que não é & ou terminal.")
                                        # Quando simbolo for unico, não pode possuir simbolo que não é & ou terminal ou numero

                                if len(p) >= 2:
                                    terminal = p[0]
                                    nao_terminal = p[1:]

                                    if (nao_terminal == self.__simbolo_inicial and self.__tem_epsilon):
                                        return (False, linhas.index(linha)+1, linha, "Quando possuir epsilon, não pode haver produção que retorna para simbolo inicial.")
                                        # Quando possuir epsilon, não pode haver produção que retorna para simbolo inicial

                                    if self.__simbolo_inicial[-1:] == '0' and nao_terminal == self.__simbolo_inicial[:-1]:
                                        volta_inicio = True

                                    if (terminal.islower() or self.is_int(terminal)) and nao_terminal.isupper():
                                        self.__t.add(terminal)
                                        self.__n.add(nao_terminal)
                                        producoes.append(p)

                                    else:
                                        return (False, linhas.index(linha)+1, linha, "O terminal possui letra maiuscula ou não terminal possui letra minuscula")
                                        # terminal possui letra maiuscula ou não terminal possui letra minuscula

                            tmp_producoes[chave] = producoes

                        else:
                            return (False, (linhas.index(linha)+1), linha, "O símbolo "+li[0]+" antes de -> não pode ter letras minusculas.") # Simbolo nao eh maiuscula
                            # Simbolo antes de -> não pode ter letras minusculas

                    else:
                        return (False, (linhas.index(linha)+1), linha, "Sem símbolo a esquerda ou direita de ->.") # Sem simbolo a esquerda ou direita de ->

                else:
                    return (False, (linhas.index(linha)+1), linha, "Sem símbolo ->.") # Sem simbolo ->

        if (not volta_inicio) and self.__simbolo_inicial[-1:] == '0':
            return (False, 0, "", "Existe uma cabeça de produção S', mas não existe S. Portanto, S' não precisa existir.")

        for n in self.__n:
            if n not in tmp_producoes:
                return (False, 0, "", "A gramática possui símbolo não terminal que não é chamado em nenhuma produção a direita.")
                # Possui simbolo não terminal que não é chamado em nenhuma produção a direita

        self.__producoes = tmp_producoes
        return (True, 0, "", "")


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
