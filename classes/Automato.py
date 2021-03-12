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

    # Verifica se existe estado no autômato
    def contemEstado(self, estado):
        for tmp in self.__estados:
            if estado.getNome() == tmp.getNome():
                return True
        return False

    # Gera o autômato a partir do texto escrito pelo usuario
    def parse(self, texto):
        if not texto:
            print("Texto vazio")
            return
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
