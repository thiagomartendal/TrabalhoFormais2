import string

from .Item import *
from .Arvore.Nodos.NodoConcatenacao import NodoConcatenacao
from .Arvore.Nodos.NodoFecho import NodoFecho
from .Arvore.Nodos.NodoFolha import NodoFolha
from .Arvore.Nodos.NodoInterrogacao import NodoInterrogacao
from .Arvore.Nodos.NodoUniao import NodoUniao
from .Arvore.Arvore import Arvore
from .OperacaoER import OperacaoER, prioridade

class Expressao(Item):

    __arvore = None

    def __init__(self, nome):
        super(Expressao, self).__init__(TipoItem.ER, nome)
        self.__valido = False

    def getValido(self):
        return self.__valido

    def parse(self, expressao):
        arv = self.gerar_arvore(expressao)
        self.__valido = arv[0]
        return arv

    def to_string(self):
        return self.__arvore.get_em_ordem()

    def gerar_arvore(self, expressao):
        self.__arvore = Arvore()
        expressao = self.preparar_expressao(expressao)
        erro, msg = self.verifica_validade(expressao)
        if erro:
            self.__arvore.set_nodo_raiz(self.gerar_nodo(expressao))
            self.__arvore.costura_arvore()
            self.__arvore.numera_folhas()
        else:
            return (erro, msg)
        try:
            self.verifica_validade(self.to_string())
            return (True, "")
        except:
            return (False, "Expressão possui operadores redundantes que resultam em recursão sem fim.") # Expressão possui operadores redundantes que resultam em recursão sem fim.

    def gerar_nodo(self, expressao):
        subexpressao = self.remover_parenteses_externos(expressao)

        if len(subexpressao) == 1 or (len(subexpressao) == 3 and subexpressao[0] == "'" and subexpressao[2] == "'"):
            return NodoFolha(subexpressao)
        else:
            operador_div = None
            prioridade_div = -1
            posicao_div = None

            parenteses_abertos = 0
            for i in range(0, len(subexpressao)):
                char = subexpressao[i]
                if char == "(":
                    if i > 0 and i < (len(subexpressao)-1):
                        if not(subexpressao[i-1] == "'" and subexpressao[i+1] == "'"):
                            parenteses_abertos += 1
                elif char == ")":
                    if i > 0 and i < (len(subexpressao)-1):
                        if not(subexpressao[i-1] == "'" and subexpressao[i+1] == "'"):
                            parenteses_abertos -= 1
                elif parenteses_abertos == 0:
                    if char == "|" and prioridade_div < 2:
                        operador_div = OperacaoER.UNIAO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "." and prioridade_div < 1:
                        operador_div = OperacaoER.CONCAT
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "*" and prioridade_div < 0:
                        operador_div = OperacaoER.FECHO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i
                    if char == "?" and prioridade_div < 0:
                        operador_div = OperacaoER.INTERROGACAO
                        prioridade_div = prioridade(operador_div)
                        posicao_div = i

            nodo = None
            if operador_div == OperacaoER.UNIAO:
                nodo = NodoUniao()
                nodo.set_filho_esquerdo(self.gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == OperacaoER.CONCAT:
                nodo = NodoConcatenacao()
                nodo.set_filho_esquerdo(self.gerar_nodo(subexpressao[0:posicao_div]))
                nodo.set_filho_direito(self.gerar_nodo(subexpressao[posicao_div + 1:]))

            elif operador_div == OperacaoER.FECHO:
                nodo = NodoFecho()
                nodo.set_filho_esquerdo(self.gerar_nodo(subexpressao[0:posicao_div]))

            else:  # operadorDiv == OperacaoER.INTERROGACAO:
                nodo = NodoInterrogacao()
                nodo.set_filho_esquerdo(self.gerar_nodo(subexpressao[0:posicao_div]))

            return nodo


    def verifica_validade(self, expressao):
        if not expressao:
            return (False, "A expressão não pode ser vazia.") # A expressão não pode ser vazia
        chars_validos = string.ascii_lowercase + string.digits + "|.*?()" + "+-/,;{}=<>'" + string.ascii_uppercase + '"'
        simbolo = string.ascii_lowercase + string.digits + "*()+-/,;{}=<>'" + string.ascii_uppercase + '"'
        nivel_parentesis = 0
        char_anterior = " "
        i_real = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if char in chars_validos:
                if i > 1:
                    if (char_anterior in "|.(" and char in "|.?*)"):
                        return (False, "Simbolo não esperado em alguma posição.") # Simbolo não esperado em alguma posição
                    elif char_anterior in "*?" and char in "*?":
                        return (False, "Simbolo não esperado em alguma posição.") # Simbolo não esperado em alguma posição

                if char == "(":
                    if i > 0 and i < (len(expressao)-1):
                        if not(expressao[i-1] == "'" and expressao[i+1] == "'"):
                            nivel_parentesis += 1
                elif char == ")":
                    if not(expressao[i-1] == "'" and expressao[i+1] == "'"):
                        nivel_parentesis -= 1
                    if nivel_parentesis < 0:
                        return (False, "Parenteses fechado sem correspondente em alguma posição.") # Parenteses fechado sem correspondente em alguma posição
                elif char == ".":
                    i_real -= 1
            else:
                return (False, "Simbolo desconhecido em alguma posição.") # Simbolo desconhecido em alguma posição
            char_anterior = char
            i_real += 1

        if nivel_parentesis > 0:
            return (False, "Parenteses aberto sem correspondente em alguma posição.") # Parenteses aberto sem correspondente em alguma posição
        return (True, "")

    def preparar_expressao(self, expressao):
        # Remove espaços em branco
        expressao = "".join(expressao.split())
        # Adiciona concatenações implicitas
        expressao = self.expor_concatenacoes_implicitas(expressao)
        print(expressao)
        return expressao

    def expor_concatenacoes_implicitas(self, expressao):
        chars_validos = string.ascii_lowercase + string.digits + "+-/,;{}=<>'" + string.ascii_uppercase + '"'
        nova_expressao = expressao
        char_anterior = " "
        concats_adicionadas = 0
        for i in range(0, len(expressao)):
            char = expressao[i]
            if not((char_anterior in "()*" and char in "'") or (char_anterior in "'" and char in "()*")):
                if (char_anterior in chars_validos or (char_anterior in ")*?")) and (char in chars_validos or char == "("):
                    nova_expressao = nova_expressao[:i+concats_adicionadas] + '.' + nova_expressao[i+concats_adicionadas:]
                    concats_adicionadas += 1
            char_anterior = char

        return nova_expressao

    def remover_parenteses_externos(self, expressao):
        parenteses_encontrados = 0
        nivel = 0
        inicio = True
        i = 0
        comprimento_expr = len(expressao)
        while i < comprimento_expr - parenteses_encontrados:
            char = expressao[i]
            if char == "(":
                if i > 0 and i < (len(expressao)-1):
                    if not(expressao[i-1] == "'" and expressao[i+1] == "'"):
                        nivel += 1
                        if inicio:
                            parenteses_encontrados = nivel
            else:
                inicio = False
                if char == ")":
                    if i > 0 and i < (len(expressao)-1):
                        if not(expressao[i-1] == "'" and expressao[i+1] == "'"):
                            nivel -= 1
                            parenteses_encontrados = min(parenteses_encontrados, nivel)
            i += 1
        return expressao[parenteses_encontrados:comprimento_expr - parenteses_encontrados]


    def obter_automato_finito_equivalente(self):
        from .Automato import Automato
        from .Estado import Estado
        from .Transicao import Transicao

        folhas = self.__arvore.numera_folhas()
        lista_de_nomes = []

        obter_composicao = {}  # mapeia estados para sua composição
        obter_estado = {}  # mapeia composicoes para seu estado

        composicao_da_raiz = self.__arvore.composicao_da_raiz()

        estado_inicial = Estado(self.novo_nome(lista_de_nomes), 0)
        for simbolo in composicao_da_raiz:
            if simbolo == "$":
                estado_inicial.setTipo(3)

        automato = Automato(self.get_nome() + " (convertido para AF)")
        automato.addEstado(estado_inicial)

        obter_composicao[estado_inicial] = composicao_da_raiz
        obter_estado[self.obter_composicao_como_chave(composicao_da_raiz)] = estado_inicial

        lista_estados = [estado_inicial]

        while len(lista_estados) > 0:
            estado_atual = lista_estados.pop(0)
            composicao_atual = obter_composicao[estado_atual]

            for simbolo in composicao_atual:
                if simbolo != "$":
                    novo_estado = Estado(self.novo_nome(lista_de_nomes), 1)
                    nova_composicao = {}

                    for numero_folha in composicao_atual[simbolo]:
                        folhas[numero_folha].subir(nova_composicao)
                    obter_composicao[novo_estado] = nova_composicao

                    nova_composicao_como_chave = self.obter_composicao_como_chave(nova_composicao)
                    if nova_composicao_como_chave not in obter_estado:
                        obter_estado[nova_composicao_como_chave] = novo_estado
                        automato.addEstado(novo_estado)
                        lista_estados.append(novo_estado)
                    else:
                        lista_de_nomes.pop()
                        novo_estado = obter_estado[nova_composicao_como_chave]

                    transicao = Transicao(estado_atual, simbolo, [novo_estado])
                    automato.addTransicao(transicao)
                else:
                    if estado_atual.getTipo() == 1:
                        estado_atual.setTipo(2)
        return automato

    def obter_composicao_como_chave(self, composicao):
        id_nova_composicao = []
        for simb in composicao:
            par = (simb, tuple(sorted(list(composicao[simb]))))
            id_nova_composicao.append(par)
        return tuple(id_nova_composicao)

    def novo_nome(self, lista):
        from string import ascii_uppercase
        novo_nome = None
        for letra in ascii_uppercase:
            if letra not in lista:
                novo_nome = letra
                break

        if novo_nome == None:
            found = False
            for letra in ascii_uppercase:
                for letra2 in ascii_uppercase:
                    novo = letra + letra2
                    if novo not in lista:
                        novo_nome = novo
                        found = True
                        break
                if found:
                    break

        lista.append(novo_nome)
        return novo_nome

