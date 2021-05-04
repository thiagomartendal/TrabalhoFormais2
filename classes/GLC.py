from .Item import Item, TipoItem
# from Item import Item, TipoItem # Usar este quando executar testeFatoracao.py
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

    def getTextoFormacao(self):
        txt = ""
        i = 0
        for NT in self.__nao_terminais:
            txt += NT
            if i < (len(self.__nao_terminais)-1):
                txt += ","
            i += 1
        txt += "\n"
        j = 0
        for T in self.__terminais:
            txt += T
            if j < (len(self.__terminais)-1):
                txt += ","
            j += 1
        txt += "\n"
        dicionario = self.getProducoes().items()
        for cabeca, corpo in dicionario:
            txt += cabeca+"->"
            k = 0
            for c in corpo:
                txt += c
                if k < (len(corpo)-1):
                    txt += "|"
                k += 1
            txt += "\n"
        return txt


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
            self.__nao_terminais.add(simbolo)
        else:
            self.__producoes[simbolo] += producao

    # Método que inicia a fatoração
    # Primeiro deve-se procurar determinismos diretos, pois eles aparecem primeiro em algumas gramáticas,
    # embora se deva verificar qual não-determinismo ocorre primeiro
    def fatorar(self):
        dicionario = self.getProducoes().items()
        # Deve-se achar uma maneira de verificar quando começar com o determinismo direto
        l3 = self.__procuraDireto() # Algumas gramáticas devem primeiro verificar o determinismo direto
        self.__removerDireto(l3)
        l1 = self.__procuraIndireto()
        if len(l1) > 0:
            self.__derivacoesSucessivas(l1)
        l2 = self.__procuraDireto()
        self.__removerDireto(l2)
        l4 = self.__procuraEpsilon()
        if len(l4) > 0:
            self.__derivacoesSucessivas(l4)
            l5 = self.__procuraDireto()
            self.__removerDireto(l5)

    # Procura não-determinismos indiretos
    def __procuraIndireto(self):
        dicionario = self.getProducoes().items()
        i = 0
        l = []
        for cabeca, corpo in dicionario:
            if len(corpo) > 1:
                k = 0
                for c in corpo:
                    if c[0] in self.__nao_terminais:
                        k += 1
                if k > 1:
                    for c in corpo:
                        if len(c) > 1:
                            if c[0] in self.__nao_terminais:
                                if (i, c) not in l:
                                    l.append((i, c))
            i += 1
        l = self.__procuraIndireto1(l, dicionario)
        return l

    # Procura não-determinismos em produções que tem um terminal em comum com uma produção anterior que a chama
    def __procuraIndireto1(self, l, dicionario):
        for cabeca1, corpo1 in dicionario:
            for c1 in corpo1:
                if c1[0] in self.__terminais:
                    j = 0
                    for cabeca2, corpo2 in dicionario:
                        if corpo1 != corpo2:
                            for c2 in corpo2:
                                if len(c2) > 1:
                                    if c2[0] in self.__nao_terminais:
                                        for cabeca3, corpo3 in dicionario:
                                            if c2[0] == cabeca3:
                                                for c3 in corpo3:
                                                    if c1[0] == c3[0]:
                                                        if (j, c2) not in l:
                                                            l.append((j, c2))
                        j += 1
        return l

    # Procura não-determinismos indiretos em produções que contém épsilon
    def __procuraEpsilon(self):
        dicionario = self.getProducoes().items()
        l = []
        j = 0
        for cabeca, corpo in dicionario:
            for c in corpo:
                if len(c) > 1:
                    cabecaProd = ""
                    aceito = False
                    for i in range(len(c)):
                        cabecaProd += c[i]
                        if (i < len(c)-1) and (c[i+1] != "'"):
                            if cabecaProd in self.__nao_terminais:
                                aceito = True
                                break
                    if aceito:
                        for cabeca1, corpo1 in dicionario:
                            if cabecaProd == cabeca1:
                                if '&' in corpo1:
                                    l.append((j, c))
            j += 1
        return l

    # Procura não-determinismos diretos
    def __procuraDireto(self):
        dicionario = self.getProducoes().items()
        i = 0
        # l = []
        l = {}
        for cabeca, corpo in dicionario:
            if len(corpo) > 1:
                for C1 in corpo:
                    for C2 in corpo:
                        if C1 != C2:
                            if C1[0] == C2[0]:
                                l.update({(i, C1[0]): []})
                                l[(i, C1[0])].append(C2[1:])
                                l[(i, C1[0])].append(C1[1:])
            i += 1
        return l

    # Realiza as derivações sucessivas de gramáticas com não-determinismo indireto
    def __derivacoesSucessivas(self, indireto):
        dicionario = self.getProducoes().items()
        for tupla in indireto:
            producao = tupla[1]
            cabecaProd = ""
            for i in range(len(producao)):
                cabecaProd += producao[i]
                if (i < len(producao)-1) and (producao[i+1] != "'"):
                    if cabecaProd in self.__nao_terminais:
                        break
            for k, v in dicionario:
                if k == cabecaProd:
                    for p in v:
                        str = p
                        for i in range(1, len(producao)):
                            str += producao[i]
                        # print(tupla, str)
                        if '&' not in str:
                            self.__trocarProducao(tupla, str)

    # Realiza a troca de produções para as derivações sucessivas
    def __trocarProducao(self, tupla, producao):
        dicionario = self.getProducoes().items()
        txt = ""
        i = 0
        for cabeca, corpo in dicionario:
            if i == tupla[0]:
                if tupla[1] in corpo:
                    corpo.remove(tupla[1])
                # print(producao)
                corpo.append(producao)
            i += 1

    # Remove o não-determinismo direto
    def __removerDireto(self, direto):
        dicionario = self.getProducoes().items()
        n = []
        for k, v in direto:
            i = 0
            for k1, v1 in dicionario:
                if i == k:
                    for p in direto[(k, v)]:
                        v1.remove(v+p)
                    cabeca = k1
                    cabeca += "'"
                    if (v+cabeca) in v1:
                        cabeca += "'"
                        v1.append(v+cabeca)
                    else:
                        v1.append(v+cabeca)
                        for j in range(len(direto[(k, v)])):
                            if direto[(k, v)][j] == '':
                                direto[(k, v)][j] = '&'
                            # else:
                                # direto[(k, v)][j] = direto[(k, v)][j][1:]
                    self.adicionaProducao(direto[(k, v)], cabeca)
                    break
                i += 1

    def calculaFirst(self):
        firsts = []
        first = set()
        temp = []
        for i in self.__nao_terminais:
            temp.append(i)
            first = (self.First(i))
            temp.append(first)
            firsts.append(temp)
            temp = []
        # print(firsts)
        return firsts

    def First(self, simbolo):
        first = set()
        if(simbolo in self.__terminais):
            first.add(simbolo)
            return first
        else:
            producoes = self.__producoes.get(simbolo)
            # print("produções: {prod}".format(prod = producoes))
            for i in producoes:
                # corpo_producao = i.split()
                # print(corpo_producao[0][0])
                if(i[0] in self.__terminais or i == '&'):
                    first.add(i[0])
                elif(i[0] in self.__nao_terminais):
                    # print("simbolo atual: {simb}".format(simb = i))
                    first_nao_terminal = self.First(i[0])
                    if('&' in first_nao_terminal):
                        for x in first_nao_terminal:
                            first.add(x)
                        # print(first)
                        if(len(i) > 1):
                            for w in range(1, len(i)):
                                if('&' in first_nao_terminal):
                                    first_nao_terminal = self.First(i[w])
                                    for x in first_nao_terminal:
                                        first.add(x)
                    for k in first_nao_terminal:
                        first.add(k)
                else:
                    print("simbolo não pertence a GLC")
        # print("first: {a}".format(a = first))
        return first
