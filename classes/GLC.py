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

    #################################### Começa os Métodos de Recursão ####################################

    # Método que remove a recursão procurando primeiro a ocorrência de recursao indireta,
    # e depois a direta
    def removerRecursaoAEsquerda(self):
        dicionario = self.getProducoes().items()
        while True: # Executa até não ter mais recursões
            parar = False # Não deve parar até as duas procuras serem falsas e todas as ptoduções tiverem sido lidas
            producoesLidas = [] # Lista com as cabeças de produções lidas
            producoesNovas = [] # Lista com produções criadas durante a remoção de recursão direta
            k = 0 # Contador do total de produções lidas
            for cabeca, corpo in dicionario: # Percorre as produções
                recIndireta, prod = self.__procuraRecursaoIndireta(producoesLidas, cabeca, corpo) # Retorna se foi encontrada uma recursão indireta e o não terminal com recursão
                recDireta = self.__procuraRecursaoDireta(cabeca, corpo) # Retorna se foi encontrada uma recursão direta
                if recDireta and (recIndireta is False): # Checa se existe apenas recursão direta
                    np = self.__removerRecursaoDireta(cabeca, corpo) # Remove a recusão direta, retornando novas produções criadas
                    for n in np: # Loop para adicionar produções novas
                        if n not in producoesNovas: # Evita repetições
                            producoesNovas.append(n) # Adiciona nova produção
                if recIndireta: # Caso exista recursão indireta, está deve ser removida
                    self.__removerRecursaoIndireta(prod, cabeca, corpo) # Remove a recursão indireta
                producoesLidas.append(cabeca) # Adiciona a cabeça da produção que foi lida na interação
                if (recIndireta is False) and (recDireta is False) and (k == (len(dicionario)-1)): # Caso não existam mais recursões autoriza a parada
                    parar = True # Libera a interrupção do loop
                k += 1
            # Abaixo são adicionadas novas produções
            if len(producoesNovas) > 0:
                for np in producoesNovas:
                    adicionaEP = True
                    for cabeca1, corpo1 in dicionario:
                        if cabeca1 == np[0]:
                            if '&' in corpo1:
                                adicionaEP = False # Evita adicionar mais de um epsilon
                                break
                    if adicionaEP:
                        self.adicionaProducao([np[1], np[2]], np[0])
                    else:
                        self.adicionaProducao([np[1]], np[0])
            if (k == len(dicionario)) and parar: # Em caso de loop infinito, trocar a condição para (k >= len(dicionario)) and parar
                break

    def __procuraRecursaoIndireta(self, producoesLidas, cabeca, corpo):
        if len(producoesLidas) > 0: # Checa se existem produções lidas
            for c in corpo: # Para cada produção no corpo
                if c[0] in producoesLidas: # Se o primeiro elemento da produção for o não terminal da cabeça de uma produção anterior
                    return True, c[0] # Existe recursão indireta
        return False, None # Do contrário, não

    def __procuraRecursaoDireta(self, cabeca, corpo):
        for c in corpo: # Para cada produção no corpo
            if c[0] == cabeca: # Se o primeiro elemento da produção for o não terminal da cabeça da produção
                return True # Existe recursão direta
        return False # Do contrário, não

    def __removerRecursaoIndireta(self, producaoTroca, cabeca, corpo):
        dicionario = self.getProducoes().items()
        novos = [] # Lista de produções modificadas com o coropo no lugar da cabeça, para remover a recursão indireta
        for c in corpo: # Para cada produção no corpo
            if c[0] == producaoTroca: # Se o primeiro simbolo da produção for igual a cabeça encontrada na recursão indireta
                corpo.remove(c) # Remove essa produção do corpo
                temp = c[1:] # Copia a produção sem a cabeça que causa recursão
                for cabeca1, corpo1 in dicionario: # Para cada item no dicionário
                    if cabeca1 == producaoTroca: # Se a cabeça da produção for igual a cabeça que se deve trocar
                        for c1 in corpo1: # Para cada produção no corpo
                            novos.append(c1+temp) # Adiciona o corpo da produção junto ao corpo da produção que será atualizada
        for n in novos: # Para cada produção atualizada
            corpo.append(n) # Adiciona ao corpo
        """
            O Que essa função faz:
            S -> Aa | b
            A -> Ac | Sd | a
            Transforma em:
            S -> Aa | b
            A -> Ac | Aad | bd | a
        """

    def __removerRecursaoDireta(self, cabeca, corpo):
            dicionario = self.getProducoes().items()
            novasProducoes = [] # Novas produções encontradas para conter elementos que retiram a recursão direta
            betas = [] # Novos corpos de produções modificados
            atualiza = False # Demarca se a atualização deve ocorrer
            for c in corpo: # Para cada produção no corpo
                cabecaProd = "" # String que deve procurar a cabeça de produção que é igual a cabeça de produção que causa recursão direta
                remover = False # Demarca se haverá remoção da cabeça no corpo
                for i in range(len(c)): # Loop para o tamanho da palavra
                    cabecaProd += c[i] # Forma a cabeça da produção caractere por caractere
                    if cabecaProd == cabeca: # Se a cabeça formada for igual a cabeça passada
                        remover = True # Pode remover da produção
                        break # Quebra
                if remover: # Se puder remvoer
                    atualiza = True # Também pode atualizar
                    alfa = c # O alfa inicia com uma produção do corpo
                    alfa = alfa.replace(cabecaProd, "") # Retira a cabeça da produção do alfa
                    cabecaProd2 = cabecaProd+"'" # Forma uma nova cabeça de produção para adicionar elementos para retirar a recusão
                    for c1 in corpo: # Para cada produção no corpo
                        if c1 != c: # Se esse produção for diferente da anterior
                            if cabecaProd not in c1: # Se a cabeça encontrada não está na produção atual
                                beta = c1+cabecaProd2 # Forma o beta, Ex: aS'
                                if beta not in betas: # Evita repetições
                                    betas.append(beta) # Adiciona o beta na lista de betas
                    novasProducoes.append([cabecaProd2, alfa+cabecaProd2, "&"]) # Adiciona uma nova produção
            if atualiza: # Podendo-se atualizar
                corpo.clear() # Limpar o corpo
                for b in betas: # Para cada beta
                    corpo.append(b) # Adiciona no corpo
            return novasProducoes # Retorna as novas produções

    #################################### Fim dos Métodos de Recursão ####################################
            
    #################################### Começa os Métodos de Fatoração ####################################

    def fatorar(self):
        dicionario = self.getProducoes().items()
        for i in range(8):
            novasProducoes = []
            for cabeca, corpo in dicionario:
                direto = self.__procuraNaoDeterminismoDireto(corpo)
                indireto = self.__procuraNaoDeterminismoIndireto(cabeca, corpo)
                if direto and (indireto is False):
                    novaCabeca, producoes = self.__removerNaoDeterminismoDireto(cabeca, corpo)
                    novasProducoes.append([novaCabeca, producoes])
                if indireto:
                    self.__removerNaoDeterminismoIndireto(cabeca, corpo)
            for n in novasProducoes:
                for i in range(len(n[1])):
                    if n[1][i] == '':
                        n[1][i] = '&'
                    i += 1
                self.adicionaProducao(n[1], n[0])

    def __procuraNaoDeterminismoDireto(self, corpo):
        for c1 in corpo:
            for c2 in corpo:
                if c1 != c2:
                    t1 = self.__retornaTerminal(c1)
                    t2 = self.__retornaTerminal(c2)
                    if (t1 in self.__terminais) and (t2 in self.__terminais) and (t1 == t2):
                        return True
        return False

    def __retornaTerminal(self, producao):
        terminal = ""
        for i in range(len(producao)):
            terminal += producao[i]
            if terminal in self.__terminais:
                break
        return terminal

    def __procuraNaoDeterminismoIndireto(self, cabeca, corpo):
        dicionario = self.getProducoes().items()
        for c1 in corpo:
            if c1[0] in self.__nao_terminais:
                for cabeca1, corpo1 in dicionario:
                    if c1[0] == cabeca1:
                        checa = self.__checarCorpoProducao1(corpo, corpo1)
                        if checa:
                            return True
            for c2 in corpo:
                if c1 != c2:
                    if c1[0] in self.__nao_terminais and c2[0] in self.__nao_terminais:
                        checa = self.__checarCorpoProducao2(c1[0], c2[0])
                        if checa:
                            return True
        return False

    def __checarCorpoProducao1(self, corpoAtual, corpoVerificado):
        for c1 in corpoVerificado:
            for c2 in corpoAtual:
                if c1[0] == c2[0]:
                    return True
        return False

    def __checarCorpoProducao2(self, cabeca1, cabeca2):
        dicionario = self.getProducoes().items()
        for cabeca3, corpo3 in dicionario:
            for cabeca4, corpo4 in dicionario:
                if (cabeca1 == cabeca3) and (cabeca2 == cabeca4):
                    for c3 in corpo3:
                        for c4 in corpo4:
                            if c3[0] == c4[0]:
                                return True
        return False

    def __removerNaoDeterminismoDireto(self, cabeca, corpo):
        novaCabeca = cabeca+"'"
        l = []
        for c1 in corpo:
            for c2 in corpo:
                if c1 != c2:
                    t1 = self.__retornaTerminal(c1)
                    t2 = self.__retornaTerminal(c2)
                    # if (c1[0] in self.__terminais) and (c2[0] in self.__terminais) and (c1[0] == c2[0]):
                    if (t1 in self.__terminais) and (t2 in self.__terminais) and (t1 == t2):
                        tmp = t1+novaCabeca
                        # p1 = c1.replace(t1, '')
                        # p2 = c2.replace(t2, '')
                        p1 = self.__removerTerminal(c1, t1)
                        p2 = self.__removerTerminal(c2, t2)
                        if p1 != novaCabeca:
                            if p1 not in l:
                                l.append(p1)
                        if p2 != novaCabeca:
                            if p2 not in l:
                                l.append(p2)
                        if c1 in corpo:
                            corpo.remove(c1)
                        if c2 in corpo:
                            corpo.remove(c2)
                        if tmp not in corpo:
                            corpo.append(tmp)
        # print(novaCabeca, "->", l)
        return novaCabeca, l

    def __removerTerminal(self, producao, terminal):
        for i in range(len(terminal)):
            terminal = terminal[1:]
            producao = producao[1:]
        return producao

    def __removerNaoDeterminismoIndireto(self, cabeca, corpo):
        dicionario = self.getProducoes().items()
        for c1 in corpo:
            for c2 in corpo:
                if c2[0] in self.__nao_terminais:
                    for cabeca2, corpo2 in dicionario:
                        if c2[0] == cabeca2:
                            for c3 in corpo2:
                                if c1[0] == c3[0]:
                                    beta1 = c2[1:]
                                    for c3 in self.__retornaCorpoProducao(c2[0]):
                                        if c2 in corpo:
                                            corpo.remove(c2)
                                        if c3+beta1 not in corpo:
                                            corpo.append(c3+beta1)
        for c1 in corpo:
            for c2 in corpo:
                if c1 != c2:
                    if c1[0] in self.__nao_terminais and c2[0] in self.__nao_terminais:
                        beta1 = c1[1:]
                        beta2 = c2[1:]
                        if beta1 == beta2:
                            for c3 in self.__retornaCorpoProducao(c1[0]):
                                if c1 in corpo:
                                    corpo.remove(c1)
                                if c3+beta1 not in corpo:
                                    corpo.append(c3+beta1)
                            for c3 in self.__retornaCorpoProducao(c2[0]):
                                if c2 in corpo:
                                    corpo.remove(c2)
                                if c3+beta2 not in corpo:
                                    corpo.append(c3+beta2)

    def __retornaCorpoProducao(self, cabeca):
        dicionario = self.getProducoes().items()
        for cabeca1, corpo1 in dicionario:
            if cabeca == cabeca1:
                return corpo1
        return []

    #################################### Fim dos Métodos de Fatoração ####################################

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
