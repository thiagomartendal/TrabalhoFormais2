from GLC import GLC
from Item import Item, TipoItem

print()
print("--------------")
print()

glc = """
A
a,b
A -> Aa | b
"""

gramatica = GLC("Teste")
gramatica.parse(glc)
gramatica.removerRecursaoAEsquerda()

dicionario1 = gramatica.getProducoes().items()

for cabeca, corpo in dicionario1:
    print(str(cabeca)+"->", end="")
    i = 0
    for c in corpo:
        if i < (len(corpo)-1):
            print(str(c), end="|")
        else:
            print(str(c), end="")
        i += 1
    print()

print()
print("--------------")
print()

glc1 = """
S, A, B
a,b,c
S -> Sc | Aa | c
A -> Sa | Bb | a
B -> Sc | Bb
"""

gramatica1 = GLC("Teste")
gramatica1.parse(glc1)
gramatica1.removerRecursaoAEsquerda()

dicionario2 = gramatica1.getProducoes().items()

for cabeca, corpo in dicionario2:
    print(str(cabeca)+"->", end="")
    i = 0
    for c in corpo:
        if i < (len(corpo)-1):
            print(str(c), end="|")
        else:
            print(str(c), end="")
        i += 1
    print()

print()
print("--------------")
print()

glc2 = """
S, A
a,b,c,d
S -> Aa | b
A -> Ac | Sd | a
"""

gramatica2 = GLC("Teste")
gramatica2.parse(glc2)
gramatica2.removerRecursaoAEsquerda()

dicionario3 = gramatica2.getProducoes().items()

for cabeca, corpo in dicionario3:
    print(str(cabeca)+"->", end="")
    i = 0
    for c in corpo:
        if i < (len(corpo)-1):
            print(str(c), end="|")
        else:
            print(str(c), end="")
        i += 1
    print()

print()
print("--------------")
print()

# Um pequeno problema nessa gramática

glc3 = """
S, A
a,c
S -> Sc | SA
A -> a
"""

gramatica3 = GLC("Teste")
gramatica3.parse(glc3)
gramatica3.removerRecursaoAEsquerda()

dicionario4 = gramatica3.getProducoes().items()

for cabeca, corpo in dicionario4:
    print(str(cabeca)+"->", end="")
    i = 0
    for c in corpo:
        if i < (len(corpo)-1):
            print(str(c), end="|")
        else:
            print(str(c), end="")
        i += 1
    print()
