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
            criarAutomato()
        elif request.form.get('criar-gramatica') == "Confirmar":
            criarGramatica()
        elif request.form.get('criar-expressao') == "Confirmar":
            criarExpressao()
        elif request.form.get('abrir') == "Abrir":
            abrir()
        elif request.form.get('avaliar') == "Avaliar":
            arr = avaliar()
            return render_template('index.html', palavra=arr[0], res=arr[1])
    return render_template('index.html')

@app.route("/editar", methods=['GET', 'POST'])
def edicaoAutomato():
    if request.args.get('tipo') == "AF":
        editarAutomato()
        arr = retornarTextoAutomato()
        return render_template('editar.html', tipo="AF", nomeAutomato=arr[0], textoAutomato=arr[1], posicao=arr[2])
    elif request.args.get('tipo') == "GR":
        editarGramatica()
        arr = retornarTextoGramatica()
        return render_template('editar.html', tipo="GR", nomeGramatica=arr[0], textoGramatica=arr[1], posicao=arr[2])
    elif request.args.get('tipo') == "ER":
        editarExpressao()
        arr = retornarTextoExpressao()
        print(arr)
        return render_template('editar.html', tipo="ER", nomeExpressao=arr[0], textoExpressao=arr[1], posicao=arr[2])
    return render_template('editar.html')

@app.route("/exibir", methods=['GET', 'POST'])
def exibir():
    if request.args.get('tipo') == "AF":
        arr = retornarAutomato()
        return render_template('exibir.html', nomeAutomato=arr[0], simbolosAutomato=arr[1], transicoes=arr[2], dicionario=arr[3], tipo="AF")
    elif request.args.get('tipo') == "GR":
        arr = retornarTextoGramatica()
        txt = "<br />".join(arr[1].split("\n"))
        return render_template('exibir.html', nomeGramatica=arr[0], textoGramatica=txt, tipo="GR")
    elif request.args.get('tipo') == "ER":
        arr = retornarTextoExpressao()
        txt = "<br />".join(arr[1].split("\n"))
        return render_template('exibir.html', nomeExpressao=arr[0], textoExpressao=txt, tipo="ER")
    return render_template('exibir.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    item = listaItens.getItem(int(pos))
    nome = item.get_nome()+".txt"
    salvar(item)
    return redirect("/")

@app.route('/det')
def determinizar():
    defaultI = ""
    pos = request.args.get('pos', defaultI)
    item = listaItens.getItem(int(pos))
    automatoDeterminizado = item.determinizar()
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
    elif tipo == "ERAF":
        novoItem = item.obter_automato_finito_equivalente()
    listaItens.getLista()[int(pos)] = novoItem
    return redirect("/")

@app.route('/avaliar')
def avaliarSentenca():
    defaultI = ""
    defaultT = ""
    pos = request.args.get('pos', defaultI)
    tipo = request.args.get('tipo', defaultT)
    print(pos, tipo)
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
        itens.append([item.get_nome(), tipo, i])
    return {'itens': itens}

if __name__ == '__main__':
    app.run(debug=True)
