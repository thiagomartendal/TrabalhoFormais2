from GLC import GLC
from Item import Item, TipoItem

print()
print("--------------")
print()

glc = """
S,A,B,C,D
a,c,d,e,f
S -> AC | BC
A -> aD | cC
B -> aB | dD
C -> eC | eA
D -> fD | CB
"""

gramatica = GLC("Teste")
gramatica.parse(glc)
gramatica.fatorar()

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
S,A,B
a,b
S -> aSB | aSA
A -> a
B -> b
"""

gramatica1 = GLC("Teste")
gramatica1.parse(glc1)
gramatica1.fatorar()

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

# Gramática problemática

glc2 = """
S,B,D
b,c,d
S -> bcD | Bcd
B -> bB|b
D -> dD|d
"""

gramatica2 = GLC("Teste")
gramatica2.parse(glc2)
gramatica2.fatorar()

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
