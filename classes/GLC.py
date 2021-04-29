from Item import Item, TipoItem
import string

simbolos_nao_terminais = string.ascii_uppercase + "'"
simbolos_terminais = string.ascii_lowercase + string.digits + "!#%()*+,.-/:;<=>?@[\]^_`{}~"


class GLC(Item):

    def __init__(self, nome):
        super(GLC, self).__init__(TipoItem.GLC, nome)
        self.__producoes = {} # dicionario de producoes
        self.__nao_terminais = set() # conjunto de nao terminais que aparecem a esquerda de ->
        self.__terminais = set()
        self.__simbolo_inicial = None


    def setSimboloInicial(self, simbolo):
        self.__simbolo_inicial = simbolo

    def getSimboloInicial(self):
        return self.__simbolo_inicial

    def getProducoes(self):
        return self.__producoes


    def parse(self, texto_glc):
        texto = texto_glc.replace(" ","")
        texto = texto.splitlines()
        return self.verificaEstruturaGLC(texto)


    def verificaEstruturaGLC(self, texto_glc):
        texto = texto_glc
        simbolo_inicial_definido = False
        tmp_producoes = {}
        tmp_nao_terminais = set()
        tmp_nao_terminais_a_esquerda = set()
        tmp_terminais = set()
        k = 0

        for linha in texto:
            if linha:
                if k == 0:
                    for simbolo in linha.split(","):
                        for simb in simbolo:
                            if simb not in simbolos_nao_terminais:
                                return (False, "Simbolo " + simb + " não pertence aos não terminais")
                        tmp_nao_terminais.add(simbolo)
                    k += 1

                elif k == 1:
                    for simbolo in linha.split(","):
                        for simb in simbolo:
                            if simb not in simbolos_terminais:
                                return (False, "Simbolo " + simb + " não pertence aos terminais")
                        tmp_terminais.add(simbolo)
                    k += 1

                elif not linha.find("->") == -1:
                    if k == 2:
                        lista_nao_terminais = list(tmp_nao_terminais)
                        lista_terminais = list(tmp_terminais)
                        k += 1
                        lista_nao_terminais.sort(key = len, reverse = True)
                        lista_terminais.sort(key = len, reverse = True)

                    li = linha.split("->")
                    if len(li) <= 2:
                        if li[0].isupper():
                            chave = li[0]
                            tmp_nao_terminais_a_esquerda.add(chave)

                            if not simbolo_inicial_definido:
                                self.__simbolo_inicial = chave
                                simbolo_inicial_definido = True
                            
                            producoes = []
                            prod = li[1].split("|") # separa as producoes

                            for p in prod:
                                if len(p) == 1:
                                    if not (p in tmp_nao_terminais or p in tmp_terminais or p == "&"):
                                        return (False, "Simbolo " + p + " precisa ou estar definido no não terminais ou nos terminais ou ser um &.")
                                
                                elif len(p) >= 2:
                                    

                                    terminal = ""
                                    nao_terminal = ""
                                    for i in range(len(p)):
                                        if p[i] in simbolos_nao_terminais:
                                            nao_terminal += p[i]
                                        elif p[i] in simbolos_terminais:
                                            terminal += p[i]
                                        elif p[i] != "&":
                                            return (False, "Simbolo " + p[i] + " precisa ser um não terminal, terminal ou &.")

                                    for simbolo in lista_nao_terminais:
                                        if simbolo in nao_terminal:
                                            nao_terminal = nao_terminal.replace(simbolo, "")

                                    for simbolo in lista_terminais:
                                        if simbolo in terminal:
                                            terminal = terminal.replace(simbolo, "")   

                                    if len(terminal) > 0 or len(nao_terminal) > 0:
                                        return (False, p + " possui algum simbolo que não foi definido como terminal ou não terminal ou &")

                                producoes.append(p)

                            tmp_producoes[chave] = producoes

                        else:
                            return (False, "Simbolo não terminal possui letra minuscula.")

                    else:
                        return (False, "Simbolo -> encontrado mais de uma vez em uma linha.")
                
                else:
                    return (False, "Linha não possui simbolo ->.")

        for vn in tmp_nao_terminais_a_esquerda:
            if vn not in tmp_nao_terminais:
                return (False, "Simbolo não terminal " + vn + " aparece na produção, mas não foi definido na primeira linha.")

        self.__producoes = tmp_producoes
        self.__nao_terminais = tmp_nao_terminais
        self.__terminais = tmp_terminais
        #print(self.__nao_terminais, self.__terminais)
        #print(self.__producoes)

        return (True, "")


    def adicionaProducao(self, producao, simbolo):
        if simbolo not in self.__producoes:
            self.__producoes[simbolo] = producao
        else:
            self.__producoes[simbolo].append(producao)
