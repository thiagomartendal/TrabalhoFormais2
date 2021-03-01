from flask import request
from collections import defaultdict
from classes.Estado import Estado
from classes.Automato import Automato
from classes.Transicao import Transicao
from classes.Gramatica import Gramatica
from classes.ListaDeItens import ListaDeItens

listaItens = ListaDeItens()

def criarAutomato():
    if request.method == 'POST':
        if request.form.get('criar-automato') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            nome = request.form.get('nome-automato', defaultN)
            texto = request.form.get('texto-automato', defaultT)
            automato = Automato(nome)
            automato.parse(texto)
            listaItens.adicionaItem(automato)

def criarGramatica():
    if request.method == 'POST':
        if request.form.get('criar-gramatica') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            nome = request.form.get('nome-gramatica', defaultN)
            texto = request.form.get('texto-gramatica', defaultT)
            gramatica = Gramatica(nome)
            gramatica.parse(texto)
            listaItens.adicionaItem(gramatica)

def editarAutomato():
    if request.method == 'POST':
        if request.form.get('editar-automato') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            defaultI = ""
            nome = request.form.get('nome-automato', defaultN)
            texto = request.form.get('texto-automato', defaultT)
            pos = request.args.get('pos', defaultI)
            automato = listaItens.getItem(int(pos))
            automato.set_nome(nome)
            automato.parse(texto)
            listaItens.getLista()[int(pos)] = automato

def retornarTextoAutomato():
    global listaItens
    default = ""
    pos = request.args.get('pos', default)
    nomeAutomato = ""
    textoAutomato = ""
    if pos != "":
        automato = listaItens.getItem(int(pos))
        nomeAutomato = automato.get_nome()
        for estado in automato.getEstados():
            tipo = ""
            if estado.getTipo() == 0:
                tipo = "I"
            elif estado.getTipo() == 1:
                tipo = "N"
            elif estado.getTipo() == 2:
                tipo = "F"
            elif estado.getTipo() == 3:
                tipo = "IF"
            textoAutomato += estado.getNome()+","+tipo+"\n"
        textoAutomato += "-\n"
        for j in range(len(automato.getTransicoes())):
            transicao = automato.getTransicoes()[j]
            textoAutomato += transicao.getEstadoPartida().getNome()+","+transicao.getSimbolo()+","
            for i in range(len(transicao.getEstadosChegada())):
                estado2 = transicao.getEstadosChegada()[i]
                textoAutomato += estado2.getNome()
                if i < len(transicao.getEstadosChegada())-1:
                    textoAutomato += "."
            if j < len(automato.getTransicoes())-1:
                textoAutomato += "\n"
    return [nomeAutomato, textoAutomato, pos]

def editarGramatica():
    if request.method == 'POST':
        if request.form.get('editar-gramatica') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            defaultI = ""
            nome = request.form.get('nome-gramatica', defaultN)
            texto = request.form.get('texto-gramatica', defaultT)
            pos = request.args.get('pos', defaultI)
            gramatica = listaItens.getItem(int(pos))
            gramatica.set_nome(nome)
            gramatica.parse(texto)
            listaItens.getLista()[int(pos)] = gramatica

def retornarTextoGramatica():
    global listaItens
    default = ""
    pos = request.args.get('pos', default)
    nomeGramatica = ""
    textoGramatica = ""
    if pos != "":
        gramatica = listaItens.getItem(int(pos))
        txt = ""
        dicionario = gramatica.getProducoes().items()
        for k, v in dicionario:
            txt += str(k)+"->"+str(v)+"\n"
        txt = txt.replace("[", "")
        txt = txt.replace("]", "")
        txt = txt.replace("'", "")
        txt = txt.replace(", ", "|")
        nomeGramatica = gramatica.get_nome()
        textoGramatica = txt
    return [nomeGramatica, textoGramatica, pos]

def retornarAutomato():
    global listaItens
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    automato = listaItens.getItem(int(pos))
    transicoes = []
    dic = defaultdict(list)
    for transicao in automato.getTransicoes():
        partida = ""
        if transicao.getEstadoPartida().getTipo() == 0:
            partida += "->"
        elif transicao.getEstadoPartida().getTipo() == 2:
            partida += "*"
        elif transicao.getEstadoPartida().getTipo() == 3:
            partida += "->*"
        partida += transicao.getEstadoPartida().getNome()
        chegada = "{"
        for i in range(len(transicao.getEstadosChegada())):
            estado = transicao.getEstadosChegada()[i]
            chegada += estado.getNome()
            if i < len(transicao.getEstadosChegada())-1:
                chegada += ","
        chegada += "}"
        dic[partida].append(chegada)
        transicoes.append([partida, transicao.getSimbolo(), chegada])
    print(dic)
    return [automato.get_nome(), automato.getSimbolos(), transicoes, dic]
