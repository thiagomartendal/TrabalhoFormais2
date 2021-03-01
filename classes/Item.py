from enum import Enum

class Item:
    def __init__(self, tipo, nome):
        self.__nome = nome
        self.__tipo = tipo

    def get_nome(self):
        return self.__nome

    def get_tipo(self):
        return self.__tipo

    def set_nome(self, nome):
        self.__nome = nome

    def set_tipo(self):
        return self.__tipo

    def parse(self):
        pass


class TipoItem(Enum):
    AF = 0
    GR = 1
    ER = 2
