from classes.Arvore.Nodo import Nodo
from classes.OperacaoER import *

class NodoConcatenacao(Nodo):

    def __init__(self):
        super(NodoConcatenacao, self).__init__(OperacaoER.CONCAT.value, prioridade=prioridade(OperacaoER.CONCAT))

    def descer(self, composicao):
        composicao = self.get_filho_esquerdo().descer(composicao)
        return composicao

    def subir(self, composicao):
        composicao = self.get_filho_direito().descer(composicao)
        return composicao