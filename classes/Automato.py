from collections import defaultdict
from .Estado import Estado
from .Transicao import Transicao
from .Item import Item, TipoItem

class Automato(Item):

    def __init__(self, nome):
        super(Automato, self).__init__(TipoItem.AF, nome)
        self.__simbolos = [] # Lista de simbolos do alfabeto
        self.__estados = [] # Lista de estados, não é necessário classificar entre estado inicial e finais, pois o próprio estado já deve conhecer esta informação
        self.__transicoes = [] # Lista de transições

    # Adiciona simbolo ao alfabeto
    def addSimbolo(self, simbolo):
        if simbolo not in self.__simbolos:
            self.__simbolos.append(simbolo)
            self.__simbolos.sort()

    # Adiciona uma lista de simbolos
    def setSimbolos(self, simbolos):
        if type(simbolos) is list:
            self.__simbolos.clear()
            self.__simbolos = [s for s in simbolos]
            self.__simbolos.sort()

    # Retorna o alfabeto do automato
    def getSimbolos(self):
        self.__simbolos.sort()
        return self.__simbolos

    # Adiciona um estado pronto
    def addEstado(self, estado):
        if estado not in self.__estados:
            self.__estados.append(estado)

    # Cria um novo estado a partir de seus atributos, e o adiciona a lista de estados
    def formarEstado(self, nome, tipo):
        estado = Estado(nome, tipo)
        self.__estados.append(estado)

    # Define a lista de estados da classe com uma outra lista já existente
    def setEstados(self, estados):
        if type(estados) is list:
            self.__estados.clear()
            self.__estados = [x for x in estados]

    # Retorna os estados
    def getEstados(self):
        return self.__estados

    # Retorna um estado do automato pelo nome
    def procurarEstado(self, nomeEstado):
        for estado in self.__estados:
            if estado.getNome() == nomeEstado:
                return estado
        return None

    # Adiciona uma transição pronta
    def addTransicao(self, transicao):
        self.addSimbolo(transicao.getSimbolo())
        self.__transicoes.append(transicao)

    # Cria uma nova transição com seus parâmetros, e então adiciona a lista de transições
    def formarTransicao(self, estadoPartida, simbolo, estadosChegada):
        if type(estadosChegada) is list:
            transicao = Transicao(estadoPartida, simbolo, estadosChegada)
            self.__transicoes.append(transicao)

    # Define a lista de transições da classe com uma outra lista já existente
    def setTransicoes(self, transicoes):
        if type(transicoes) is list:
            self.__transicoes.clear()
            self.__transicoes = [x for x in transicoes]
            for x in transicoes:
                self.addSimbolo(x.getSimbolo())

    # Retorna a lista de transições
    def getTransicoes(self):
        return self.__transicoes

    # Retorna uma transição especifica
    def getTransicao(self, estado, simbolo):
        for i in self.__transicoes:
            if(i.getEstadoPartida() == estado and i.getSimbolo() == simbolo):
                return i

    # Retorna uma transição especifica a partir do nome do estado e do símbolo
    def getTransicaoNome(self, nome_estado, simbolo):
        for i in self.__transicoes:
            if(i.getEstadoPartida().getNome() == nome_estado and i.getSimbolo() == simbolo):
                return i

    def ordenarTransicoes(self):
        self.__simbolos.sort()
        for e in self.__estados:
            print(e.getNome(), end=" ")
        print()
        for i in range(len(self.__transicoes)):
            if i < (len(self.__transicoes)-1):
                t1 = self.__transicoes[i]
                t2 = self.__transicoes[i+1]
                if self.__simbolos.index(t1.getSimbolo()) > self.__simbolos.index(t2.getSimbolo()):
                    self.__transicoes[i] = t2
                    self.__transicoes[i+1] = t1
        for i in range(len(self.__transicoes)):
            if i < (len(self.__transicoes)-1):
                t1 = self.__transicoes[i]
                t2 = self.__transicoes[i+1]
                if self.__estados.index(t1.getEstadoPartida()) > self.__estados.index(t2.getEstadoPartida()):
                    self.__transicoes[i] = t2
                    self.__transicoes[i+1] = t1

    # Verifica se existe estado no autômato
    def contemEstado(self, estado):
        for tmp in self.__estados:
            if estado.getNome() == tmp.getNome():
                return True
        return False

    def contemTransicao(self, estadoPartida, simbolo):
        for transicao in self.__transicoes:
            if (transicao.getEstadoPartida() == estadoPartida) and (transicao.getSimbolo() == simbolo):
                return True
        return False

    def deterministico(self):
        if "&" in self.__simbolos:
            return False
        for transicao in self.__transicoes:
            if len(transicao.getEstadosChegada()) > 1:
                return False
        return True

    def reconhecerErros(self, texto):
        texto = texto.replace(" ", "")
        if '-' not in texto:
            return (False, 0, "", "A declaração de estados e transições deve ser separada com uma linha contendo um hífem (-).")
        else:
            linhas = texto.splitlines()
            totalHifens = texto.count('-')
            if totalHifens > 1:
                return (False, 0, "", "O hífem deve apenas ser usado para separar a definição de estados e transições, onde é necessário apenas um hífem.")
            estadosDeclarados = []
            for i in range(len(linhas)):
                posHifem = linhas.index('-')
                if linhas[i] != '-':
                    linhaAtual = linhas[i]
                    if i < posHifem:
                        if ',' not in linhaAtual:
                            return (False, (i+1), linhaAtual, "Separe nome do estado e o tipo com vírgula.")
                        else:
                            estadoTipo = linhaAtual.split(',')
                            if estadoTipo[0] == '':
                                return (False, (i+1), linhaAtual, "O nome do estado não foi declarado.")
                            elif '.' in estadoTipo[0]:
                                return (False, (i+1), linhaAtual, "O nome do estado não deve conter '.', pois este é usado para separar estados de chegada em transições não-determinísticas.")
                            else:
                                estadosDeclarados.append(estadoTipo[0])
                            if estadoTipo[1] == '':
                                return (False, (i+1), linhaAtual, "O tipo do estado não foi declarado.")
                            elif estadoTipo[1] != 'I' and estadoTipo[1] != 'N' and estadoTipo[1] != 'F' and estadoTipo[1] != "IF":
                                return (False, (i+1), linhaAtual, "O tipo do estado declarado não é correto. Os tipos reconhecidos são: I - Inicial, N - Normal, F - Final, IF - Inicial e Final.")
                    else:
                        if ',' not in linhaAtual:
                            return (False, (i+1), linhaAtual, "Separe nome do estado de partida, o símbolo, e os estados de chegada com vírgula para formar uma transição.")
                        else:
                            totalVirgulas = linhaAtual.count(',')
                            if totalVirgulas < 2:
                                return (False, (i+1), linhaAtual, "Separe nome do estado de partida, o símbolo, e os estados de chegada com vírgula para formar uma transição.")
                            elif totalVirgulas > 2:
                                return (False, (i+1), linhaAtual, "A linha não deve conter mais de 2 vírgulas para efetuar as separações.")
                            else:
                                transicao = linhaAtual.split(',')
                                if transicao[0] == '':
                                    return (False, (i+1), linhaAtual, "O estado de partida não foi definido na transição da linha "+str(i+1)+".")
                                if transicao[0] not in estadosDeclarados:
                                    return (False, (i+1), linhaAtual, "O estado "+transicao[0]+" não foi declarado acima. Declare o estado com "+transicao[0]+",Tipo (I,N,F,IF).")
                                if transicao[1] == '':
                                    return (False, (i+1), linhaAtual, "O símbolo de transição não foi definido na transição da linha "+str(i+1)+".")
                                if '.' in transicao[2]:
                                    estadosChegada = transicao[2].split('.')
                                    if transicao[2] == '.':
                                        return (False, (i+1), linhaAtual, "Os estados de chegada não foram definidos.")
                                    for e in estadosChegada:
                                        if e == '':
                                            return (False, (i+1), linhaAtual, "Um dos estados de chegada não foram definidos. Uma transição não deve terminar com '.' pois este indica a separação dos estados de chegada para um autômato não-determinístico.")
                                        if e not in estadosDeclarados:
                                            return (False, (i+1), linhaAtual, "O estado "+e+" não foi declarado acima. Declare o estado com "+e+",Tipo (I,N,F,IF).")
                                else:
                                    if transicao[2] == '':
                                        return (False, (i+1), linhaAtual, "Os estados de chegada não foram definidos na transição da linha "+str(i+1)+".")
                                    if transicao[2] not in estadosDeclarados:
                                        return (False, (i+1), linhaAtual, "O estado "+transicao[2]+" não foi declarado acima. Declare o estado com "+transicao[2]+",Tipo (I,N,F,IF).")
        return (True, 0, "", "")

    # Gera o autômato a partir do texto escrito pelo usuario
    def parse(self, texto):
        if not texto:
            print("Texto vazio")
            return
        texto = texto.replace(" ", "")
        self.__estados.clear()
        self.__simbolos.clear()
        self.__transicoes.clear()
        linhasEstados = texto.split('-')[0].splitlines()
        linhasEstados = list(filter(None, linhasEstados))
        linhasTransicoes = texto.split('-')[1].splitlines()
        linhasTransicoes = list(filter(None, linhasTransicoes))
        for l in linhasEstados:
            estado = Estado(l.split(",")[0])
            if l.split(",")[1] == "I":
                estado.setTipo(0)
            elif l.split(",")[1] == "N":
                estado.setTipo(1)
            elif l.split(",")[1] == "F":
                estado.setTipo(2)
            elif l.split(",")[1] == "IF":
                estado.setTipo(3)
            self.addEstado(estado)
        for l in linhasTransicoes:
            l1 = l.split(",")
            estado1 = self.procurarEstado(l1[0])
            if estado1 is None:
                return 1
            transicao = Transicao(estado1, l1[1])
            if l1[1] not in self.__simbolos:
                self.__simbolos.append(l1[1])
            estado2 = None
            if "." in l1[2]:
                l2 = l1[2].split(".")
                for l3 in l2:
                    estado2 = self.procurarEstado(l3)
                    if estado2 is None:
                        return 2
                    transicao.addEstadoChegada(estado2)
            else:
                estado2 = self.procurarEstado(l1[2])
                if estado2 is None:
                    return 2
                transicao.addEstadoChegada(estado2)
            self.addTransicao(transicao)

    # Verifica se exite transição por epsilon
    def __contemEpsilon(self):
        if "&" in self.__simbolos:
            return True
        return False

    # Realiza a determinização do automato
    def determinizar(self):
        eFecho = defaultdict(list)
        for estado in self.__estados:
            eFecho[estado].append(estado)
        if self.__contemEpsilon():
            for estado in self.__estados:
                eFecho = self.__eFechoRecursivo(eFecho, estado)
        estadoInicial, estadosFormadores = self.__construirEstado(eFecho, self.__estados[0], True)
        automato = Automato(self.get_nome())
        automato = self.__determinizacao(automato, eFecho, estadoInicial, estadosFormadores)
        return automato

    # Calcula o e-fecho recursivo
    def __eFechoRecursivo(self, eFecho, estadoAtual):
        for transicao in self.__transicoes:
            if (transicao.getEstadoPartida() == estadoAtual) and (transicao.getSimbolo() == "&"):
                for estado in transicao.getEstadosChegada():
                    if estado not in eFecho[estadoAtual]:
                        eFecho[estadoAtual].append(estado)
                        eFecho = self.__eFechoRecursivo(eFecho, estado)
        return eFecho

    # Forma novos estados a partir do e-fecho e um estado de referência (estadoMestre)
    def __construirEstado(self, eFecho, estadoMestre, formatarEstado):
        nomeEstado = ""
        tipoEstado = 1
        estadosFormadores = []
        for estado in eFecho[estadoMestre]:
            if estado.getNome() not in nomeEstado:
                nomeEstado += estado.getNome()+","
                if estado.getTipo() == 2:
                    tipoEstado = 2
                if estado not in estadosFormadores:
                    estadosFormadores.append(estado)
        if nomeEstado == self.__estados[0].getNome():
            tipoEstado = self.__estados[0].getTipo()
        elif (estadoMestre.getTipo() == 0) or (estadoMestre.getTipo() == 3):
            tipoEstado = estadoMestre.getTipo()
        if formatarEstado:
            if len(nomeEstado) > 1:
                nomeEstado = self.__formatarNomeEstado(nomeEstado)
        return Estado(nomeEstado, tipoEstado), estadosFormadores

    # Retorna os nomes dos estados existentes no autômato em uma lista
    def __estadosAutomato(self):
        lista = []
        for estado in self.__estados:
            lista.append(estado.getNome())
        return lista

    # Formata o nome de um estado criado de acordo com a ordem dos estados existentes no automato
    # Se é criado um estado ba, o nome é formatado para ab caso a lista de estado do automato esteja na ordem [a, b]
    def __formatarNomeEstado(self, nomeEstado):
        listaEstados = self.__estadosAutomato()
        vect = nomeEstado.split(",")
        vect = list(filter(None, vect))
        for i in range(len(vect)):
            for j in range(0, len(vect)-i-1):
                p1 = listaEstados.index(vect[j])
                p2 = listaEstados.index(vect[j+1])
                if p1 > p2:
                    temp = vect[j]
                    vect[j] = vect[j+1]
                    vect[j+1] = temp
        return "".join(vect)

    # Realiza o processo de determinização de forma recursiva, construindo os novos estados
    def __determinizacao(self, automato, eFecho, estadoAtual, estadosFormadores):
        automato.addEstado(estadoAtual)
        for simbolo in self.__simbolos:
            if simbolo != "&":
                nomeEstadoChegada = ""
                tipoEstado = 1
                novosFormadores = []
                for estado in estadosFormadores:
                    for transicao in self.__transicoes:
                        if (estado == transicao.getEstadoPartida()) and (simbolo == transicao.getSimbolo()):
                            for estadoChegada in transicao.getEstadosChegada():
                                tmp, formadores = self.__construirEstado(eFecho, estadoChegada, False)
                                if tmp.getNome() not in nomeEstadoChegada:
                                    nomeEstadoChegada += tmp.getNome()
                                    if tmp.getTipo() == 2:
                                        tipoEstado = 2
                                for x in formadores:
                                    if x not in novosFormadores:
                                        novosFormadores.append(x)
                if nomeEstadoChegada != "":
                    nomeEstadoChegada = self.__formatarNomeEstado(nomeEstadoChegada)
                    if nomeEstadoChegada == automato.getEstados()[0].getNome():
                        tipoEstado = automato.getEstados()[0].getTipo()
                    estado = Estado(nomeEstadoChegada, tipoEstado)
                    transicao = Transicao(estadoAtual, simbolo, [estado])
                    automato.addTransicao(transicao)
                    if automato.contemEstado(estado) == False:
                        automato = self.__determinizacao(automato, eFecho, estado, novosFormadores)
        return automato

    def conversaoEmGR(self):
        from .Gramatica import Gramatica
        gr = Gramatica(self.get_nome() + " (convertido para GR)")

        nao_terminais = set() # conjunto de simbolos não terminais
        terminais = set() # conjunto de simbolos terminais

        tipo = 0 # tipo do estado incial

        producoes = {} # dicionario de producoes

        estado_novo = False # variavel usada para verificar se um estado novo vai ser criado com epsilon

        for estado in self.__estados: # seta estado inicial e seu tipo
            if estado.getTipo() == 0:
                gr.setSimboloInicial(estado.getNome())

            elif estado.getTipo() == 3:
                gr.setSimboloInicial(estado.getNome())
                tipo = 3

            nao_terminais.add(estado.getNome())

        #print(tipo)
        gr.setN(nao_terminais)

        tmp = set(nao_terminais)
        tmp.remove(gr.getSimboloInicial())

        producoes[gr.getSimboloInicial()] = []
        for nt in tmp:
            producoes[nt] = []

        for simbolo in self.__simbolos:
            terminais.add(simbolo)

        gr.setT(terminais)

        for transicao in self.__transicoes:
            estadoPartida = transicao.getEstadoPartida()
            simbolo = transicao.getSimbolo()
            estadosChegada = transicao.getEstadosChegada()

            prod = []

            for est in estadosChegada:
                prod.append(simbolo + est.getNome())

                if est.getTipo() == 2 or est.getTipo() == 3:
                    prod.append(simbolo)

                if tipo == 3:
                    if est.getNome() == gr.getSimboloInicial():
                        estado_novo = True

            producoes[estadoPartida.getNome()] = producoes[estadoPartida.getNome()] + prod

        #print(producoes)

        if (not estado_novo) and tipo == 3: # estado inicial aceita vazio mas nao possui nenhuma transicao para si mesmo
            producoes[gr.getSimboloInicial()] = producoes[gr.getSimboloInicial()] + ['&']

        if estado_novo: # cria estado novo com epsilon
            novasProducoes = {}
            gr.setSimboloInicial(gr.getSimboloInicial() + "0")
            novasProducoes[gr.getSimboloInicial()] = producoes[gr.getSimboloInicial()[:-1]] + ['&']

            for x, y in producoes.items():
                novasProducoes[x] = y

            producoes = novasProducoes

        gr.setProducoes(producoes)
        #print(gr.getProducoes())

        return gr


    def minimizar(self):

        automato = Automato('')
        automato.setEstados(list(self.getEstados()))
        automato.setSimbolos(list(self.getSimbolos()))
        automato.setTransicoes(list(self.getTransicoes()))

        estados_inacessiveis = automato.estadosInacessiveis()
        estados_mortos = automato.estadosMortos()

        for estado in estados_inacessiveis + estados_mortos:
            automato.removerEstadoETransicoes(estado)


        conjuntos_por_iteracao = automato.equivalencia()

        novoAutomato = Automato(self.get_nome() + " minimizado")
        novoAutomato.setSimbolos(list(self.getSimbolos()))

        lista_conjuntos_finais = conjuntos_por_iteracao[-1]
        estados_aceitacao = []
        for conjunto in lista_conjuntos_finais:
            lista_estados = list(conjunto)

            nome = ""
            inicial = False
            final = False
            for estado in lista_estados:
                nome += estado.getNome()
                if estado.getTipo() == 0:
                    inicial = True
                elif estado.getTipo() == 2:
                    final = True
                elif estado.getTipo() == 3:
                    inicial = True
                    final = True

            if len(nome) > 1:
                nome = "".join(set(nome))
                nome_sorted = sorted(nome)
                nome = "".join(nome_sorted)

            if inicial == True and final == True:
                novoAutomato.addEstado(Estado(nome, 3))
            elif inicial == True and final == False:
                novoAutomato.addEstado(Estado(nome, 0))
            elif inicial == False and final == True:
                novoAutomato.addEstado(Estado(nome, 2))
            else:
                novoAutomato.addEstado(Estado(nome, 1))

        for conjunto in lista_conjuntos_finais:
            lista_estados = list(conjunto)

            for simbolo in automato.getSimbolos():
                nomeOrigem = ""
                nomeDestino = ""
                for estado in lista_estados:
                    nomeOrigem += estado.getNome()
                    nomeDestino = automato.encontrarConjunto(estado, lista_conjuntos_finais, simbolo)

                if len(nomeOrigem) > 1:
                    nomeOrigem = "".join(set(nomeOrigem))
                    nomeOrigem_sorted = sorted(nomeOrigem)
                    nomeOrigem = "".join(nomeOrigem_sorted)

                if len(nomeDestino) > 1:
                    nomeDestino = "".join(set(nomeDestino))
                    nomeDestino_sorted = sorted(nomeDestino)
                    nomeDestino = "".join(nomeDestino_sorted)

                if len(nomeDestino) > 0:
                    estadoPartida = novoAutomato.procurarEstado(nomeOrigem)
                    estadoChegada = novoAutomato.procurarEstado(nomeDestino)

                    novoAutomato.addTransicao(Transicao(estadoPartida, simbolo, [estadoChegada]))

        return novoAutomato

    def encontrarConjunto(self, estado, lista_conjuntos, simbolo):
        estado_chegada = self.getEstadoChegadaDeEstadoPartida(estado, simbolo)
        nome = ""
        for conjunto in lista_conjuntos:
            lista_estados = list(conjunto)
            if estado_chegada in lista_estados:
                for estado in lista_estados:
                    nome += estado.getNome()

        return nome


    def estadosInacessiveis(self):
        estados_alcancados = set()
        estados_alcancados.add(self.getEstadoInicial())
        estados_a_visitar = set(estados_alcancados)

        while len(estados_a_visitar) > 0:
            estados_encontrados = set()
            for estado in estados_a_visitar:
                estados_encontrados = estados_encontrados.union(self.getEstadosChegadaDeEstadoPartida(estado))

            estados_a_visitar = estados_encontrados - estados_alcancados
            estados_alcancados = estados_alcancados.union(estados_encontrados)

        tmpEstados = set(self.__estados) - estados_alcancados
        return list(tmpEstados)

    def estadosMortos(self):
        vivos_atuais = set(self.getEstadosFinais())
        vivos_anteriores = set()

        while vivos_atuais != vivos_anteriores:
            vivos_anteriores = set(vivos_atuais)
            estados_encontrados = set()
            for estado in (set(self.__estados) - vivos_atuais):

                estados = self.getEstadosChegadaDeEstadoPartida(estado)

                for est in estados:
                    if est in vivos_anteriores:
                        estados_encontrados.add(estado)
                        break

            vivos_atuais = vivos_anteriores.union(estados_encontrados)

        tmpEstados = set(self.__estados) - vivos_atuais
        return list(tmpEstados)

    def equivalencia(self):
        estado_morto = self.criaEstadoMorto()
        conjuntos_por_iteracao = []
        conjuntos_por_iteracao.append([set(self.__estados) - self.getEstadosFinais(), self.getEstadosFinais()])

        i = 0
        while i == 0 or len(conjuntos_por_iteracao[i]) != len(conjuntos_por_iteracao[i-1]):
            i += 1
            conjuntos_por_iteracao.append([])
            for conjunto_estados in conjuntos_por_iteracao[i-1]:
                lista_estados = list(conjunto_estados)
                ja_agrupados = []
                for j in range(len(lista_estados)):
                    estado_um = lista_estados[j]
                    if estado_um not in ja_agrupados:
                        ja_agrupados.append(estado_um)
                        equivalentes = [estado_um]
                        for k in range(j+1, len(lista_estados)):
                            estado_dois = lista_estados[k]
                            if estado_dois not in ja_agrupados and self.estadosEquivalentes(estado_um, estado_dois, conjuntos_por_iteracao[i-1], estado_morto):
                                equivalentes.append(estado_dois)
                                ja_agrupados.append(estado_dois)
                        conjuntos_por_iteracao[i].append(equivalentes)

        return conjuntos_por_iteracao

    def estadosEquivalentes(self, estado_um, estado_dois, lista_conjuntos, estado_morto):
        for simbolo in self.__simbolos:
            estado_destino_um = self.getEstadoDestino(estado_um, simbolo, estado_morto)
            estado_destino_dois = self.getEstadoDestino(estado_dois, simbolo, estado_morto)
            for conjunto in lista_conjuntos:
                if estado_destino_um in conjunto and estado_destino_dois not in conjunto:
                    return False
                elif estado_destino_um not in conjunto and estado_destino_dois in conjunto:
                    return False

        return True

    def getEstadoDestino(self, estadoPartida, simbolo, morto):
        estadoDestino = []
        for transicao in self.__transicoes:
            if transicao.getEstadoPartida() == estadoPartida and transicao.getSimbolo() == simbolo:
                nome = transicao.getEstadosChegada()[0].getNome()
                estadoDestino = self.procurarEstado(nome)
                break

        if estadoDestino == []:
            return morto
        else:
            return estadoDestino

    def criaEstadoMorto(self):
        from string import ascii_uppercase
        novo_estado = None
        letras = []
        for estado in self.__estados:
            letras.append(estado.getNome())

        for letra in ascii_uppercase:
            if letra not in letras:
                novo_estado = letra
                break

        return Estado(novo_estado, 2)

    def getEstadoInicial(self):
        for estado in self.__estados:
            if estado.getTipo() == 0 or estado.getTipo() == 3:
                return estado
        return None

    def getEstadosFinais(self):
        finais = []
        for estado in self.__estados:
            if estado.getTipo() == 2 or estado.getTipo() == 3:
                finais.append(estado)
        return set(finais)

    def getEstadosChegadaDeEstadoPartida(self, estado):
        estados = set()
        for transicao in self.__transicoes:
            if transicao.getEstadoPartida() == estado:
                nome = transicao.getEstadosChegada()[0].getNome()
                estados.add(self.procurarEstado(nome))
        return estados

    def getEstadoChegadaDeEstadoPartida(self, estadoPartida, simbolo):
        estado = None
        for transicao in self.__transicoes:
            if transicao.getEstadoPartida() == estadoPartida and transicao.getSimbolo() == simbolo:
                nome = transicao.getEstadosChegada()[0].getNome()
                estado = self.procurarEstado(nome)
                break

        return estado

    def removerEstadoETransicoes(self, estado):
        tmpTransicoes = list(self.__transicoes)
        for transicao in self.__transicoes:
            if transicao.getEstadoPartida() == estado:
                tmpTransicoes.remove(transicao)
        self.__transicoes = tmpTransicoes
        self.__estados.remove(estado)

    # Testa se uma palavra é aceita pelo automato
    def reconhecimento(self, word):
        aceita = False
        palavra = list(str(word))
        estado = self.getEstadoInicial()
        if(word == "&"):
            if(estado.getTipo() == 3):
                aceita = True
        else:
            aceita = self.verificaPalavra(palavra, estado)
        return aceita

    # Verifica se a palavra é reconhecida pelo automato
    def verificaPalavra(self, palavra, estado):
        sucessor = []
        palavra_computada = []
        palavra_restante = []
        for i in range(len(palavra)):
            if palavra[i] not in self.__simbolos:
                return False
            palavra_computada.append(palavra[i])
            palavra_restante = palavra[i:]
            transicao = self.getTransicao(estado, palavra[i])
            if(transicao != None):
                sucessor = transicao.getEstadosChegada()
            if(len(sucessor) > 1):
                for j in sucessor:
                    self.verificaPalavra(palavra_restante, j)
            else:
                estado = sucessor[0]

        if(estado.getTipo() == 3 or estado.getTipo() == 2):
            # print("reconhece")
            return True
        else:
            # print("não reconhece")
            return False

    # Retorna a união entre dois automatos
    def uniao(self, af):
        selfInitial = self.getEstadoInicial()
        afInitial = af.getEstadoInicial()
        initial = self.getEstadoInicial().getNome() + af.getEstadoInicial().getNome()
        estado_inicial = Estado(initial, 0)
        for i in self.getEstados():
            if(i.getTipo() == 3):
                i.setTipo(2)
            elif(i.getTipo() == 0):
                i.setTipo(1)

        for k in af.getEstados():
            if(k.getTipo() == 3):
                k.setTipo(2)
            elif(k.getTipo() == 0):
                k.setTipo(1)


        estados = self.getEstados() + af.getEstados()
        estados.append(estado_inicial)
        transicoes = self.getTransicoes() + af.getTransicoes()
        transicaoInicial = Transicao(estado_inicial, "&", [selfInitial, afInitial])
        # transicao2 = Transicao(estado_inicial, "&", [afInitial])
        transicoes.append(transicaoInicial)
        # transicoes.append(transicao2)
        alfabeto = self.getSimbolos()
        for x in af.getSimbolos():
            if(x not in alfabeto):
                alfabeto.append(x)
        alfabeto = alfabeto + ["&"]

        nome = "União {af1} + {af2}".format(af1 = self.get_nome(), af2 = af.get_nome())
        unionAF = Automato(nome)
        unionAF.setEstados(estados)
        unionAF.setTransicoes(transicoes)
        unionAF.setSimbolos(alfabeto)

        return unionAF

    # Retorna a interseção entre dois automatos
    def intersecao(self, af):
        simbolos_af1 = self.getSimbolos()
        simbolos_af2 = af.getSimbolos()
        simbolos = list(set(simbolos_af1).intersection(set(simbolos_af2)))
        if(simbolos == [] or len(simbolos_af1) != len(simbolos_af2)):
            return None
        else:
            nome = "Interseção {af1} + {af2}".format(af1 = self.get_nome(), af2 = af.get_nome())
            intersecAF = Automato(nome)
            self.preencheAutomato()
            af.preencheAutomato()
            estados = []
            for i in self.getEstados():
                for j in af.getEstados():
                    if((i.getTipo() == 0 and j.getTipo() == 0) or (i.getTipo() == 0 and j.getTipo() == 3) or (i.getTipo() == 3 and j.getTipo() == 0)):
                        nome_estado = i.getNome() + j.getNome()
                        estado_inicial = Estado(nome_estado, 0)
                        estados.append(estado_inicial)
                    elif((i.getTipo() == 2 and j.getTipo() == 2) or (i.getTipo() == 2 and j.getTipo() == 3) or (i.getTipo() == 3 and j.getTipo() == 2)):
                        nome_estado = i.getNome() + j.getNome()
                        estado_final = Estado(nome_estado, 2)
                        estados.append(estado_final)
                    elif(i.getTipo() == 3 and j.getTipo() == 3):
                        nome_estado = i.getNome() + j.getNome()
                        estado_final = Estado(nome_estado, 3)
                        estados.append(estado_final)
                    else:
                        nome_estado = i.getNome() + j.getNome()
                        estado = Estado(nome_estado, 1)
                        estados.append(estado)
            
            intersecAF.setEstados(estados)
            intersecAF.setSimbolos(simbolos)
            
            transicoes = []
            for i in self.getEstados():
                for j in af.getEstados():
                    for x in simbolos:
                        sucessor = []
                        nome_estado = i.getNome() + j.getNome()
                        estado = intersecAF.procurarEstado(nome_estado)
                        temp = self.getTransicao(i, x)
                        temp2 = af.getTransicao(j, x)
                        nome_sucessor = temp.getEstadosChegada()[0].getNome() + temp2.getEstadosChegada()[0].getNome()
                        sucessor.append(intersecAF.procurarEstado(nome_sucessor))
                        transicao = Transicao(estado, x, sucessor)
                        transicoes.append(transicao)

            for x in transicoes:
                chegada = x.getEstadosChegada()
                for w in chegada:
                    if(w == "-"):
                        index = chegada.index("-")
                        chegada.pop(index)

            intersecAF.setTransicoes(transicoes)

            return intersecAF
    
    # Retorna um automato sem transições indefinidas
    def preencheAutomato(self):
        for i in self.getEstados():
            for j in self.getSimbolos():
                transicao = self.getTransicao(i, j)
                if(transicao == None):
                    nova_transicao = Transicao(i, j, ["-"])
                    self.addTransicao(nova_transicao)

