from .Item import Item, TipoItem
import string

simbolos_nao_terminais = string.ascii_uppercase + "'"
simbolos_terminais = string.ascii_lowercase + string.digits + "!#%()*+,.-/:;<=>?@[\]^_`{}~"


class GLC(Item):

    def __init__(self, nome):
        super(GLC, self).__init__(TipoItem.GLC, nome)
        self.__producoes = {} # dicionario de producoes
        self.__nao_terminais_a_direita = set() # conjunto de nao terminais que aparecem a direita de ->
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
        tmp_nao_terminais_a_direita = set()
        tmp_nao_terminais_a_esquerda = set()
        tmp_terminais = set()

        for linha in texto:
            if linha:
                if not linha.find("->") == -1:
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
                                    if p in simbolos_nao_terminais:
                                        tmp_nao_terminais_a_direita.add(p)

                                    elif p in simbolos_terminais:
                                        tmp_terminais.add(p)

                                    elif p != "&":
                                        return (False, "Produção precisa ser um não terminal ou um terminal ou &")
                                
                                elif len(p) >= 2:
                                    lista_nao_terminais = set()
                                    lista_terminais = set()

                                    terminal = ""
                                    nao_terminal = ""
                                    for i in range(len(p)):
                                        if p[i] == "." and len(terminal) > 0:
                                            lista_terminais.add(terminal)
                                            terminal = ""

                                        elif p[i] in simbolos_terminais:
                                            terminal += p[i]
                                            if len(nao_terminal) > 0:
                                                lista_nao_terminais.add(nao_terminal)
                                                nao_terminal = ""

                                        elif p[i] in simbolos_nao_terminais:
                                            if p[i] == "'" and len(nao_terminal) > 0:
                                                nao_terminal += p[i]
                                            elif p[i] in string.ascii_uppercase:
                                                if len(nao_terminal) > 0:
                                                    lista_nao_terminais.add(nao_terminal)

                                                nao_terminal = p[i]
                                            
                                            if len(terminal) > 0:
                                                lista_terminais.add(terminal)
                                                terminal = ""
                                        
                                        elif p[i] == "&":
                                            return (False, "& não pode estar junto de outro simbolo")

                                        else:
                                            return (False, "Produção precisa ser um não terminal ou um terminal ou &")
                                    

                                    if len(nao_terminal) > 0:
                                        lista_nao_terminais.add(nao_terminal)

                                    if len(terminal) > 0:
                                        lista_terminais.add(terminal)

                                    for simbolo in lista_nao_terminais:
                                        tmp_nao_terminais_a_direita.add(simbolo)
                                    
                                    for simbolo in lista_terminais:
                                        tmp_terminais.add(simbolo)

                                    p = p.replace('.', '')

                                producoes.append(p)

                            tmp_producoes[chave] = producoes


                        else:
                            return (False, "Simbolo não terminal possui letra minuscula")

                    else:
                        return (False, "Simbolo -> encontrado mais de uma vez em uma linha.")
                
                else:
                    return (False, "Linha não possui simbolo ->.")

        for vn in tmp_nao_terminais_a_direita:
            if vn not in tmp_nao_terminais_a_esquerda:
                return (False, "Simbolo não terminal " + vn + " aparece depois de ->, mas não aparece antes de ->")

        self.__producoes = tmp_producoes
        self.__nao_terminais = tmp_nao_terminais_a_esquerda
        self.__nao_terminais_a_direita = tmp_nao_terminais_a_direita
        self.__terminais = tmp_terminais

        return (True, "")


    def adicionaProducao(self, producao, simbolo):
        if simbolo not in self.__producoes:
            self.__producoes[simbolo] = producao
        else:
            self.__producoes[simbolo].append(producao)
