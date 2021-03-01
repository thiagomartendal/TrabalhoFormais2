from Item import *

class Expressao(Item):

    def __init__(self, nome):
        super(Gramatica, self).__init__(TipoItem.ER, nome)