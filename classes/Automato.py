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
        self.__simbolos.append(simbolo)

    # Adiciona uma lista de simbolos
    def setSimbolos(self, simbolos):
        if type(simbolos) is list:
            self.__simbolos.clear()
            self.__simbolos = [s for s in simbolos]

    # Retorna o alfabeto do automato
    def getSimbolos(self):
        return self.__simbolos

    # Adiciona um estado pronto
    def addEstado(self, estado):
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

    # Retorna a lista de transições
    def getTransicoes(self):
        return self.__transicoes

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
