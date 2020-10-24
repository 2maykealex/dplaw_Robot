from pprint import pprint
from os import path
import pandas as pd
from os import getcwd
from time import strftime
from basic_functions import createFolder
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, json

UPLOAD_FOLDER = path.abspath(getcwd()) + '\\arquivos_importados'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
DADOS = path.abspath(getcwd()) +'\\arquivos_necessarios'

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
    print(path.abspath(getcwd()))
    data = request.form.to_dict()
    file = request.files['arquivo']
    filename = secure_filename(file.filename)
    newPathFile = path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(newPathFile)

    df = pd.read_excel(newPathFile)
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
                itemDict = {'txtPasta':registro[7]}

        elif (base['tipo'] == 'abertura'):
            dados = path.abspath(getcwd()) +'\\arquivos_necessarios'
            #importando dados base
            clientes = DADOS +'\\'+'clientes.txt'
            clientes = open(clientes, 'r')
            gruposprocessos = DADOS +'\\'+'gruposprocessos.txt'
            gruposprocessos = open(gruposprocessos, 'r')
            locaistramites = DADOS +'\\'+'locaistramites.txt'
            locaistramites = open(locaistramites, 'r')
            localizadores = DADOS +'\\'+'localizadores.txt'
            localizadores = open(localizadores, 'r')
            responsaveis = DADOS +'\\'+'responsaveis.txt'
            resp1 = open(responsaveis, 'r')
            resp2 = open(responsaveis, 'r')
            resp3 = open(responsaveis, 'r')
            status = DADOS +'\\'+'status.txt'
            status = open(status, 'r')
            varas = DADOS +'\\'+'varas.txt'
            varas = open(varas, 'r')
            assuntos = DADOS +'\\'+'assuntos.txt'
            assuntos = open(assuntos, 'r', encoding='utf-8')
            detalhes = DADOS +'\\'+'detalhes.txt'
            detalhes = open(detalhes, 'r', encoding='utf-8')
            areasAtuacao = DADOS +'\\'+'areasAtuacao.txt'
            areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
            fases = DADOS +'\\'+'fases.txt'
            fases = open(fases, 'r', encoding='utf-8')
            objetosAcao = DADOS +'\\'+'objetosAcao.txt'
            objetosAcao = open(objetosAcao, 'r', encoding='utf-8')

            if base['funcao'] == 'bradesco_arquivo':
                print('ARQUIVO enviado pelo BRADESCO')
                itemDict['txtPasta'] = registro[0]
                if (registro[1] != ''):
                    parteAdversa['txtNome']  = registro[1]
                    itemDict['parteAdversa'] = parteAdversa
                itemDict['txtDataContratacao'] = registro[2].to_pydatetime().strftime("%d/%m/%Y")
                itemDict['txtNroProcesso'] = registro[3]
                itemDict['txtNroCnj']      = registro[3]
                itemDict['slcNumeroVara']  = registro[4].split('/')[0]  #registro[4]
                itemDict['slcComarca']     = registro[4].split('/')[1].strip()
                itemDict['txtUf']          = registro[4].split('/')[-1]

                if (type(registro[5]) == type(str()) and registro[5] != ''):
                    agendamentos['Audiência'] = registro[5]
                    itemDict['agendamentos']  = agendamentos

            elif base['funcao'] == 'bradesco_email':
                print('TEXTO enviado pelo BRADESCO')
                itemDict['txtPasta'] = registro[0].split('      ')[0].strip()
                if (registro[0][1] != ''):
                    parteAdversa['txtNome']  = registro[0].split('/')[0][:-2].strip().split('      ')[1].strip()
                    itemDict['parteAdversa'] = parteAdversa

                itemDict['txtDataContratacao'] = registro[0][(int(registro[0].find('/'))-2):((int(registro[0].find('/'))-2)+10)].strip()
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

            elif base['funcao'] == 'faro_judicial':
                itemDict['txtNroProcesso']    = registro[0]
                itemDict['txtNroCnj']    = registro[0]
                #ADVERSA
                if (registro[1] != ''):
                    parteAdversa['txtNome']  = registro[1].strip()
                if (registro[2] != ''):
                    parteAdversa['txtCPF']  = registro[2]

                if (len(parteAdversa) > 0):
                    itemDict['parteAdversa'] = parteAdversa

                if (registro[3] != ''):
                    itemDict['txtValorCausa'] = registro[3]

                try:
                    if (registro[4] != ''):
                        dataCorrigida ='{}'.format(registro[4]).split(' ')[0].split('-')
                        dataCorrigida = '{}/{}/{}'.format(dataCorrigida[2], dataCorrigida[1], dataCorrigida[0])
                        itemDict['txtDataDistribuicao']  = dataCorrigida
                except:
                    pass

                if (type(registro[5]) == type(str())):
                    itemDict['txtObservacao'] = registro[5]

                #padrões pre definidos
                itemDict['slcComarca'] = 'Porto Velho'
                itemDict['txtUf'] = 'RO'
                itemDict['txtDataDistribuicao']  = '13/10/2020'
                itemDict['txtDataContratacao']   = '13/10/2020'

            elif base['funcao'] == 'faro_alunos':
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
                itemDict['txtNroCnj'] = str(registro[1])
                itemDict['txtNroProcesso'] = str(registro[2])
                itemDict['slcStatusProcessual']  = str(registro[3])
                itemDict['slcObjetoAcao']        = registro[4]
                itemDict['slcComarca']           = registro[5].strip()
                itemDict['txtUf']                = registro[6]
                itemDict['slcNumeroVara']        = "{} ª-º".format(registro[7])
                itemDict['slcLocalTramite']      = registro[8].split(' DE ')[0]
                if (type(registro[9]) == type(str() and registro[9] != '')):
                    itemDict['txtDataDistribuicao']  = str(registro[9])
                if (type(registro[10]) == type(str() and registro[10] != '')):
                    itemDict['txtDataContratacao']   = str(registro[10])
                if (type(registro[11]) == type(str() and registro[11] != '')):
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
    # pprint(registros)
    if (base['tipo'] == 'abertura'):
        return render_template('abertura_default.html', data=registros, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)
    elif (base['tipo'] == 'atualizacao'):
        gera_arquivo_atualizacao(registros)
        return redirect(url_for('monitoramento'))

@app.route("/abertura/oi/default/part2", methods=['POST'])
@app.route("/abertura/bv/default/part2", methods=['POST'])
@app.route("/abertura/faro/default/part2", methods=['POST'])
@app.route("/abertura/bradesco/default/part2", methods=['POST'])
def abertura_default2():
    #importando dados base
    clientes = DADOS +'\\'+'clientes.txt'
    clientes = open(clientes, 'r')
    gruposprocessos = DADOS +'\\'+'gruposprocessos.txt'
    gruposprocessos = open(gruposprocessos, 'r')
    locaistramites = DADOS +'\\'+'locaistramites.txt'
    locaistramites = open(locaistramites, 'r')
    localizadores = DADOS +'\\'+'localizadores.txt'
    localizadores = open(localizadores, 'r')
    responsaveis = DADOS +'\\'+'responsaveis.txt'
    resp1 = open(responsaveis, 'r')
    resp2 = open(responsaveis, 'r')
    resp3 = open(responsaveis, 'r')
    status = DADOS +'\\'+'status.txt'
    status = open(status, 'r')
    varas = DADOS +'\\'+'varas.txt'
    varas = open(varas, 'r')
    assuntos = DADOS +'\\'+'assuntos.txt'
    assuntos = open(assuntos, 'r', encoding='utf-8')
    detalhes = DADOS +'\\'+'detalhes.txt'
    detalhes = open(detalhes, 'r', encoding='utf-8')
    areasAtuacao = DADOS +'\\'+'areasAtuacao.txt'
    areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
    fases = DADOS +'\\'+'fases.txt'
    fases = open(fases, 'r', encoding='utf-8')
    objetosAcao = DADOS +'\\'+'objetosAcao.txt'
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
    try:
        data = data['txtAbertura']
    except:
        pass
    data = json.loads(data)

    #reordenando os registros
    newRegistros= {}
    for k, v in data['registros'].items():
        newRegistros[int(k)] = v   #TODO CHECK INCREMENTO

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

def gera_arquivo_atualizacao(data):
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

@app.route("/monitoramento")
def monitoramento():
    return render_template('monitoramento.html')

# @app.route("/monitoramento/<log>", methods=['POST'])
# def monitoramento(log):
#     return render_template('log.html')

@app.route("/getLog/<filePath>", methods=['POST'])
def getLog(filePath):
    from os import walk
    files = {}
    logsPath = '{}\\logs'.format(path.dirname(__file__))
    # for folder, _subdirs, filesFolder in walk(logsPath):
    #     for name in filesFolder:
    #         tipo = folder.split('\\')[-1]
    arquivo =  open('{}'.format(filePath), 'r')
    message = arquivo.readlines()
    files = {
                name: {'tipo': tipo,
                        'path': folder,
                        'log' : message,
                }
            }
    return files
# @app.route("/getLog", methods=['POST'])
# def getLog():
#     from os import walk
#     files = {}
#     logsPath = '{}\\logs'.format(path.dirname(__file__))
#     for folder, _subdirs, filesFolder in walk(logsPath):
#         for name in filesFolder:
#             tipo = folder.split('\\')[-1]
#             arquivo =  open('{}\\{}'.format(folder, name), 'r')
#             message = arquivo.readlines()
#             files = {
#                         name: {'tipo': tipo,
#                                 'path': folder,
#                                 'log' : message,
#                         }
#                     }
#     return files

@app.route("/listLogs", methods=['POST'])
def listLogs():
    from os import walk
    files = {}
    item = 1
    logsPath = '{}\\logs'.format(path.dirname(__file__))
    for folder, _subdirs, filesFolder in walk(logsPath):
        for name in filesFolder:
            tipo = folder.split('\\')[-1]
            files = {
                        item: {'ARQUIVO':name,
                               'TIPO': tipo,
                               'PATH': folder,
                        }
                    }
    return files

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
#     clientes = DADOS +'\\'+'clientes.txt'
#     clientes = open(clientes, 'r')
#     gruposprocessos = DADOS +'\\'+'gruposprocessos.txt'
#     gruposprocessos = open(gruposprocessos, 'r')
#     locaistramites = DADOS +'\\'+'locaistramites.txt'
#     locaistramites = open(locaistramites, 'r')
#     localizadores = DADOS +'\\'+'localizadores.txt'
#     localizadores = open(localizadores, 'r')
#     responsaveis = DADOS +'\\'+'responsaveis.txt'
#     resp1 = open(responsaveis, 'r')
#     resp2 = open(responsaveis, 'r')
#     resp3 = open(responsaveis, 'r')
#     status = DADOS +'\\'+'status.txt'
#     status = open(status, 'r')
#     varas = DADOS +'\\'+'varas.txt'
#     varas = open(varas, 'r')
#     assuntos = DADOS +'\\'+'assuntos.txt'
#     assuntos = open(assuntos, 'r', encoding='utf-8')
#     detalhes = DADOS +'\\'+'detalhes.txt'
#     detalhes = open(detalhes, 'r', encoding='utf-8')
#     areasAtuacao = DADOS +'\\'+'areasAtuacao.txt'
#     areasAtuacao = open(areasAtuacao, 'r', encoding='utf-8')
#     fases = DADOS +'\\'+'fases.txt'
#     fases = open(fases, 'r', encoding='utf-8')
#     objetosAcao = DADOS +'\\'+'objetosAcao.txt'
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