from flask import Flask, render_template, request, redirect, url_for, json
from collections import OrderedDict
from pprint import pprint
from os import getcwd
from os import path
from time import strftime
from integra_functions import IntegraFunctions
from basic_functions import createLog
from basic_functions import createFolder
import pyexcel as pe
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

@app.route("/abertura/faro")
def abertura_faro():
    return render_template('abertura_faro.html')

@app.route("/abertura/bv")
def abertura_bv():
    return render_template('abertura_bv.html')

@app.route("/abertura/oi")
def abertura_oi():
    return render_template('abertura_oi.html')

@app.route("/abertura/oi/default", methods=['POST'])
@app.route("/abertura/bv/default", methods=['POST'])
@app.route("/abertura/faro/default", methods=['POST'])
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
    assuntos = dados+'\\'+'assuntos.txt'
    assuntos = open(assuntos, 'r', encoding='utf-8')
    detalhes = dados+'\\'+'detalhes.txt'
    detalhes = open(detalhes, 'r', encoding='utf-8')
    areasAtuacao = dados+'\\'+'areasAtuacao.txt'
    areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
    fases = dados+'\\'+'fases.txt'
    fases = open(fases, 'r', encoding='utf-8')
    objetosAcao = dados+'\\'+'objetosAcao.txt'
    objetosAcao = open(objetosAcao, 'r', encoding='utf-8')

    requested = request.form.to_dict()
    data = requested['txtAbertura']
    data = json.loads(data)
    try:
        data['clientePadrao'] = requested['clientePadrao']
    except:
        pass

    return render_template('abertura_default.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)

@app.route("/abertura/oi/default/part2", methods=['POST'])
@app.route("/abertura/bv/default/part2", methods=['POST'])
@app.route("/abertura/faro/default/part2", methods=['POST'])
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
    assuntos = dados+'\\'+'assuntos.txt'
    assuntos = open(assuntos, 'r', encoding='utf-8')
    detalhes = dados+'\\'+'detalhes.txt'
    detalhes = open(detalhes, 'r', encoding='utf-8')
    areasAtuacao = dados+'\\'+'areasAtuacao.txt'
    areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
    fases = dados+'\\'+'fases.txt'
    fases = open(fases, 'r', encoding='utf-8')
    objetosAcao = dados+'\\'+'objetosAcao.txt'
    objetosAcao = open(objetosAcao, 'r', encoding='utf-8')

    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)
    return render_template('abertura_default_2.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)

@app.route("/abertura/executa", methods=['POST'])
@app.route("/atualizacao/executa", methods=['POST'])
def executa():
    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)

    #reordenando os registros
    newRegistros= {}
    for k, v in data['registros'].items():
        newRegistros[int(k)+1] = v

    del data['registros']
    data['registros'] = newRegistros

    # CRIANDO ARQUIVO DE LOG .CSV
    hoje = "%s" % (strftime("%Y-%m-%d"))
    hoje = hoje.replace('-', '_')
    hora = strftime("%H:%M:%S")
    hora = hora.replace(':', '_')
    pathPasta   = '{}\\arquivos_a_executar'.format(path.dirname(__file__))
    createFolder(pathPasta) # CRIA DIRETÓRIO SE NÃO EXISTIR.
    pathPasta   = '{}\\{}'.format(pathPasta, data['tipo'])
    createFolder(pathPasta) # CRIA DIRETÓRIO SE NÃO EXISTIR.

    criaArquivo = "{}\\{}__{}__{}.txt".format(pathPasta, data['siglaPadrao'], hoje, hora)
    with open(criaArquivo, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=True)

    return render_template('monitoramento.html')#TODO ENVIAR PARA ROTA!

@app.route("/monitoramento")
def monitoramento():
    return render_template('monitoramento.html')

@app.route("/atualizacao")
def atualizacao():
    return render_template('atualizacao.html')

@app.route("/atualizacao/contrato")
def atualizacao_contrato():
    return render_template('contrato.html')

@app.route("/atualizacao/volumetria")
def atualizacao_volumetria():
    return render_template('volumetria.html')

@app.route("/atualizacao/geral")
def atualizacao_geral():
    return render_template('geral.html')

if __name__ == "__main__":
    app.run(debug=True)