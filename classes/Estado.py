class Estado:

    # nome recebe uma string que nomeia o estado
    # tipo recebe um inteiro que indica se o estado é inicial, normal, final ou ainda inicial e final ao mesmo tempo
    # para tipo = 0 -> Estado Inicial
    # para tipo = 1 -> Estado Normal
    # para tipo = 2 -> Estado Final
    # para tipo = 3 -> Estado Inicial e Final

    def __init__(self, nome=None, tipo=None):
        self.__nome = nome
        self.__tipo = tipo

    # Define o nome do estado
    def setNome(self, nome):
        self.__nome = nome

    # Define o tipo do estado
    def setTipo(self, tipo):
        self.__tipo = tipo

    # Retorna o nome do estado
    def getNome(self):
        return self.__nome

    # Retorna o tipo do estado
    def getTipo(self):
        return self.__tipo
