from flask import request
from collections import defaultdict
from classes.Estado import Estado
from classes.Automato import Automato
from classes.Transicao import Transicao
from classes.Gramatica import Gramatica
from classes.GLC import GLC
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

def criarGramaticaRegular():
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
                return (erro2, linha2, textoLinha2, msg2, nome, texto)
            listaItens.adicionaItem(gramatica)
    return (True, 0, "", "", "", "")

def criarGramaticaLivreDeContexto():
    if request.method == 'POST':
        if request.form.get('criar-glc') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            nome = request.form.get('nome-glc', defaultN)
            texto = request.form.get('texto-glc', defaultT)
            gramatica = GLC(nome)
            erro, msg = gramatica.parse(texto)
            if erro is False:
                return (erro, msg, nome, texto)
            listaItens.adicionaItem(gramatica)
    return (True, "", "", "")

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
            erro, linha, textoLinha, msg = automato.reconhecerErros(texto)
            if erro is False:
                return (erro, linha, textoLinha, msg, nome, texto)
            automato.set_nome(nome)
            automato.parse(texto)
            listaItens.getLista()[int(pos)] = automato
    return (True, 0, "", "", "", "")

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
            erro1, linha1, textoLinha1, msg1 = gramatica.reconhecerErros(texto)
            if erro1 is False:
                return (erro1, linha1, textoLinha1, msg1, nome, texto)
            erro2, linha2, textoLinha2, msg2 = gramatica.parse(texto)
            if erro2 is False:
                return (erro2, linha2, textoLinha2, msg2, nome, texto)
            listaItens.getLista()[int(pos)] = gramatica
    return (True, 0, "", "", "", "")

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
            # print(k, v)
            corpo = ""
            for i in range(len(v)):
                if i < (len(v)-1):
                    corpo += str(v[i])+"|"
                else:
                    corpo += str(v[i])
            txt += str(k)+"->"+corpo+"\n"
        # txt = txt.replace("[", "")
        # txt = txt.replace("]", "")
        # txt = txt.replace("'", "")
        # txt = txt.replace(", ", "|")
        nomeGramatica = gramatica.get_nome()
        textoGramatica = txt
    return [nomeGramatica, textoGramatica, pos]

def editarGLC():
    if request.method == 'POST':
        if request.form.get('editar-glc') == "Confirmar":
            global listaItens
            defaultN = ""
            defaultT = ""
            defaultI = ""
            nome = request.form.get('nome-glc', defaultN)
            texto = request.form.get('texto-glc', defaultT)
            pos = request.args.get('pos', defaultI)
            gramatica = listaItens.getItem(int(pos))
            gramatica.set_nome(nome)
            erro, msg = gramatica.parse(texto)
            if erro is False:
                return (erro, msg, nome, texto)
            listaItens.getLista()[int(pos)] = gramatica
    return (True, "", "", "")

def retornarTextoGLC():
    global listaItens
    default = ""
    pos = request.args.get('pos', default)
    nomeGramatica = ""
    textoGramatica = ""
    if pos != "":
        gramatica = listaItens.getItem(int(pos))
        nomeGramatica = gramatica.get_nome()
        textoGramatica = gramatica.getTextoFormacao()
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
            erro, msg = expressao.parse(texto)
            if erro is False:
                return (erro, msg, nome, texto)
            listaItens.getLista()[int(pos)] = expressao
    return (True, "", "", "")

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

def reconhecerLinguagem():
    defaultC = ""
    codigo = request.form.get('texto-codigo', defaultC)
    copiaCodigo = codigo
    codigo = codigo.lower()
    linhas = codigo.splitlines()
    palavras = []
    for linha in linhas:
        quebra = linha.split(" ")
        for p in quebra:
            if p != '':
                palavras.append(p)

    expressaoLinguagem1 = "program|if|else|for|while|void|int|double|string|char|float|return|+|-|/|'*'|=|<|>|==|<=|>=|'('|')'|{|}|\"|\'|;|,"
    expressaoLinguagem2 = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9"
    expressao1 = Expressao("Palavras Reservadas")
    expressao1.parse(expressaoLinguagem1)
    expressao2 = Expressao("Letras e Numeros")
    expressao2.parse(expressaoLinguagem2)
    automato1 = expressao1.obter_automato_finito_equivalente() # Verifica se é uma palavra reservada
    automato2 = expressao2.obter_automato_finito_equivalente() # Verifica se é uma palavra comum
    # Monta a tabela de significa para cada palavra
    tabela = []
    for i in range(len(palavras)):
        palavra = palavras[i]
        reconhecePalavraReservada = automato1.reconhecimento(palavra)
        reconheceLetraNumero = automato2.reconhecimento(palavra)
        nomeProprio = False
        if reconheceLetraNumero is True and reconhecePalavraReservada is False:
            if (i < len(palavras)-1) and palavras[i+1] == "=":
                tabela.append([palavra, "ID", "Nome da Variável"])
                nomeProprio = True
            elif (i > 0) and (palavras[i-1] == "void" or palavras[i-1] == "int" or
            palavras[i-1] == "double" or palavras[i-1] == "float" or
            palavras[i-1] == "string" or palavras[i-1] == "char" or
            palavras[i-1] == "return" or palavras[i-1] == "+" or
            palavras[i-1] == "-" or palavras[i-1] == "*" or palavras[i-1] == "/"):
                if i < (len(palavras)-1):
                    if palavras[i+1] == "(":
                        tabela.append([palavra, "ID", "Nome da Função"])
                    else:
                        tabela.append([palavra, "ID", "Nome da Variável"])
                else:
                    tabela.append([palavra, "ID", "Nome da Variável"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '<' or palavras[i+1] == '<'):
                tabela.append([palavra, "V", "Valor comparado"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '>' or palavras[i+1] == '>'):
                tabela.append([palavra, "V", "Valor comparado"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '==' or palavras[i+1] == '=='):
                tabela.append([palavra, "V", "Valor comparado"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '<=' or palavras[i+1] == '<='):
                tabela.append([palavra, "V", "Valor comparado"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '>=' or palavras[i+1] == '>='):
                tabela.append([palavra, "V", "Valor comparado"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '='):
                if palavras[i+1] == '(':
                    tabela.append([palavra, "ID", "Nome da Função"])
                else:
                    tabela.append([palavra, "V", "Valor atribuído"])
                nomeProprio = True
            elif (i > 0) and (i < (len(palavras)-1)) and (palavras[i-1] == '(' or palavras[i-1] == ',' or palavras[i+1] == ',' or palavras[i+1] == ')'):
                tabela.append([palavra, "V", "Valor passado"])
                nomeProprio = True
            elif (i > 0) and (palavras[i-1] == '"'):
                if i < (len(palavras)-1):
                    if palavras[i+1] == "\"":
                        tabela.append([palavra, "PL", "String"])
                    else:
                        tabela.append([palavra, "PLN", "String não fechada"])
                else:
                    tabela.append([palavra, "PLN", "String não fechada"])
                nomeProprio = True
            elif (i > 0) and (palavras[i-1] == '\''):
                if i < (len(palavras)-1):
                    if palavras[i+1] == "\'":
                        tabela.append([palavra, "C", "Caractere"])
                    else:
                        tabela.append([palavra, "CN", "Caractere não fechado"])
                else:
                    tabela.append([palavra, "CN", "Caractere não fechado"])
                nomeProprio = True
        if reconhecePalavraReservada is True:
            simboloFinal = automato1.ultimoSimboloReconhecido()
            if len(palavra) == 1:
                if simboloFinal == '+':
                    tabela.append([palavra, "AD", "Operador de adição"])
                elif simboloFinal == '-':
                    tabela.append([palavra, "SB", "Operador de subtração"])
                elif simboloFinal == '/':
                    tabela.append([palavra, "DV", "Operador de divisão"])
                elif simboloFinal == '*':
                    tabela.append([palavra, "ML", "Operador de multiplicação"])
                elif simboloFinal == '=':
                    tabela.append([palavra, "AT", "Atribuição"])
                elif simboloFinal == '<':
                    tabela.append([palavra, "MN", "Menor"])
                elif simboloFinal == '>':
                    tabela.append([palavra, "MA", "Maior"])
                elif simboloFinal == '(':
                    tabela.append([palavra, "PA", "Parenteses de abertura"])
                elif simboloFinal == ')':
                    tabela.append([palavra, "PF", "Parenteses de fechamento"])
                elif simboloFinal == '{':
                    tabela.append([palavra, "CA", "Chave de abertura"])
                elif simboloFinal == '}':
                    tabela.append([palavra, "CF", "Chave de fechamento"])
                elif simboloFinal == '"':
                    tabela.append([palavra, "AS", "Aspa"])
                elif simboloFinal == "'":
                    tabela.append([palavra, "AP", "Apóstrofo"])
                elif simboloFinal == ";":
                    tabela.append([palavra, "FS", "Fim de sentença"])
                elif simboloFinal == ",":
                    tabela.append([palavra, "SS", "Separador de sentença"])
                else:
                    tabela.append([palavra, "ER", "Erro: Símbolo desconhecido"])
            else:
                if palavra[0] == 'p' and simboloFinal == 'm':
                    tabela.append([palavra, "PR", "Declaração de programa"])
                elif (i > 0) and palavras[i-1] == "else" and palavra[0] == 'i' and simboloFinal == 'f':
                    tabela.append([palavras[i-1]+" "+palavra, "EF", "Nova condição na estrutura condicional"])
                elif palavra[0] == 'i' and simboloFinal == 'f':
                    tabela.append([palavra, "IF", "Inicio de estrutura condicional"])
                elif palavra[0] == 'e' and simboloFinal == 'e':
                    tabela.append([palavra, "EL", "Nova condição na estrutura condicional"])
                elif palavra[0] == 'f' and simboloFinal == 'r':
                    tabela.append([palavra, "FR", "Laço de repetição"])
                elif palavra[0] == 'w' and simboloFinal == 'e':
                    tabela.append([palavra, "WE", "Laço de repetição"])
                elif palavra[0] == 'v' and simboloFinal == 'd':
                    tabela.append([palavra, "VD", "Tipo vazio"])
                elif palavra[0] == 'i' and simboloFinal == 't':
                    tabela.append([palavra, "IT", "Tipo numérico"])
                elif palavra[0] == 'd' and simboloFinal == 'e':
                    tabela.append([palavra, "DE", "Tipo numérico"])
                elif palavra[0] == 'f' and simboloFinal == 't':
                    tabela.append([palavra, "FT", "Tipo numérico"])
                elif palavra[0] == 's' and simboloFinal == 'g':
                    tabela.append([palavra, "ST", "Tipo de texto"])
                elif palavra[0] == 'c' and simboloFinal == 'r':
                    tabela.append([palavra, "CR", "Caractere"])
                elif palavra[0] == 'r' and simboloFinal == 'n':
                    tabela.append([palavra, "RE", "Declaração de retorno"])
                elif palavra[0] == '=' and simboloFinal == '=':
                    tabela.append([palavra, "IG", "Igualdade"])
                elif palavra[0] == '<' and simboloFinal == '=':
                    tabela.append([palavra, "MI", "Menor ou igual"])
                elif palavra[0] == '>' and simboloFinal == '=':
                    tabela.append([palavra, "AI", "Maior ou igual"])
                else:
                    tabela.append([palavra, "ER", "Erro: Símbolo Desconhecido"])
        else:
            if nomeProprio is False:
                tabela.append([palavra, "ER", "Erro: Símbolo desconhecido"])

    return copiaCodigo, tabela
