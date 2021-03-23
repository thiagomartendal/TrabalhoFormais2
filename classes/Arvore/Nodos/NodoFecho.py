from classes.Arvore.Nodo import Nodo
from classes.OperacaoER import *


class NodoFecho(Nodo):

    def __init__(self):
        super(NodoFecho, self).__init__(OperacaoER.FECHO.value, prioridade=prioridade(OperacaoER.FECHO))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        composicao = self.get_costura().subir(composicao)
        return composicao

    def subir(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        composicao = self.get_costura().subir(composicao)
        return composicao