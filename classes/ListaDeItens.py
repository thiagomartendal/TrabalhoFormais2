class ListaDeItens:

    def __init__(self):
        self.__lista_de_itens = [] # Lista de itens (automatos, gramaticas, etc)

    # Padrão singleton para usar uma única instancia da lista
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(ListaDeItens, cls).__new__(cls)
        return cls.instance

    # Adiciona item na lista de itens
    def adicionaItem(self, item):
        self.__lista_de_itens.append(item)

    # Remove item da lista de itens
    def removeItem(self, posicao):
        self.__lista_de_itens.pop(posicao)

    # Retorna item da lista de itens
    def getItem(self, posicao):
        return self.__lista_de_itens[posicao]

    def getLista(self):
        return self.__lista_de_itens
