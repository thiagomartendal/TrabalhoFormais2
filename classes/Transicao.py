class Transicao:

    # estadoPartida recebe o estado de saída por algum símbolo de transição
    # simbolo tecebe o caractere que realiza a transição entre estados
    # estadosChegada é uma lista que recebe um estado caso o autômato seja determinístico
    # caso o autômato seja não-determinístico estadosChegada deve conter mais de um estado

    def __init__(self, estadoPartida=None, simbolo=None, estadosChegada=None):
        self.__estadoPartida = estadoPartida
        self.__simbolo = simbolo
        if type(estadosChegada) is list:
            self.__estadosChegada = [x for x in estadosChegada]
        else:
            self.__estadosChegada = []

    # Define o estado de partida
    def setEstadoPartida(self, estadoPartida):
        self.__estadoPartida = estadoPartida

    # Define o símbolo de transição
    def setSimbolo(self, simbolo):
        self.__simbolo = simbolo

    # Define os estados de chegada a partir de uma lista
    def setEstadosChegada(self, estadosChegada):
        if type(estadosChegada) is list:
            self.__estadosChegada.clear()
            self.__estadosChegada = [x for x in estadosChegada]

    # Adiciona um novo estado de chegada
    def addEstadoChegada(self, estado):
        self.__estadosChegada.append(estado)

    # Retorna o estado de partida da transição
    def getEstadoPartida(self):
        return self.__estadoPartida

    # Retorna o símbolo
    def getSimbolo(self):
        return self.__simbolo

    # Retorna os estados de chegada da transição
    def getEstadosChegada(self):
        return self.__estadosChegada
