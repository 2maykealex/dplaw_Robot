from flask import Flask, render_template, request, redirect, url_for, json
from pprint import pprint
from os import getcwd
from os import path
from integra_functions import IntegraFunctions
# from basic_functions import abreArquivo

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/abertura")
def abertura():
    return render_template('abertura.html')

@app.route("/abertura/bradesco")
def abertura_bradesco():
    return render_template('abertura_bradesco.html')

@app.route("/abertura/bradesco/default", methods=['POST'])
def abertura_default():
    dados = path.dirname(getcwd())+'\\dados'
    #importando dados base
    clientes = dados+'\\'+'clientes.txt'
    clientes = open(clientes, 'r')
    gruposprocessos = dados+'\\'+'gruposprocessos.txt'
    gruposprocessos = open(gruposprocessos, 'r')
    locaistramites = dados+'\\'+'locaistramites.txt'
    locaistramites = open(locaistramites, 'r')
    localizadores = dados+'\\'+'localizadores.txt'
    localizadores = open(localizadores, 'r')
    responsaveis = dados+'\\'+'responsaveis.txt'
    resp1 = open(responsaveis, 'r')
    resp2 = open(responsaveis, 'r')
    resp3 = open(responsaveis, 'r')
    status = dados+'\\'+'status.txt'
    status = open(status, 'r')
    varas = dados+'\\'+'varas.txt'
    varas = open(varas, 'r')

    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)
    return render_template('abertura_default.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites)

@app.route("/abertura/bradesco/default/part2", methods=['POST'])
def abertura_default2():
    dados = path.dirname(getcwd())+'\\dados'
    #importando dados base
    clientes = dados+'\\'+'clientes.txt'
    clientes = open(clientes, 'r')
    gruposprocessos = dados+'\\'+'gruposprocessos.txt'
    gruposprocessos = open(gruposprocessos, 'r')
    locaistramites = dados+'\\'+'locaistramites.txt'
    locaistramites = open(locaistramites, 'r')
    localizadores = dados+'\\'+'localizadores.txt'
    localizadores = open(localizadores, 'r')
    responsaveis = dados+'\\'+'responsaveis.txt'
    resp1 = open(responsaveis, 'r')
    resp2 = open(responsaveis, 'r')
    resp3 = open(responsaveis, 'r')
    status = dados+'\\'+'status.txt'
    status = open(status, 'r')
    varas = dados+'\\'+'varas.txt'
    varas = open(varas, 'r')

    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)
    return render_template('abertura_default_2.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites)

@app.route("/abertura/executa", methods=['POST'])
def abertura_executa():
    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)


    data['tipo'] = 'abertura'
    # print(data)
    integra = IntegraFunctions()
    integra.controle(data)





    return render_template('atualizacao.html')

# @app.route("/abertura/monitoramento", methods='POST')
# def abertura_monitoramento():
#     return render_template('atualizacao.html')

@app.route("/atualizacao")
def atualizacao():
    return render_template('atualizacao.html')

@app.route("/contrato")
def contrato():
    return render_template('contrato.html')

@app.route("/volumetria")
def volumetria():
    return render_template('volumetria.html')

if __name__ == "__main__":
    app.run(debug=True)