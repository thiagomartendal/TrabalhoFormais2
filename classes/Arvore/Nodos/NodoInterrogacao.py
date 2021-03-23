from classes.Arvore.Nodo import Nodo
from classes.OperacaoER import *

class NodoInterrogacao(Nodo):

    def __init__(self):
        super(NodoInterrogacao, self).__init__(OperacaoER.INTERROGACAO.value, prioridade=prioridade(OperacaoER.INTERROGACAO))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        composicao = self.get_costura().subir(composicao)
        return composicao

    def subir(self, composicao):
        composicao = self.get_costura().subir(composicao)
        return composicao