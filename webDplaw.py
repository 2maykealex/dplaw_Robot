from pprint import pprint
from os import path
import pandas as pd
from os import getcwd
from time import strftime
from datetime import datetime
from basic_functions import createFolder
from werkzeug.utils import secure_filename
from basic_functions import ajustarNumProcessoCNJ
from flask import Flask, render_template, request, redirect, url_for, json

UPLOAD_FOLDER = path.abspath(getcwd()) + '\\arquivos_importados'
ALLOWED_EXTENSIONS = {'xls', 'xls'}
DADOS = path.abspath(getcwd()) +'\\arquivos_necessarios'
HOJE = datetime.today().strftime('%Y-%m-%d')

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

def getDefault(sigla):
    responsaveis = {}
    dadosPadroes = {}

    if (sigla=='BRA'):
        dadosPadroes['slcGrupo'] = 'Grupo 4'
        dadosPadroes['slcStatusProcessual'] = 'DEMANDADO'
        dadosPadroes['slcAreaAtuacao'] = 'Direito do Consumidor'
        dadosPadroes['slcFase'] = 'Conhecimento'
        dadosPadroes['slcLocalizador'] = 'Novo contrato Bradesco'
        responsaveis['Anexar']    = ['ESTAGBRA']
        responsaveis['Audiência'] = ['cbradesco','advbradesco','ESTAGBRA','GST']
        responsaveis['Fotocópia'] = ['GST']
        responsaveis['Processo']  = ['cbradesco','advbradesco','ESTAGBRA']
        responsaveis['Ciencia de novo processo'] = ['cbradesco','advbradesco','ESTAGBRA']

    elif (sigla=='BV'):
        dadosPadroes['slcGrupo'] = 'Grupo 4'
        dadosPadroes['slcStatusProcessual'] = 'DEMANDADO'
        dadosPadroes['slcAreaAtuacao'] = 'Direito do Consumidor'
        dadosPadroes['slcFase'] = 'Conhecimento'
        responsaveis['Processo']  = ['CBV']
        responsaveis['Ciencia de novo processo'] = ['CBV']
        responsaveis['Anexar']    = ['ESTAGBRA']
        responsaveis['Audiência'] = ['CBV','GST']
        responsaveis['Fotocópia'] = ['GST']

    elif (sigla=='FARO'):
        dadosPadroes['slcGrupo'] = 'Grupo 3'
        dadosPadroes['slcStatusProcessual'] = 'DEMANDANTE'
        dadosPadroes['slcAreaAtuacao'] = 'Direito Cível'
        dadosPadroes['slcFase'] = 'COBRANÇA - EM ANDAMENTO'
        dadosPadroes['slcComarca'] = 'Porto Velho'
        dadosPadroes['txtUf'] = 'RO'
        responsaveis['Processo'] = ['ADV1GE','ADV6GE','CGE','NEGOCIEGE']
        responsaveis['Ciencia de novo processo'] = ['ADV1GE','ADV6GE']
        responsaveis['Audiência'] = ['ADV1GE','ADV6GE','CGE','GST']
        responsaveis['Fotocópia'] = ['GST']

    elif (sigla=='OI'):
        dadosPadroes['slcGrupo'] = 'Grupo 4'
        dadosPadroes['slcStatusProcessual'] = 'DEMANDADO'
        dadosPadroes['slcAreaAtuacao'] = 'Direito do Consumidor'
        dadosPadroes['slcFase'] = 'Conhecimento'
        responsaveis['Processo']  = ['COI','advoi']
        responsaveis['Ciencia de novo processo'] = ['COI','advoi']
        responsaveis['Anexar']    = ['COI','apoioOi']
        responsaveis['Audiência'] = ['COI','advoi','GST']
        responsaveis['Fotocópia'] = ['GST']
    else:
        return False

    dadosPadroes['slcResponsavel'] = responsaveis
    return dadosPadroes

@app.route("/defining", methods=['POST'])
def defining():
    print(path.abspath(getcwd()))
    data = request.form.to_dict()
    file = request.files['arquivo']
    filename = secure_filename(file.filename)
    createFolder(UPLOAD_FOLDER)

    newPathFile = path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(newPathFile)

    df = pd.read_excel(newPathFile).fillna('')

    itensPadroes = {}
    registros    = {}
    base         = {}

    #padroes dos links dos Clientes
    urlBRA  = 'https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=14421241&codigo2=14421241'
    urlBV   = 'https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=15208822&codigo2=15208822'
    urlOi   = 'https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=103848554&codigo2=103848554'
    urlFARO = 'https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=104066917&codigo2=104066917'

    #separando base e padrões
    for k, item in data.items():
        if k in ['clientePadrao', 'grupoPadrao', 'siglaPadrao', 'tipo', 'funcao']:
            base[k] = item.strip()
        else:
            itensPadroes[k] = item

    registros.update(base)
    recNum = 1
    regs={}
    dadosPadroes = None
    for registro in df.values:

        if (registro[0] in ['', ' ']):
        # if (registro[0] == ' '):
            continue

        itemDict = {}
        agendamentos = {}
        parteAdversa = {}

        dadosPadroes = getDefault(base['siglaPadrao'])
        if (dadosPadroes):
            for k, dp in dadosPadroes.items():
                itemDict[k] = dp

        if (base['tipo'] == 'atualizacao'):
            if base['funcao'] == 'volumetria':
                itemDict = {'txtPasta': '{}'.format(registro[7]), 'txtCampoLivre3': '{}'.format(filename.replace(filename[-5:], '').replace('_', ' ').strip())}
            elif base['funcao'] == 'contrato':
                itemDict = {'txtPasta': '{}'.format(registro[7]), 'txtCampoLivre4': '{}'.format(filename.replace(filename[-5:], '').replace('_', ' ').strip())}

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
                itemDict['urlCliente']  = urlBRA

            elif base['funcao'] == 'bradesco_email':
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
                itemDict['urlCliente']  = urlBRA

            elif base['funcao'] == 'bv':
                itemDict['txtPasta']    = registro[0]
                if (registro[1] != ''):
                    parteAdversa['txtNome']  = registro[1]
                    itemDict['parteAdversa'] = parteAdversa
                itemDict['txtNroProcesso']  = registro[2]
                itemDict['txtNroCnj']       = registro[2]
                if (type(registro[3]) == type(str() and registro[3] != '')):
                    itemDict['slcNumeroVara']   = "{} ª-º".format(registro[3].split('ª')[0])
                if (type(registro[4]) == type(str() and registro[4] != '')):
                    itemDict['slcLocalTramite'] = registro[4].split(' DE ')[0]
                itemDict['slcComarca']  = registro[5].strip()
                itemDict['txtUf']       = registro[6]

                if (type(registro[7]) == type(str()) and registro[7] != ''):
                    agendamentos['Audiência'] = registro[7].replace('\n','')

                if (type(registro[8]) == type(str()) and registro[8] != ''):
                    agendamentos['HoraAudiencia'] = registro[8].replace('\n','')

                itemDict['txtUf']       = registro[6]
                itemDict['txtUf']       = registro[6]
                itemDict['urlCliente']  = urlBV

            elif base['funcao'] == 'faro_judicial':
                itemDict['txtNroProcesso']    = registro[0]
                itemDict['txtNroCnj']    = registro[0]
                #ADVERSA
                if (registro[1] != ''):
                    parteAdversa['txtNome']  = registro[1].strip()
                if (registro[2] != ''):
                    parteAdversa['txtCPF']  = registro[2]
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

                itemDict['urlCliente']  = urlFARO

            elif base['funcao'] == 'faro_extrajudicial':
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
                itemDict['txtPedido'] = registro[8]
                itemDict['urlCliente']  = urlFARO

            elif base['funcao'] == 'oi_migracao':
                try:
                    itemDict['txtPasta']  = str(int(registro[0]))
                except:
                    continue
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
                itemDict['urlCliente']  = urlOi

            elif base['funcao'] == 'oi_civel':
                try:
                    itemDict['txtPasta']  = str(int(registro[0]))
                except:
                    continue

                itemDict['txtNroCnj']      = str(registro[1]).replace('[','').replace(']','').strip()
                itemDict['txtNroProcesso'] = str(registro[1]).replace('[','').replace(']','').strip()

                if (type(registro[4]) == type(str() and registro[4] != '')):
                    itemDict['txtUf'] = registro[4]

                if (type(registro[5]) == type(str() and registro[5] != '')):
                    itemDict['slcComarca'] = registro[5].strip()

                if (type(registro[6]) == type(str() and registro[6] != '')):
                    itemDict['slcLocalTramite'] = "Vara Cível"
                    try:
                        if ('º' in registro[6] or 'ª' in registro[6]):
                            numero = 'º' if ('º' in registro[6]) else 'ª' if ('ª' in registro[6]) else ''
                            itemDict['slcNumeroVara']   = "{} ª-º".format(str(registro[6].split('{}'.format(numero))[0]))
                    except:
                        pass
                        # itemDict['slcLocalTramite'] = "{}".format(str(registro[7].split('º')[-1]).strip())

                if (type(registro[7]) == type(str() and registro[7] != '')):
                    itemDict['slcObjetoAcao'] = registro[7].strip()
                if (registro[12] != ''):
                    itemDict['txtValorCausa'] = "{}".format(registro[12])

                #   PARTE ADVERSA
                ddd = ''
                if (type(registro[16]) == type(str() and registro[16] != '')):
                    parteAdversa['txtNome']      = registro[16]
                if (type(registro[18]) == type(str() and registro[18] != '')):
                    ddd = (registro[18])
                if (type(registro[19]) == type(str() and registro[19] != '')):
                    parteAdversa['txtTelContato'] = '{}{}'.format(ddd, (registro[19]))
                if (type(registro[26]) == type(float() and registro[26] != '' and registro[26] != 'nan')):
                    parteAdversa['txtCPF'] = '{}'.format(str(int(registro[26])))
                if (type(registro[27]) == type(str() and registro[27] != '')):
                    parteAdversa['txtEndereco'] = '{}'.format(registro[27])
                itemDict['urlCliente']  = urlOi

            elif base['funcao'] == 'oi_jec':
                try:
                    itemDict['txtPasta']  = str(int(registro[0]))
                except:
                    continue

                itemDict['txtNroCnj']      = str(registro[1]).replace('[','').replace(']','').strip()
                itemDict['txtNroProcesso'] = str(registro[1]).replace('[','').replace(']','').strip()

                if (type(registro[5]) == type(str() and registro[5] != '')):
                    itemDict['txtUf'] = registro[5]

                if (type(registro[6]) == type(str() and registro[6] != '')):
                    itemDict['slcComarca'] = registro[6].strip()

                if (type(registro[7]) == type(str() and registro[7] != '')):
                    itemDict['slcLocalTramite'] = "Juizado Especial Cível"
                    try:
                        if ('º' in registro[7] or 'ª' in registro[7]):
                            numero = 'º' if ('º' in registro[7]) else 'ª' if ('ª' in registro[7]) else ''
                            itemDict['slcNumeroVara']   = "{} ª-º".format(str(registro[7].split('{}'.format(numero))[0]))
                    except:
                        pass
                        # itemDict['slcLocalTramite'] = "{}".format(str(registro[7].split('º')[-1]).strip())

                if (type(registro[8]) == type(str() and registro[8] != '')):
                    itemDict['slcObjetoAcao'] = registro[8].strip()
                if (registro[14] != ''):
                    itemDict['txtValorCausa'] = "{}".format(registro[14])

                #   PARTE ADVERSA
                ddd = ''
                if (type(registro[18]) == type(str() and registro[18] != '')):
                    parteAdversa['txtNome']      = registro[18]
                if (type(registro[20]) == type(str() and registro[20] != '')):
                    ddd = (registro[20])
                if (type(registro[21]) == type(str() and registro[21] != '')):
                    parteAdversa['txtTelContato'] = '{}{}'.format(ddd, (registro[21]))
                if (type(registro[28]) == type(float() and registro[28] != '' and registro[28] != 'nan')):
                    parteAdversa['txtCPF'] = '{}'.format(str(int(registro[28])))
                if (type(registro[29]) == type(str() and registro[29] != '')):
                    parteAdversa['txtEndereco'] = '{}'.format(registro[29])

                itemDict['urlCliente']  = urlOi

        if ('txtNroProcesso' in itemDict):
            itemDict['txtNroProcesso'] = ajustarNumProcessoCNJ(str(itemDict['txtNroProcesso']))

        if ('txtNroCnj' in itemDict):
            itemDict['txtNroCnj'] = ajustarNumProcessoCNJ(str(itemDict['txtNroCnj']))

        if (len(agendamentos)>0):
            itemDict['agendamentos'] = agendamentos

        if (len(parteAdversa) > 0):
            itemDict['parteAdversa'] = parteAdversa

        if not("txtDataContratacao" in itemDict):
            itemDict['txtDataContratacao'] = HOJE

        if (itensPadroes):
            itemDict.update(itensPadroes)

        regs[recNum] = itemDict
        recNum = recNum + 1

    data = {}
    registros['registros'] = regs
    data.update(registros)

    data['dadosPadroes'] = dadosPadroes
    # pprint(registros)
    if (base['tipo'] == 'abertura'):
        return render_template('abertura_default.html', data=data, clientes=clientes, gruposprocessos=gruposprocessos, localizadores=localizadores, resp1=resp1, resp2=resp2, resp3=resp3, status=status, varas=varas, locaistramites=locaistramites, assuntos=assuntos, detalhes=detalhes, areasAtuacao=areasAtuacao, fases=fases, objetosAcao=objetosAcao)
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
        newRegistros[int(k)] = v

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
        newRegistros[int(k)] = v

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
    app.run(host="0.0.0.0", port=5000, debug=True)
