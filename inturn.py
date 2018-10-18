'''
projeto   deeplaw: intern
automatizar abertura de pastas no sistema dplaw
'''
import datetime
import locale
import time
import sys
import os
import robot_functions as rf

def responsavelXpath(responsavel):
    if responsavel == 'acordosg4':
        return '//*[@id="ui-multiselect-slcResponsavel-option-1"]'
    elif responsavel == 'ADV1GE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-2"]'
    elif responsavel == 'ADV2GE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-3"]'
    elif responsavel == 'ADV3GE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-3"]'
    elif responsavel == 'ADV4GE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-4"]'
    elif responsavel == 'advbradesco':
        return '//*[@id="ui-multiselect-slcResponsavel-option-5"]'
    elif responsavel == 'advgg1':
        return '//*[@id="ui-multiselect-slcResponsavel-option-6"]'
    elif responsavel == 'AG6':
        return '//*[@id="ui-multiselect-slcResponsavel-option-7"]'
    elif responsavel == 'AGE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-8"]'
    elif responsavel == 'AGE2':
        return '//*[@id="ui-multiselect-slcResponsavel-option-9"]'
    elif responsavel == 'AGS':
        return '//*[@id="ui-multiselect-slcResponsavel-option-10"]'
    elif responsavel == 'ApoioBV':
        return '//*[@id="ui-multiselect-slcResponsavel-option-11"]'
    elif responsavel == 'apoiogg1':
        return '//*[@id="ui-multiselect-slcResponsavel-option-12"]'
    elif responsavel == 'apoiogg2':
        return '//*[@id="ui-multiselect-slcResponsavel-option-13"]'
    elif responsavel == 'BVADV1':
        return '//*[@id="ui-multiselect-slcResponsavel-option-14"]'
    elif responsavel == 'BVADV2':
        return '//*[@id="ui-multiselect-slcResponsavel-option-15"]'
    elif responsavel == 'cbradesco':
        return '//*[@id="ui-multiselect-slcResponsavel-option-16"]'
    elif responsavel == 'CBV':
        return '//*[@id="ui-multiselect-slcResponsavel-option-17"]'
    elif responsavel == 'CGE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-18"]'
    elif responsavel == 'COBRA1':
        return '//*[@id="ui-multiselect-slcResponsavel-option-19"]'
    elif responsavel == 'COP':
        return '//*[@id="ui-multiselect-slcResponsavel-option-20"]'
    elif responsavel == 'Correspondente':
        return '//*[@id="ui-multiselect-slcResponsavel-option-21"]'
    elif responsavel == 'CSEG':
        return '//*[@id="ui-multiselect-slcResponsavel-option-22"]'
    elif responsavel == 'ESP':
        return '//*[@id="ui-multiselect-slcResponsavel-option-23"]'
    elif responsavel == 'EXT':
        return '//*[@id="ui-multiselect-slcResponsavel-option-24"]'
    elif responsavel == 'Financeiro':
        return '//*[@id="ui-multiselect-slcResponsavel-option-25"]'
    elif responsavel == 'GFP':
        return '//*[@id="ui-multiselect-slcResponsavel-option-26"]'
    elif responsavel == 'GG1':
        return '//*[@id="ui-multiselect-slcResponsavel-option-27"]'
    elif responsavel == 'GG2':
        return '//*[@id="ui-multiselect-slcResponsavel-option-28"]'
    elif responsavel == 'GST':
        return '//*[@id="ui-multiselect-slcResponsavel-option-29"]'
    elif responsavel == 'JEP':
        return '//*[@id="ui-multiselect-slcResponsavel-option-30"]'
    elif responsavel == 'jREP':
        return '//*[@id="ui-multiselect-slcResponsavel-option-31"]'
    elif responsavel == 'KET':
        return '//*[@id="ui-multiselect-slcResponsavel-option-32"]'
    elif responsavel == 'LBG':
        return '//*[@id="ui-multiselect-slcResponsavel-option-33"]'
    elif responsavel == 'LVC':
        return '//*[@id="ui-multiselect-slcResponsavel-option-34"]'
    elif responsavel == 'operacoes':
        return '//*[@id="ui-multiselect-slcResponsavel-option-35"]'
    elif responsavel == 'PLV':
        return '//*[@id="ui-multiselect-slcResponsavel-option-36"]'
    elif responsavel == 'PUB':
        return '//*[@id="ui-multiselect-slcResponsavel-option-37"]'
    elif responsavel == 'Robô':
        return '//*[@id="ui-multiselect-slcResponsavel-option-38"]'
    elif responsavel == 'SMF':
        return '//*[@id="ui-multiselect-slcResponsavel-option-39"]'
    elif responsavel == 'STJ':
        return '//*[@id="ui-multiselect-slcResponsavel-option-40"]'
    elif responsavel == 'TESTE':
        return '//*[@id="ui-multiselect-slcResponsavel-option-41"]'
    elif responsavel == 'TLA -':
        return '//*[@id="ui-multiselect-slcResponsavel-option-42"]'
    elif responsavel == 'TRIA':
        return '//*[@id="ui-multiselect-slcResponsavel-option-43"]'

def pesquisarCliente(cliente):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # buscando o cliente e acessando sua pasta
    element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(cliente)
    driver.find_element_by_id("btnPesquisar").click()
    rf.createLog(arquivo, 'Pesquisando pelo cliente {}'.format(cliente.upper()))
    rf.checkElement(driver, "#loopVazio")

    # ATÉ A URL NÃO MUDAR
    time.sleep(3)
    # SELECIONA O CLIENTE PESQUISADO
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()
    rf.createLog(arquivo, 'Cliente {} localizado e selecionado'.format(cliente.upper()))

def incluirProcesso(urlPage, df):    

    # incluindo processo    
    element = rf.waitinstance(driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 30, 1, 'show')
    element.click()

    rf.createLog(arquivo, "Incluindo novo processo para o cliente {}".format(df['razaoSocial']))

    rf.checkElement(driver, "#aProximo")   #AGUARDA O CARREGAMENTO DO ÚLTIMO ELEMENTO DA PÁGINA

    # Grupo internodd
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))
    rf.createLog(arquivo, "--- preenchendo Grupo {}".format(df['gpProcesso']))

    if (df['cnj'] != ''):
        #Numero do CNJ
        element = rf.waitinstance(driver, '//*[@id="txtNroCnj"]', 30, 1, 'show', 'xpath')
        element.clear()
        element.send_keys(str(df['cnj']))
        rf.createLog(arquivo, "--- preenchendo CNJ: {}".format(df['cnj']))

        time.sleep(1)
        # Segredo de Justiça  #por padrão, será marcado não
        element = rf.waitinstance(driver, 'segredoJusticaN', 30, 1, 'show', 'id')
        element.click()
        rf.createLog(arquivo, "--- Marcando NÃO em Segredo de Justiça")

        time.sleep(1)
        # Capturar andamentos
        
        # element = rf.waitinstance(driver, 'capturarAndamentosS', 30, 1, 'show', 'id')

        # element = driver.find_element_by_id("capturarAndamentosS")
        # print (element.

        # driver.execute_script("$('#capturarAndamentosS').css('display', 'block');") # torna elemento visível

        # //*[@id="capturarAndamentosS"]


        # element = rf.waitinstance(driver, 'capturarAndamentosS', 30, 1, 'show', 'id')
        # element.click()
        # rf.createLog(arquivo, "--- Marcando SIM em Capturar andamentos")

    #Numero do Processo
    element = rf.waitinstance(driver, '//*[@id="txtNroProcesso"]', 30, 1, 'show', 'xpath')
    element.clear()
    element.send_keys(str(df['numProcesso']))
    rf.createLog(arquivo, "--- preenchendo num. Processo: {}".format(df['numProcesso']))
    
    # Status
    element = rf.waitinstance(driver, '//*[@id="slcStatusProcessual"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))
    rf.createLog(arquivo, "--- preenchendo Status do proceso: {}".format(df['statusProcessual']))


    ########### COLUNA 2 DA PÁGINA
    # Pasta
    element = rf.waitinstance(driver, '//*[@id="txtPasta"]', 30, 1, 'show')
    element.send_keys(str(df['pasta']))
    rf.createLog(arquivo, "--- preenchendo a pasta: {}".format(df['pasta']))

    # Grupo Local trâmite
    if (df['localTr'] != ''):
        element = rf.waitinstance(driver, '//*[@id="slcNumeroVara"]', 30, 1, 'show')
        select = rf.Select(element)
        select.select_by_visible_text(str(df['localTr']))
        rf.createLog(arquivo, "--- preenchendo a Local trâmite: {}".format(df['localTr']))
        
    element = rf.waitinstance(driver, '//*[@id="slcLocalTramite"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTramite']))
    rf.createLog(arquivo, "--- preenchendo a Local trâmite: {}".format(df['localTramite']))

    # Comarca
    element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['comarca']))
    rf.createLog(arquivo, "--- preenchendo a Comarca: {}".format(df['comarca']))

    # UF
    element = rf.waitinstance(driver, '//*[@id="txtUf"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['uf']))
    rf.createLog(arquivo, "--- preenchendo a UF: {}".format(df['uf']))

    # RESPONSÁVEL    
    driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

    comboResponsavel = rf.waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 30, 1, 'show')
    comboResponsavel.click()  # clica e abre as opções
    
    element = rf.waitinstance(driver, responsavelXpath(df['responsavel']), 30, 1, 'show')
    time.sleep(0.5)
    element.click() # seleciona o item desejado
    rf.createLog(arquivo, "--- selecionando o responsável: {}".format(df['responsavel']))

    comboResponsavel.click() # clica para fechar as opções do combo
    driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
    
    # Data da Contratação
    element = rf.waitinstance(driver, '//*[@id="txtDataContratacao"]', 30, 1, 'show')
    element.send_keys(str(df['dataContratacao']))
    rf.createLog(arquivo, "--- preenchendo a data de contratação: {}".format(df['dataContratacao']))

    # Valor da Causa
    element = rf.waitinstance(driver, '//*[@id="txtValorCausa"]', 30, 1, 'show')
    element.send_keys(str(df['vCausa']))
    rf.createLog(arquivo, "--- preenchendo o valor da causa: {}".format(df['vCausa']))

    if (df['cnj'] != ''):
        element = rf.waitinstance(driver, 'capturarAndamentosS', 30, 1, 'show', 'id')
        element.click()
        rf.createLog(arquivo, "--- Marcando SIM em Capturar andamentos")
        time.sleep(4)

    # Abre a aba Parte Adversa
    element = rf.waitinstance(driver, "//*[@id='div_menu17']", 30, 1, 'show')
    element.click()
    rf.createLog(arquivo, "--- Abrindo aba - Parte adversa")

    # Parte Adversa
    element = rf.waitinstance(driver, '//*[@id="txtNome"]', 30, 1, 'show')
    element.send_keys(str(df['adversa']))
    rf.createLog(arquivo, "--- preenchendo parte adversa: {}".format(df['adversa']))
    
    #Botão salvar
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
    element.click() 
    rf.createLog(arquivo, "--- SALVANDO OS DADOS PREENCHIDOS ")
    
    time.sleep(6)
    driver.get(urlPage)




    # #OUTRA CONDIÇÃO !!!
    # element = waitinstance(driver, "//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]", 30, 5, 'click')
    # element.click()

    # #acessa
    # driver.get('http://www.integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=14421241&codigo2=14421241')
    # //*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]
    # jsbutton = ActionChains(driver).click(element)
    # jsbutton.perform()

def abrePastaTeste(arquivoAbrirPasta):  #teste pandas
    
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"

    dfExcel = rf.abreArquivo(arquivoAbrirPasta)
    dfExcel = rf.getFile(arquivoAbrirPasta)
    # dfExcel.to_dict()
    # dfExcel = rf.pd.DataFrame.to_dict (dfExcel)
    # pesquisarCliente()

    listIndex = ['razaoSocial', 'gpCliente', 'cnpjCliente', 'numProcesso', 'pasta', 'statusProcessual', 'cnpjAdversa', 'cpfAdversa', 
                'gpProcesso', 'adversa', 'tipoProcesso', 'comarca', 'localTr', 'localTramite', 'responsavel', 'vCausa', 
                'dataContratacao', 'uf']

    df = []    
    item = 0
    for key, value in dfExcel.items():
        # print(value[0])

        linha  = 0
        coluna =  0

        while coluna <= 16:

            while linha <= value.count():

                df[linha][coluna] =  value[0]
                print (df)

                linha = linha + 1

            coluna  = coluna  + 1






        # for x in value:
        #     print(x)
            # if (item != 12):  # item que corresponde à coluna local Tramite na planilha
            #     print('item = ', item, ' - ', listIndex[item],'=>', x)
            #     df[listIndex[item]] = x
            # else:
            #     print(x)
            #     local = x.split(';')
                
            #     # print('item = ', item, ' - ', listIndex[item],'=>', str(local[0]))
            #     df[listIndex[item]] = str(local[0])
            #     item = item + 1
            #     df[listIndex[item]] = str(local[1])
            #     # item = item + 1
            #     # print('item = ', item, ' - ', listIndex[item],'=>', str(local[1]))
            
            # item = item + 1
    
    print (df)

        # df[listIndex[item]] = val
        # print(val)

        # myDict['razaoSocial'] = val

        # df['razaoSocial']      =  dfExcel[0][item]

        
        

    print('==================')
    # print(val)
    # print (df['vCausa'][1])


    # print (df['vCausa'][1])

    # item = 1

    # while (item <= 2):


        # df = {}

        # df['razaoSocial']      =  dfExcel[0][item]#dfExcel[item, 0]
        # df['gpCliente']        =  dfExcel[1][item]#dfExcel[item, 1]
        # df['cnpjCliente']      =  dfExcel[2][item]#dfExcel[item, 2]
        # df['numProcesso']      =  dfExcel[3][item]#dfExcel[item, 3]
        # df['pasta']            =  dfExcel[4][item]#dfExcel[item, 4]
        # df['statusProcessual'] =  dfExcel[5][item]#dfExcel[item, 5]
        # df['cnpjAdversa']      =  dfExcel[6][item]#dfExcel[item, 6]
        # df['cpfAdversa']       =  dfExcel[7][item]#dfExcel[item, 7]
        # df['gpProcesso']       =  dfExcel[8][item]#dfExcel[item, 8]
        # df['adversa']          =  dfExcel[9][item]#dfExcel[item, 9]
        # df['tipoProcesso']     =  dfExcel[10][item]#dfExcel[item, 10]
        # df['comarca']          =  dfExcel[11][item]#dfExcel[item, 11]

        # # local = dfExcel[12][item].split(';')

        # # df['localTr']          =  str(local[0])
        # # df['localTramite']     =  str(local[1])

        # df['responsavel']      =  dfExcel[13][item]

        # valorCausa             = locale.format_string("%1.2f", dfExcel[14][item] , 0)
        # df['vCausa']           =  valorCausa

        # dataContratacao        = (dfExcel[15][item])
        # dataContratacao         = str(dataContratacao.strftime("%d/%m/%Y"))
        # dataContratacao         = dataContratacao.replace("/", "")

        # df['dataContratacao']  =  dataContratacao
        # df['uf']               =  dfExcel[16][item]

        # # time.sleep(3)            
        # # incluirProcesso(urlPage, df)

        # item = item + 1

        # print ('item ',item, ' ', df['vCausa'])

    # while (item <= 2):
    #     df = {}


    # print(listIndex)

    #     df['razaoSocial']      =  dfExcel[0][item]#dfExcel[item, 0]
    #     df['gpCliente']        =  dfExcel[1][item]#dfExcel[item, 1]
    #     df['cnpjCliente']      =  dfExcel[2][item]#dfExcel[item, 2]
    #     df['numProcesso']      =  dfExcel[3][item]#dfExcel[item, 3]
    #     df['pasta']            =  dfExcel[4][item]#dfExcel[item, 4]
    #     df['statusProcessual'] =  dfExcel[5][item]#dfExcel[item, 5]
    #     df['cnpjAdversa']      =  dfExcel[6][item]#dfExcel[item, 6]
    #     df['cpfAdversa']       =  dfExcel[7][item]#dfExcel[item, 7]
    #     df['gpProcesso']       =  dfExcel[8][item]#dfExcel[item, 8]
    #     df['adversa']          =  dfExcel[9][item]#dfExcel[item, 9]
    #     df['tipoProcesso']     =  dfExcel[10][item]#dfExcel[item, 10]
    #     df['comarca']          =  dfExcel[11][item]#dfExcel[item, 11]

    #     # local = dfExcel[12][item].split(';')

    #     # df['localTr']          =  str(local[0])
    #     # df['localTramite']     =  str(local[1])

    #     df['responsavel']      =  dfExcel[13][item]

    #     valorCausa             = locale.format_string("%1.2f", dfExcel[14][item] , 0)
    #     df['vCausa']           =  valorCausa

    #     dataContratacao        = (dfExcel[15][item])
    #     dataContratacao         = str(dataContratacao.strftime("%d/%m/%Y"))
    #     dataContratacao         = dataContratacao.replace("/", "")

    #     df['dataContratacao']  =  dataContratacao
    #     df['uf']               =  dfExcel[16][item]

    #     # time.sleep(3)            
    #     # incluirProcesso(urlPage, df)

    #     item = item + 1

    #     print ('item ',item, ' ', df['vCausa'])

        # TODO IMPORTAR DADOS DA PLANILHA PARA UM DICIONÁRIO
        # from pyexcel._compact import OrderedDict
        # dfExcel = pe.get_dict(file_name="teste_db.xlsx", name_columns_by_row=0)
        # isinstance(dfExcel, OrderedDict)
        # True

        # for key, values in dfExcel.items():
        #     print({str(key): values})

        # dfExcel = pe.get_records(file_name="teste_db.xlsx")
        # print (dfExcel[1])
        # print('=============================================================================')
        # for record in dfExcel:
        #     print(record['Grupo Cliente'])
        #     print('=============================================================================')

def abrePasta(arquivoAbrirPasta):
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    
    dfExcel = rf.abreArquivo(arquivoAbrirPasta)
    count = dfExcel.number_of_rows()-1
    
    item = 1

    while (item <= count):
        df = {}

        df['razaoSocial']      =  dfExcel[item, 0]
        df['gpCliente']        =  dfExcel[item, 1]
        df['cnj']              =  dfExcel[item, 2]
        df['numProcesso']      =  dfExcel[item, 3]
        df['pasta']            =  dfExcel[item, 4]
        df['statusProcessual'] =  dfExcel[item, 5]
        df['cnpjAdversa']      =  dfExcel[item, 6]
        df['cpfAdversa']       =  dfExcel[item, 7]
        df['gpProcesso']       =  dfExcel[item, 8]
        df['adversa']          =  dfExcel[item, 9]
        df['tipoProcesso']     =  dfExcel[item, 10]
        df['comarca']          =  dfExcel[item, 11]

        local = dfExcel[item, 12]

        if (local[0].isdigit()):            
            position = dfExcel[item, 12].index('º')
            position = position + 1

            df['localTr']       = dfExcel[item, 12][0:position]
            df['localTr'] = df['localTr'].replace('ª', 'ª')       # Em casa funciona sem o replace.. no escritorio tive que usar  replace('ª', ' ª')  

            df['localTramite']  = dfExcel[item, 12][position+1: ]

        else:
            df['localTr']       = ''
            df['localTramite']  = dfExcel[item, 12]

        df['responsavel']      =  dfExcel[item, 13]

        valorCausa             = locale.format_string("%1.2f", dfExcel[item, 14] , 0)
        df['vCausa']           =  valorCausa

        dataContratacao        = (dfExcel[item, 15])
        dataContratacao         = str(dataContratacao.strftime("%d/%m/%Y"))
        dataContratacao         = dataContratacao.replace("/", "")

        df['dataContratacao']  =  dataContratacao
        df['uf']               =  dfExcel[item, 16]

        pesquisarCliente(df['razaoSocial'])
        time.sleep(3)            
        incluirProcesso(urlPage, df)

        item = item + 1

def uploadFile():

    # ACESSAR ÁREA DE DOWNLOADS
    driver.execute_script("clickMenuCadastro(108,'processoDocumento.asp');")


    # TODO FAZER LOOPING PARA ADD TODOS OS ARQUIVOS PERTINENTES AO PROCESSO/CLIENTE
    time.sleep(6)      
    path = 'C:/Users/DPLAW-BACKUP/Desktop/dprobot/dpRobot/dplaw_Robot/pdf.pdf' # CAMINHO DO ARQUIVO 
    # TODO MONTAR CAMINHO DINAMICAMENTE # driver.send_keys(os.getcwd() + "/tests/sample_files/Figure1.tif")

    # driver.switch_to.frame(1)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe")) #ACESSANDO CONTEUDO DE UM FRAME

    element = driver.find_element_by_xpath('//*[@id="realupload"]')
    element.send_keys(path)

    driver.switch_to.default_content()   #VOLTAR PARA O CONTEUDO PRINCIPAL

    #Botão salvar
    time.sleep(6)  
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
    element.click()
    # POP UP (OK)
    time.sleep(2)  
    element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 30, 1, 'show')
    element.click()

def pesquisarPasta(pasta):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 30, 1, 'show')
    element.click()

    # buscando pasta
    element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

# TODO ADD FUNCÕES DE PESQUISA EM ROBOT_FUNCTIONS: COLOCAR OPÇÃO PARA PESQUISA

#============================PROGRAMA PRINCIPAL==============================
#executando python inturn.py "teste_db.xlsx" no TERMINAL
arquivoAbrirPasta = sys.argv[1]
arquivoAbrirPasta = arquivoAbrirPasta[:-5]

os.chdir(os.getcwd()) # obtem o caminho do script e seleciona o diretório do script

hoje = "%s" % (time.strftime("%Y_%m_%d"))
hora = time.strftime("%H:%M:%S")
horaStr = hora.replace(':', '-')
logFile = os.getcwd() + "/logs/_{}_{}_log_dplaw_robot.txt".format(hoje, horaStr)

arquivo = open(logFile, 'w+')

driver = rf.iniciaWebdriver(False) 
rf.acessToIntegra(arquivo, driver)
abrePasta(arquivoAbrirPasta)

# abrePastaTeste(arquivoAbrirPasta)  #teste para usar o PANDAS
# pesquisarPasta()
# uploadFile()
# rf.getFile(arquivoAbrirPasta)



# rf.acessToPJE(arquivo, driver)


rf.createLog(arquivo, '>>>>>>>>> SCRIPT ENCERRADO! <<<<<<<<<')
rf.createLog(arquivo, '_________________________________________________________________')
arquivo.close()
rf.logoutIntegra(driver)