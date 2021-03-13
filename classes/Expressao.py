from .Item import Item, TipoItem
import string

class Expressao(Item):

    def __init__(self, nome):
        super(Expressao, self).__init__(TipoItem.ER, nome)
        self.__texto = None
        self.__expressoes = {}
        self.__valido = False

    def parse(self, texto):
        self.__texto = texto
        self.__texto.replace(" ","")
        self.__valido = self.validaExpressao(self.__texto.splitlines())

    def getValido(self):
        return self.__valido

    def getTexto(self):
        return self.__texto

    def validaExpressao(self, linhas):
        for linha in linhas:
            if len(linha) > 0:
                if not linha.find("<-") == -1:
                    li = linha.split('<-')
                    chave = li[0]

                    if not chave.isupper():
                        return False # chave nao eh maiuscula

                    expressao = li[1]

                    chars_validos = chars_validos = string.ascii_lowercase + string.digits + "|.*()"

                    nivel_parentesis = 0
                    char_anterior = " "

                    if len(expressao) <= 1:
                        return False

                    if expressao[-1:] in "|.(" or (expressao.find("|") == -1 and expressao.find(".") == -1 and expressao.find("*") == -1):
                        return False

                    for char in expressao:
                        if char in chars_validos:
                            if (char_anterior == " " or char_anterior in "|.(") and char in "|.*)":
                                return False
                            if char_anterior == "*" and char == "*":
                                return False

                            if char == "(":
                                nivel_parentesis += 1
                            elif char == ")":
                                nivel_parentesis -= 1
                                if nivel_parentesis < 0:
                                    return False

                        char_anterior = char

                    if nivel_parentesis > 0:
                        return False

        return True
                        
                        