from flask import Flask, render_template, request, redirect
from classes.Item import TipoItem
from classes.ListaDeItens import ListaDeItens
from criarItens import *
import pickle

app = Flask(__name__)
listaItens = ListaDeItens()

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.form.get('criar-automato') == "Confirmar":
        criarAutomato()
    elif request.form.get('criar-gramatica') == "Confirmar":
        criarGramatica()
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
    return render_template('exibir.html')

@app.route("/salvar", methods=['GET', 'POST'])
def salvar():
    default = ""
    pos = request.args.get('pos', default)
    item = listaItens.getItem(int(pos))
    with open(item.get_nome()+'.pkl', 'wb') as output:
        pickle.dump(item, output, pickle.HIGHEST_PROTOCOL)
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
