from flask import request
from collections import defaultdict
from classes.Estado import Estado
from classes.Automato import Automato
from classes.Transicao import Transicao
from classes.Gramatica import Gramatica
from classes.Expressao import Expressao
from classes.ListaDeItens import ListaDeItens
from classes.Item import TipoItem
import os

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
            erro, linha, textoLinha, msg = automato.reconhecerErros(texto)
            if erro is False:
                return (erro, linha, textoLinha, msg, nome, texto)
            automato.parse(texto)
            listaItens.adicionaItem(automato)
    return (True, 0, "", "", "", "")

def criarGramatica():
    if request.method == 'POST':
        if request.form.get('criar-gramatica') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            nome = request.form.get('nome-gramatica', defaultN)
            texto = request.form.get('texto-gramatica', defaultT)
            gramatica = Gramatica(nome)
            erro1, linha1, textoLinha1, msg1 = gramatica.reconhecerErros(texto)
            if erro1 is False:
                return (erro1, linha1, textoLinha1, msg1, nome, texto)
            erro2, linha2, textoLinha2, msg2 = gramatica.parse(texto)
            if erro2 is False:
                print("Houve um erro.")
                return (erro2, linha2, textoLinha2, msg2, nome, texto)
            listaItens.adicionaItem(gramatica)
    return (True, 0, "", "", "", "")

def criarExpressao():
    if request.method == 'POST':
        if request.form.get('criar-expressao') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            nome = request.form.get('nome-expressao', defaultN)
            texto = request.form.get('texto-expressao', defaultT)
            expressao = Expressao(nome)
            erro, msg = expressao.parse(texto)
            if erro is False:
                return (erro, msg, nome, texto)
            listaItens.adicionaItem(expressao)
    return (True, "", "", "")

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

def editarExpressao():
    if request.method == 'POST':
        if request.form.get('editar-expressao') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            defaultI = ""
            nome = request.form.get('nome-expressao', defaultN)
            texto = request.form.get('texto-expressao', defaultT)
            pos = request.args.get('pos', defaultI)
            expressao = listaItens.getItem(int(pos))
            expressao.set_nome(nome)
            expressao.parse(texto)
            listaItens.getLista()[int(pos)] = expressao

def retornarTextoExpressao():
    global listaItens
    default = ""
    pos = request.args.get('pos', default)
    nomeExpressao = ""
    textoExpressao = ""
    if pos != "":
        expressao = listaItens.getItem(int(pos))
        txt = ""
        if expressao.getValido():
            txt = expressao.to_string()
        nomeExpressao = expressao.get_nome()
        textoExpressao = txt
    return [nomeExpressao, textoExpressao, pos]

def retornarAutomato():
    global listaItens
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    automato = listaItens.getItem(int(pos))
    dic = defaultdict(list)
    for e in automato.getEstados():
        partida = ""
        if e.getTipo() == 0:
            partida += "->"
        elif e.getTipo() == 2:
            partida += "*"
        elif e.getTipo() == 3:
            partida += "->*"
        partida += e.getNome()
        # print(partida)
        for s in automato.getSimbolos():
            if automato.contemTransicao(e, s) is True:
                transicao = automato.getTransicao(e, s)
                chegada = "{"
                for i in range(len(transicao.getEstadosChegada())):
                    estado = transicao.getEstadosChegada()[i]
                    chegada += estado.getNome()
                    if i < len(transicao.getEstadosChegada())-1:
                        chegada += ","
                chegada += "}"
                if len(dic[partida]) <= len(automato.getSimbolos()):
                    dic[partida].append(chegada)
            else:
                if len(dic[partida]) <= len(automato.getSimbolos()):
                    dic[partida].append("")
    return [automato.get_nome(), automato.getSimbolos(), dic]

def abrir():
    if request.method == 'POST':
        global listaItens
        arquivo = request.files['arquivo']
        nomeArquivo = arquivo.filename
        local = os.path.abspath(nomeArquivo)
        f = open(local, "r")
        i = 1
        tipo = ""
        conteudo = ""
        for linha in f:
            if i == 1:
                tipo = linha
                tipo = tipo.rstrip("\n")
            else:
                conteudo += linha
            i += 1
        f.close()
        nomeArquivo = nomeArquivo.split('.')[0]
        if tipo == "AF":
            automato = Automato(nomeArquivo)
            automato.parse(conteudo)
            listaItens.adicionaItem(automato)
        elif tipo == "GR":
            gramatica = Gramatica(nomeArquivo)
            gramatica.parse(conteudo)
            listaItens.adicionaItem(gramatica)
        elif tipo == "ER":
            expressao = Expressao(nomeArquivo)
            expressao.parse(conteudo)
            listaItens.adicionaItem(expressao)

def salvar(item):
    global listaItens
    conteudo = ""
    if item.get_tipo() == TipoItem.AF:
        conteudo += "AF\n"
        arr = retornarTextoAutomato()
        conteudo += arr[1]
    elif item.get_tipo() == TipoItem.GR:
        conteudo += "GR\n"
        arr = retornarTextoGramatica()
        conteudo += arr[1]
    elif item.get_tipo() == TipoItem.ER:
        conteudo += "ER\n"
        arr = retornarTextoExpressao()
        conteudo += arr[1]
    f = open(item.get_nome()+".txt", "w")
    f.write(conteudo)
    f.close()

def avaliar():
    global listaItens
    if request.method == 'POST':
        defaultI = ""
        defaultP = ""
        pos = request.args.get('pos', defaultI)
        palavra = request.form.get('sentenca', defaultP)
        automato = listaItens.getItem(int(pos))
        if automato.deterministico():
            automato = automato.determinizar()
        reconhece = automato.reconhecimento(palavra)
        return [palavra, reconhece]
    return [None, None]

def uniaoInterseccaoAutomato(tipo):
    global listaItens
    if request.method == 'POST':
        defaultP1 = ""
        defaultP2 = ""
        posAutomato1 = request.form.get('automato1', defaultP1)
        posAutomato2 = request.form.get('automato2', defaultP2)
        automato1 = listaItens.getItem(int(posAutomato1))
        automato2 = listaItens.getItem(int(posAutomato2))
        automato3 = None
        if tipo == 0:
            automato3 = automato1.uniao(automato2)
        elif tipo == 1:
            automato3 = automato1.intersecao(automato2)
        listaItens.getLista()[int(posAutomato1)] = automato3
        listaItens.removeItem(int(posAutomato2))
