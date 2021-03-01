from .Item import Item, TipoItem

class Gramatica(Item):

    def __init__(self, nome):
        super(Gramatica, self).__init__(TipoItem.GR, nome)
        self.__producoes = {}  # Dicionario de producoes
        self.__texto = None
        self.__simbolo_inicial = None

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
        if not texto:
            print("Texto vazio")
            return
        self.__producoes.clear()
        self.__texto = None
        self.__simbolo_inicial = None
        self.__texto = texto.replace(" ", "")
        lista_de_linhas = self.__texto.splitlines()
        self.estruturaGramatica(lista_de_linhas)

    # Verifica se a estrutura gramatica esta certa e gera ela
    def estruturaGramatica(self, linhas):
        tem_epsilon = False
        for linha in linhas:
            if len(linha) > 0:
                if not linha.find("->") == -1:
                    li = linha.split("->") # separa a producao entre o lado esquerdo e direito de ->
                    if (len(li) == 2):
                        if (linha.find("'") or len(li[0]) == 1) and li[0].isupper():
                            chave = li[0]
                            if (linhas.index(linha) == 0):
                                self.setSimboloInicial(li[0])

                            producoes = []
                            prod = li[1].split("|") # separa as producoes

                            if not li[1].find("&") == -1:
                                tem_epsilon = True

                            for p in prod:
                                if len(p) == 1:
                                    if (p.islower() or p == "&"):
                                        if (p == "&" and linha.index(linha) != 0):
                                            print("Producao possui epsilon e nao eh inicial")
                                            return
                                        producoes.append(p)

                                    else:
                                        print("Possui um simbolo maiusculo isolado a direita da producao")
                                        return

                                elif len(p) == 2:
                                    terminal = p[0]
                                    nao_terminal = p[1]

                                    if (not terminal.islower()) or (not nao_terminal.isupper()):
                                        print("Producao nao segue formato de terminal seguido de nao terminal")
                                        return

                                    if nao_terminal == self.__simbolo_inicial and tem_epsilon:
                                        print("Producao nao segue regras do epsilon")
                                        return

                                    producoes.append(p)

                                else:
                                    print("Possui simbolo vazio ou mais que duas letras")
                                    return

                            self.adicionaProducao(chave, producoes)


                        else:
                            print("Simbolo antes de -> tem mais de uma letra ou nao eh maiuscula")
                            return
                    else:
                        print("Sem simbolo a esquerda ou direita de ->")
                        return
                else:
                    print("Producao sem simbolo ->")
                    return
            else:
                print("Texto tem linha vazia")
                return
