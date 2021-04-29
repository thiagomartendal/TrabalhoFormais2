from GLC import GLC

#glc = GLC("teste")
#print(glc.parse("E,T,F\n+,-,*,/,(,),id\nE -> E+T | E-T | T\nT -> T*F | T/F | F\nF -> (E) | id"))

#glc = GLC("teste")
#print(glc.parse("S',S,A,B\nc,a,b\nS' -> S | &\nS -> AB | A | B | Sc | c\nA -> aA | a\nB -> bB | b"))

#glc = GLC("teste")
#print(glc.parse("S,S',A,A'\na,b,d,c\nS -> AaS'\nS' -> bS' | &\nA -> dA'\nA' -> aS'cA' | &"))

glc = GLC("teste")
print(glc.parse("P,K,V,F,C\ne,b,c,v,f,;,com\nP -> KVC\nK -> cK | &\nV -> vV | F\nF -> fP;F | &\nC -> bVCe | com;C | &"))


'''
from Estado import Estado
from Transicao import Transicao
from Automato import Automato
from Item import Item, TipoItem

# p = Estado("p", 0)
# q = Estado("q", 2)
# r = Estado("r", 1)
# s = Estado("s", 2)
#
# t1 = Transicao(p, "0", [q, s])
# t2 = Transicao(p, "1", [q])
# t3 = Transicao(q, "0", [r])
# t4 = Transicao(q, "1", [q, r])
# t5 = Transicao(r, "0", [s])
# t6 = Transicao(r, "1", [p])
# t7 = Transicao(s, "1", [p])
#
# automato = Automato("Teste")
# automato.setEstados([p, q, r, s])
# automato.setTransicoes([t1, t2, t3, t4, t5, t6, t7])
# novo = automato.determinizar()
# for transicao in novo.getTransicoes():
#     print(transicao.getEstadoPartida().getNome(), transicao.getSimbolo(), transicao.getEstadosChegada()[0].getNome())
# print("------------------")
#
# q0 = Estado("q0", 0)
# q1 = Estado("q1", 2)
# q2 = Estado("q2", 2)
# q3 = Estado("q3", 1)
# q4 = Estado("q4", 1)
#
# l1 = Transicao(q0, "0", [q1])
# l2 = Transicao(q0, "1", [q2])
# l3 = Transicao(q1, "0", [q1, q3])
# l4 = Transicao(q1, "1", [q1])
# l5 = Transicao(q2, "0", [q2])
# l6 = Transicao(q2, "1", [q2, q4])
#
# aut = Automato("Teste")
# aut.setEstados([q0, q1, q2, q3, q4])
# aut.setTransicoes([l1, l2, l3, l4, l5, l6])
# novo2 = aut.determinizar()
# for transicao in novo2.getTransicoes():
#     print(transicao.getEstadoPartida().getNome(), transicao.getSimbolo(), transicao.getEstadosChegada()[0].getNome())
# print("------------------")
#
# e0 = Estado("p", 0)
# e1 = Estado("q", 1)
# e2 = Estado("r", 2)
#
# a1 = Transicao(e0, "&", [e0, e1])
# a2 = Transicao(e0, "b", [e1])
# a3 = Transicao(e0, "c", [e2])
# a4 = Transicao(e1, "a", [e0])
# a5 = Transicao(e1, "b", [e2])
# a6 = Transicao(e1, "c", [e0, e1])
#
# auto = Automato("Teste")
# auto.setEstados([e0, e1, e2])
# auto.setTransicoes([a1, a2, a3, a4, a5, a6])
# novo3 = auto.determinizar()
# for transicao in novo3.getTransicoes():
#     print(transicao.getEstadoPartida().getNome(), transicao.getSimbolo(), transicao.getEstadosChegada()[0].getNome())
# print("------------------")

eS = Estado("S", 0)
eA = Estado("A", 1)
eB = Estado("B", 1)
eC = Estado("C", 2)

p1 = Transicao(eS, "a", [eA, eC])
p2 = Transicao(eS, "b", [eB])
p3 = Transicao(eA, "a", [eA, eC])
p4 = Transicao(eB, "a", [eS, eB])

auto2 = Automato("Teste")
auto2.setEstados([eS, eA, eB, eC])
auto2.setTransicoes([p1, p2, p3, p4])
novo4 = auto2.determinizar()
for transicao in novo4.getTransicoes():
    print(transicao.getEstadoPartida().getNome(), transicao.getSimbolo(), transicao.getEstadosChegada()[0].getNome())'''