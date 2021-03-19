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
    
    # Retorna o estado inicial
    def getEstadoInicial(self):
        for estado in self.__estados:
            if(estado.get_tipo() == 0 or estado.get_tipo() == 3):
                return estado

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

    # Retorna uma transição especifica
    def getTransicao(self, estado, simbolo):
        for i in self.__transicoes:
            if(i.__estadoPartida == estado and i.__simbolo == simbolo):
                return i

    # Retorna uma transição especifica a partir do nome do estado e do símbolo
    def getTransicaoNome(self, nome_estado, simbolo):
        for i in self.__transicoes:
            if(i.__estadoPartida.__nome == nome_estado and i.__simbolo == simbolo):
                return i

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

    # Testa se uma palavra é aceita pelo automato
    def reconhecimento(self, word):
        palavra = list(str(word))
        estado = self.getEstadoInicial()
        print(palavra)
        self.verificaPalavra(palavra, estado)

    # Verifica se a palavra é reconhecida pelo automato por meio de recursão
    def verificaPalavra(self, word, estado):
        palavra = word
        if(palavra == [] or palavra == "&"):
            if(estado.getTipo() == 3 or estado.getTipo() == 2):
                print("reconhece")
            else:
                print("não reconhece")
        elif(palavra != []): 
            print(palavra[0])
            proxiTransicao = self.getTransicao(estado, palavra[0])
            proximo = proxiTransicao.getEstadosChegada()
            print(proximo)
            if(proximo != None):
                palavra.remove(palavra[0])
                if(len(proximo) > 1):
                    for i in proximo:
                        self.verificaPalavra(palavra, i)
                else:
                    self.verificaPalavra(palavra, proximo[0])

    # Retorna a união entre dois automatos    
    def uniao(self, af):
        selfInitial = self.getEstadoInicial()
        afInitial = af.getEstadoInicial()
        initial = self.getEstadoInicial().getNome() + af.getEstadoInicial().getNome()
        estado_inicial = Estado(initial, 0)
        for i in self.getEstados():
            if(i.getTipo() == 3):
                i.setTipo(2)
            elif(i.getTipo() == 0):
                i.setTipo(1)
        
        for k in af.getEstados():
            if(k.getTipo() == 3):
                k.setTipo(2)
            elif(k.getTipo() == 0):
                k.setTipo(1)


        estados = self.getEstados() + af.getEstados()
        estados.append(estado_inicial)
        transicoes = self.getTransicoes() + af.getTransicoes()
        transicao1 = Transicao(estado_inicial, "&", [selfInitial])
        transicao2 = Transicao(estado_inicial, "&", [afInitial])
        transicoes.append(transicao1)
        transicoes.append(transicao2)
        alfabeto = self.getSimbolos()
        for x in af.getSimbolos():
            if(x not in alfabeto):
                alfabeto.append(x)
        alfabeto = alfabeto + ["&"]
        
        nome = "União {af1} + {af2}".format(af1 = self.get_nome(), af2 = af.get_nome()) 
        unionAF = Automato(nome)
        unionAF.setEstados(estados)
        unionAF.setTransicoes(transicoes)
        unionAF.setSimbolos(alfabeto)

        return unionAF

    # Retorna a interseção entre dois automatos
    def intersecao(self, af):
        # estado_inicial = self.getEstadoInicial().__nome + af.getEstadoInicial().__nome
        simbolos = self.getSimbolos()
        simbolos_af = af.getSimbolos()
        for x in simbolos_af:
            if(x not in simbolos):
                simbolos.append(x)
        estados = []
        for i in self.getEstados():
            for j in af.getEstados():
                if((i.getTipo() == 0 and j.getTipo() == 0) or (i.getTipo() == 0 and j.getTipo() == 3) or (i.getTipo() == 3 and j.getTipo() == 0)):
                    nome_estado = i.getNome() + j.getNome()
                    estado_inicial = Estado(nome_estado, 2)
                    estados.append(estado_inicial)
                elif((i.getTipo() == 2 and j.getTipo() == 2) or (i.getTipo() == 2 and j.getTipo() == 3) or (i.getTipo() == 3 and j.getTipo() == 2)):
                    nome_estado = i.getNome() + j.getNome()
                    estado_final = Estado(nome_estado, 2)
                    estados.append(estado_final)
                elif(i.getTipo() == 3 and j.getTipo() == 3):
                    nome_estado = i.getNome() + j.getNome()
                    estado_final = Estado(nome_estado, 3)
                    estados.append(estado_final)
                else:
                    nome_estado = i.getNome() + j.getNome()
                    estado = Estado(nome_estado, 1)
                    estados.append(estado)
        
        transicoes = []
        for i in simbolos:
            for j in estados:
                temp = self.getTransicaoNome(j.getNome()[0], i)
                temp2 = af.getTransicaoNome(j.getNome()[1], i)
                # sucessor = temp.getEstadosChegada().getNome() + temp2.getEstadosChegada().getNome()
                sucessor = temp.getEstadosChegada() + temp2.getEstadosChegada()
                trans = Transicao(j, i, sucessor)
                transicoes.append(trans)

        nome = "Interseção {af1} + {af2}".format(af1 = self.get_nome(), af2 = af.get_nome()) 
        intersecAF = Automato(nome)
        intersecAF.setEstados(estados)
        intersecAF.setTransicoes(transicoes)
        intersecAF.setSimbolos(simbolos)
        
        return intersecAF