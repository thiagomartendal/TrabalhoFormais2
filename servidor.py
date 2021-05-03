from flask import Flask, render_template, request, redirect
from classes.Item import TipoItem
from classes.ListaDeItens import ListaDeItens
from criarItens import *

app = Flask(__name__)
listaItens = ListaDeItens()

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if request.form.get('criar-automato') == "Confirmar":
            erro, linha, textoLinha, msg, nomeAutomato, textoAutomato = criarAutomato()
            if erro is False:
                return render_template('index.html', tipoErro="AF", linha=linha, textoLinha=textoLinha, msg=msg, nomeAutomato=nomeAutomato, textoAutomato=textoAutomato)
        elif request.form.get('criar-gramatica') == "Confirmar":
            erro, linha, textoLinha, msg, nomeGramatica, textoGramatica = criarGramaticaRegular()
            if erro is False:
                return render_template('index.html', tipoErro="GR", linha=linha, textoLinha=textoLinha, msg=msg, nomeGramatica=nomeGramatica, textoGramatica=textoGramatica)
        elif request.form.get('criar-glc') == "Confirmar":
            erro, msg, nomeGramatica, textoGramatica = criarGramaticaLivreDeContexto()
            if erro is False:
                return render_template('index.html', tipoErro="GLC", msg=msg, nomeGLC=nomeGramatica, textoGLC=textoGramatica)
        elif request.form.get('criar-expressao') == "Confirmar":
            erro, msg, nomeExpressao, textoExpressao = criarExpressao()
            if erro is False:
                return render_template('index.html', tipoErro="ER", msg=msg, nomeExpressao=nomeExpressao, textoExpressao=textoExpressao)
        elif request.form.get('uniao-automato') == "Confirmar":
            uniaoInterseccaoAutomato(0)
        elif request.form.get('interseccao-automato') == "Confirmar":
            uniaoInterseccaoAutomato(1)
        elif request.form.get('abrir') == "Abrir":
            abrir()
        elif request.form.get('avaliar') == "Avaliar":
            arr = avaliar()
            return render_template('index.html', palavra=arr[0], res=arr[1])
        elif request.form.get('testar-codigo') == "Confirmar":
            codigo, tabela = reconhecerLinguagem()
            return render_template('index.html', tipo="RE", codigoFonte=codigo, tabelaSimbolos=tabela)
    return render_template('index.html')

@app.route("/editar", methods=['GET', 'POST'])
def editar():
    if request.args.get('tipo') == "AF":
        if request.form.get('editar-automato') == "Confirmar":
            erro, linha, textoLinha, msg, nomeAutomato, textoAutomato = editarAutomato()
            if erro is False:
                return render_template('editar.html', tipo="AF", tipoErro="AF", linha=linha, textoLinha=textoLinha, msg=msg, nomeAutomato=nomeAutomato, textoAutomato=textoAutomato)
        arr = retornarTextoAutomato()
        return render_template('editar.html', tipo="AF", nomeAutomato=arr[0], textoAutomato=arr[1], posicao=arr[2])
    elif request.args.get('tipo') == "GR":
        if request.form.get('editar-gramatica') == "Confirmar":
            erro, linha, textoLinha, msg, nomeGramatica, textoGramatica = editarGramatica()
            if erro is False:
                return render_template('editar.html', tipo="GR", tipoErro="GR", linha=linha, textoLinha=textoLinha, msg=msg, nomeGramatica=nomeGramatica, textoGramatica=textoGramatica)
        arr = retornarTextoGramatica()
        return render_template('editar.html', tipo="GR", nomeGramatica=arr[0], textoGramatica=arr[1], posicao=arr[2])
    elif request.args.get('tipo') == "GLC":
        if request.form.get('editar-glc') == "Confirmar":
            erro, msg, nomeGramatica, textoGramatica = editarGLC()
            if erro is False:
                return render_template('editar.html', tipo="GLC", tipoErro="GLC", msg=msg, nomeGramatica=nomeGramatica, textoGramatica=textoGramatica)
        arr = retornarTextoGLC()
        return render_template('editar.html', tipo="GLC", nomeGramatica=arr[0], textoGramatica=arr[1], posicao=arr[2])
    elif request.args.get('tipo') == "ER":
        if request.form.get('editar-expressao') == "Confirmar":
            erro, msg, nomeExpressao, textoExpressao = editarExpressao()
            if erro is False:
                return render_template('editar.html', tipo="ER", tipoErro="ER", msg=msg, nomeExpressao=nomeExpressao, textoExpressao=textoExpressao)
        arr = retornarTextoExpressao()
        return render_template('editar.html', tipo="ER", nomeExpressao=arr[0], textoExpressao=arr[1], posicao=arr[2])
    return render_template('editar.html')

@app.route("/exibir", methods=['GET', 'POST'])
def exibir():
    if request.args.get('tipo') == "AF":
        arr = retornarAutomato()
        return render_template('exibir.html', nomeAutomato=arr[0], simbolosAutomato=arr[1], dicionario=arr[2], tipo="AF")
    elif request.args.get('tipo') == "GR":
        arr = retornarTextoGramatica()
        txt = "<br />".join(arr[1].split("\n"))
        return render_template('exibir.html', nomeGramatica=arr[0], textoGramatica=txt, tipo="GR")
    elif request.args.get('tipo') == "ER":
        arr = retornarTextoExpressao()
        txt = "<br />".join(arr[1].split("\n"))
        return render_template('exibir.html', nomeExpressao=arr[0], textoExpressao=txt, tipo="ER")
    elif request.args.get('tipo') == "GLC":
        arr = retornarTextoGramatica()
        txt = "<br />".join(arr[1].split("\n"))
        return render_template('exibir.html', nomeGramatica=arr[0], textoGramatica=txt, tipo="GLC")
    return render_template('exibir.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    item = listaItens.getItem(int(pos))
    nome = item.get_nome()+".txt"
    salvar(item)
    return redirect("/")

@app.route('/min')
def minimizar():
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    item = listaItens.getItem(int(pos))
    automato = None
    if item.deterministico():
        automato = item
    else:
        automato = item.determinizar()
    automatoMinimizado = automato.minimizar()
    automatoMinimizado.ordenarTransicoes()
    listaItens.getLista()[int(pos)] = automatoMinimizado
    return redirect("/")

@app.route('/det')
def determinizar():
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    item = listaItens.getItem(int(pos))
    automatoDeterminizado = item.determinizar()
    automatoDeterminizado.ordenarTransicoes()
    listaItens.getLista()[int(pos)] = automatoDeterminizado
    return redirect("/")

@app.route('/converter')
def converterItens():
    defaultI = ""
    defaultT = ""
    pos = request.args.get('pos', defaultI)
    tipo = request.args.get('tipoConversao', defaultT)
    item = listaItens.getItem(int(pos))
    novoItem = None
    if tipo == "AFGR":
        novoItem = item.conversaoEmGR()
    elif tipo == "GRAF":
        novoItem = item.conversaoEmAFND()
        novoItem.ordenarTransicoes()
    elif tipo == "ERAF":
        novoItem = item.obter_automato_finito_equivalente()
        novoItem.ordenarTransicoes()
    listaItens.getLista()[int(pos)] = novoItem
    return redirect("/")

@app.context_processor
def itens():
    itens = []
    for i in range(len(listaItens.getLista())):
        item = listaItens.getItem(i)
        tipo = None
        if item.get_tipo() == TipoItem.AF:
            tipo = "AF"
        elif item.get_tipo() == TipoItem.GR:
            tipo = "GR"
        elif item.get_tipo() == TipoItem.ER:
            tipo = "ER"
        elif item.get_tipo() == TipoItem.GLC:
            tipo = "GLC"
        itens.append([item.get_nome(), tipo, i])
    return {'itens': itens}

if __name__ == '__main__':
    app.run(debug=True)
