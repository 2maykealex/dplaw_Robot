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
from werkzeug.utils import secure_filename
import pandas as pd
from itertools import chain

UPLOAD_FOLDER = 'E:\\DESENVOLVIMENTO\\PYTHON\\dplaw_Robot\\web\\arquivos_importados'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route("/defining", methods=['POST'])
def defining():
    data = request.form.to_dict()

    # if (len(request.files) > 0):
    file = request.files['arquivo']
    filename = secure_filename(file.filename)
    newPathFile = path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(newPathFile)
    df = pd.read_excel(newPathFile)

    # url = request.referrer
    itensPadroes = {}
    registros    = {}
    base         = {}

    #separando base e padrões
    for k, item in data.items():
        if k in ['clientePadrao', 'grupoPadrao', 'siglaPadrao', 'tipo', 'funcao']:
            base[k] = item.strip()
        else:
            itensPadroes[k] = item
    registros.update(base)

    recNum = 1
    regs={}
    for registro in df.values:
        itemDict = {}
        agendamentos = {}
        parteAdversa = {}

        if (base['tipo'] == 'atualizacao'):
            if base['funcao'] == 'volumetria':
                itemDict = {'txtPasta':registro[7]}
            elif base['funcao'] == 'contrato':
                itemDict = {'txtPasta':registro[1]}

        elif (base['tipo'] == 'abertura'):
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
            rota = 'abertura_default'
            if base['funcao'] == 'bradesco_arquivo':
                try: #ARQUIVO enviado pelo BRADESCO
                    localidade = registro[4]
                    itemDict['txtPasta'] = registro[0]
                    if (registro[1] != ''):
                        parteAdversa['txtNome']  = registro[1]
                        itemDict['parteAdversa'] = parteAdversa
                    itemDict['dataAbertura']   = registro[2]
                    itemDict['txtNroProcesso'] = registro[3]
                    itemDict['txtNroCnj']      = registro[3]
                    itemDict['slcNumeroVara']  = localidade.split('/')[0]  #registro[4]
                    itemDict['slcComarca']     = localidade.split('/')[1].strip()
                    itemDict['txtUf']          = localidade.split('/')[-1]

                    if (type(registro[5]) == type(str()) and registro[5] != ''):
                        agendamentos['Audiência'] = registro[5]
                        itemDict['agendamentos']  = agendamentos
                except: #arquivo gerado do TEXTO enviado pelo BRADESCO
                    print('TEXTO enviado pelo BRADESCO')
                    itemDict['txtPasta'] = registro[0].split('      ')[0].strip()
                    if (registro[0][1] != ''):
                        parteAdversa['txtNome']  = registro[0].split('/')[0][:-2].strip().split('      ')[1].strip()
                        itemDict['parteAdversa'] = parteAdversa

                    itemDict['dataAbertura']   = registro[0][(int(registro[0].find('/'))-2):((int(registro[0].find('/'))-2)+10)].strip()
                    itemDict['txtNroProcesso'] = registro[0].split('/')[2].split('      ')[-1].split('    ')[0]
                    itemDict['txtNroCnj']      = registro[0].split('/')[2].split('      ')[-1].split('    ')[0]
                    try:
                        if (int(registro[0].split('/')[2].split('      ')[1].split('    ')[1].split(' ')[0])):
                            itemDict['slcNumeroVara']   = "{} ª-º".format(int(registro[0].split('/')[2].split('      ')[1].split('    ')[1].split(' ')[0]))
                            itemDict['slcLocalTramite'] = registro[0].split('/')[2].split('      ')[1].split('    ')[1][3:]
                    except:
                        itemDict['slcLocalTramite'] = registro[0].split('/')[2].split('      ')[-1].split('    ')[1]
                    itemDict['slcComarca'] = registro[0].split('/')[3]
                    itemDict['txtUf']      = registro[0].split('/')[4][:2].strip()

                    try:
                        if (int(registro[0].strip()[-2:])):
                            agendamentos['Audiência'] = registro[0].strip()[-10:].strip()
                    except:
                        pass
                    if (len(agendamentos)>0):
                        itemDict['agendamentos']  = agendamentos

            elif base['funcao'] == 'bv':
                itemDict['txtPasta']    = registro[0]
                if (registro[1] != ''):
                    parteAdversa['txtNome']  = registro[1]
                    itemDict['parteAdversa'] = parteAdversa
                itemDict['txtNroProcesso']  = registro[2]
                itemDict['txtNroCnj']       = registro[2]
                itemDict['slcNumeroVara']   = "{} ª-º".format(registro[3].split('ª')[0])
                itemDict['slcLocalTramite'] = registro[4].split(' DE ')[0]
                itemDict['slcComarca']  = registro[5].strip()
                itemDict['txtUf']       = registro[6]

                if (type(registro[7]) == type(str()) and registro[7] != ''):
                    agendamentos['Audiência'] = registro[7]

                if (type(registro[8]) == type(str()) and registro[8] != ''):
                    agendamentos['HoraAudiencia'] = registro[8]

                if (len(agendamentos)>0):
                    itemDict['agendamentos']  = agendamentos

                itemDict['txtUf']       = registro[6]
                itemDict['txtUf']       = registro[6]

            elif base['funcao'] == 'faro':
                itemDict['txtPasta']    = registro[1]

                #ADVERSA
                if (registro[2] != ''):
                    parteAdversa['txtNome']  = registro[2].strip()
                if (registro[3] != ''):
                    parteAdversa['txtCPF']  = registro[3]
                if (registro[4] != ''):
                    parteAdversa['txtTelContato']  = registro[4]
                if (registro[5] != ''):
                    parteAdversa['txtEmail1']  = registro[5]
                if (registro[6] != ''):
                    parteAdversa['txtEndereco']  = registro[6]
                if (registro[7] != ''):
                    parteAdversa['txtProfissao']  = registro[7]

                if (len(parteAdversa) > 0):
                    itemDict['parteAdversa'] = parteAdversa

                itemDict['txtPedido'] = registro[8]

            elif base['funcao'] == 'oi':
                itemDict['txtPasta']  = registro[0]
                itemDict['txtNroCnj'] = registro[1]
                itemDict['txtNroProcesso'] = registro[2]
                itemDict['slcStatusProcessual']  = registro[3]
                itemDict['slcObjetoAcao']        = registro[4]
                itemDict['slcComarca']           = registro[5].strip()
                itemDict['txtUf']                = registro[6]
                itemDict['slcNumeroVara']        = "{} ª-º".format(registro[7])
                itemDict['slcLocalTramite']      = registro[8].split(' DE ')[0]
                itemDict['txtDataDistribuicao']  = registro[9]
                itemDict['txtDataContratacao']   = registro[10]
                itemDict['txtValorCausa']        = registro[11]
                if (type(registro[12]) == type(str() and registro[12] != '')):
                    parteAdversa['txtNome']      = registro[12]
                    itemDict['parteAdversa']     = parteAdversa
                if (registro[13] != '' and registro[13] != 'SEM AGENDAMENTO'):
                    agendamentos['Audiência']    = registro[13]
                if (registro[14] != '' and registro[14] != 'SEM AGENDAMENTO'):
                    agendamentos['HoraAudiencia'] = registro[14]
                itemDict['slcFase']               = registro[15]

        #todo VER SE VAI PULAR UMA SEMANA A CADA TANTOS REGISTROS
        if (itensPadroes):
            itemDict.update(itensPadroes)

        regs[recNum] = itemDict
        recNum = recNum + 1

    registros['registros'] = regs
    pprint(registros)

    # return redirect(url_for(rota, data=registros))
    # return redirect(url_for(rota, data=registros), code=307)
    # return 'teste'

    if (base['tipo'] == 'abertura'):
        # print('indo para abertura_default.html')
        return render_template('abertura_default.html', data=registros, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)
    # elif (base['tipo'] == 'atualizacao'):
    #     return render_template('abertura_default.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)

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

@app.route("/abertura/executa", methods=['POST', 'GET'])
@app.route("/atualizacao/executa", methods=['POST', 'GET'])
def executa():
    data = request.data
    data = request.form.to_dict()
    data = data['txtAbertura']
    data = json.loads(data)
    pprint(data)

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
    # app.run(debug=True)
    app.run(host= '192.168.0.10', debug=True)




# @app.route("/abertura/oi/default", methods=['POST'])
# @app.route("/abertura/bv/default", methods=['POST'])
# @app.route("/abertura/faro/default", methods=['POST'])
# @app.route("/abertura/bradesco/default", methods=['POST'])
# def abertura_default():
#     dados = path.dirname(getcwd())+'\\dados'
#     #importando dados base
#     clientes = dados+'\\'+'clientes.txt'
#     clientes = open(clientes, 'r')
#     gruposprocessos = dados+'\\'+'gruposprocessos.txt'
#     gruposprocessos = open(gruposprocessos, 'r')
#     locaistramites = dados+'\\'+'locaistramites.txt'
#     locaistramites = open(locaistramites, 'r')
#     localizadores = dados+'\\'+'localizadores.txt'
#     localizadores = open(localizadores, 'r')
#     responsaveis = dados+'\\'+'responsaveis.txt'
#     resp1 = open(responsaveis, 'r')
#     resp2 = open(responsaveis, 'r')
#     resp3 = open(responsaveis, 'r')
#     status = dados+'\\'+'status.txt'
#     status = open(status, 'r')
#     varas = dados+'\\'+'varas.txt'
#     varas = open(varas, 'r')
#     assuntos = dados+'\\'+'assuntos.txt'
#     assuntos = open(assuntos, 'r', encoding='utf-8')
#     detalhes = dados+'\\'+'detalhes.txt'
#     detalhes = open(detalhes, 'r', encoding='utf-8')
#     areasAtuacao = dados+'\\'+'areasAtuacao.txt'
#     areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
#     fases = dados+'\\'+'fases.txt'
#     fases = open(fases, 'r', encoding='utf-8')
#     objetosAcao = dados+'\\'+'objetosAcao.txt'
#     objetosAcao = open(objetosAcao, 'r', encoding='utf-8')

#     requested = request.data
#     print('Aqui', requested)

#     data = requested['txtAbertura']
#     data = json.loads(data)
#     try:
#         data['clientePadrao'] = requested['clientePadrao']
#     except:
#         pass

#     return render_template('abertura_default.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)