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

def pesquisarCliente(cliente = 'Cliente teste'):
    # # acessando a pesquisa de clientes no sistema
    # element_over = waitinstance(driver, "//*[@id='header']/ul/li[1]/a", 30, 1, 'click')
    # hover = ActionChains(driver).move_to_element(element_over)
    # hover.perform()

    # element = waitinstance(driver, "//*[@id='header']/ul/li[1]/ul/lii[1]/p", 30, 1, 'click')
    # element.click()
    # #driver.find_element_by_xpath("//*[@id='header']/ul/li[1]/ul/lii[1]/p").click()

    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # buscando o cliente e acessando sua pasta
    element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(cliente)
    driver.find_element_by_id("btnPesquisar").click()

    # ATÉ A URL NÃO MUDAR
    time.sleep(3)
    # SELECIONA O CLIENTE PESQUISADO
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def incluirProcesso(urlPage, df):    

    # if (urlPage == ""):
    #     urlPage =  driver.current_url

    # incluindo processo    
    driver.find_element_by_xpath("//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]").click()

    # Grupo internodd
    print(df['gpProcesso'])
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))

    #Numero do CNJ e do Processo
    element = rf.waitinstance(driver, '//*[@id="txtNroCnj"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))
    element = rf.waitinstance(driver, '//*[@id="txtNroProcesso"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))

    # Status
    element = rf.waitinstance(driver, '//*[@id="slcStatusProcessual"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))


    ########### COLUNA 2 DA PÁGINA

    # Pasta
    element = rf.waitinstance(driver, '//*[@id="txtPasta"]', 30, 1, 'show')
    element.send_keys(str(df['pasta']))

    # Grupo Local trâmite
    element = rf.waitinstance(driver, '//*[@id="slcNumeroVara"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTr']))
    element = rf.waitinstance(driver, '//*[@id="slcLocalTramite"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTramite']))

    # Comarca
    element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['comarca']))

    # UF
    element = rf.waitinstance(driver, '//*[@id="txtUf"]', 30, 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['uf']))

    # RESPONSÁVEL    
    driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

    comboResponsavel = rf.waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 30, 1, 'show')
    comboResponsavel.click()  # clica e abre as opções
    
    element = rf.waitinstance(driver, responsavelXpath(df['responsavel']), 30, 1, 'show')
    element.click() # seleciona o item desejado

    comboResponsavel.click() # clica para fechar as opções do combo
    driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
    
    # Data da Contratação
    element = rf.waitinstance(driver, '//*[@id="txtDataContratacao"]', 30, 1, 'show')
    element.send_keys(str(df['dataContratacao']))

    # Valor da Causa
    element = rf.waitinstance(driver, '//*[@id="txtValorCausa"]', 30, 1, 'show')
    element.send_keys(str(df['vCausa']))

    # Abre a aba Parte Adversa
    element = rf.waitinstance(driver, "//*[@id='div_menu17']", 30, 1, 'show')
    element.click()

    # Parte Adversa
    element = rf.waitinstance(driver, '//*[@id="txtNome"]', 30, 1, 'show')
    element.send_keys(str(df['adversa']))

    #Botão salvar
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
    element.click()

    time.sleep(6)
    print (urlPage)
    driver.get(urlPage)

    # TODO VER PARA IDENTIFICAR JAVASCRIPT E DAR OK QUANDO IDENTIFICA QUE JÁ EXISTE A PESSOA
    
    # //*[@id="popup_ok"]

    # element = waitinstance(driver, '//*[@id="barra"]/div/div[1]/span[2]', 30, 1, 'show')
    # hover = ActionChains(driver).move_to_element(element)
    # hover.perform()
    # element.click()

    # driver.execute_script("return clickAcessoPagina('parteVisualizar.asp?codigo=100858103&codigo2=100858103')"); #torna elemento invisível novamente
    #===================

    # #OUTRA CONDIÇÃO !!!
    # element = waitinstance(driver, "//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]", 30, 5, 'click')
    # element.click()

    # #acessa
    # driver.get('http://www.integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=14421241&codigo2=14421241')
    # //*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]
    # jsbutton = ActionChains(driver).click(element)
    # jsbutton.perform()

def abrePasta(arquivoAbrirPasta):
    
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"

    dfExcel = rf.abreArquivo(arquivoAbrirPasta)

    count = dfExcel.number_of_rows()-1
    pesquisarCliente()

    item = 1

    while (item <= count):
        df = {}

        df['razaoSocial']      =  dfExcel[item, 0]
        df['gpCliente']        =  dfExcel[item, 1]
        df['cnpjCliente']      =  dfExcel[item, 2]
        df['numProcesso']      =  dfExcel[item, 3]
        df['pasta']            =  dfExcel[item, 4]
        df['statusProcessual'] =  dfExcel[item, 5]
        df['cnpjAdversa']      =  dfExcel[item, 6]
        df['cpfAdversa']       =  dfExcel[item, 7]
        df['gpProcesso']       =  dfExcel[item, 8]
        df['adversa']          =  dfExcel[item, 9]
        df['tipoProcesso']     =  dfExcel[item, 10]
        df['comarca']          =  dfExcel[item, 11]

        local = dfExcel[item, 12].split(';')

        df['localTr']          =  str(local[0])
        df['localTramite']     =  str(local[1])

        df['responsavel']      =  dfExcel[item, 13]

        valorCausa             = locale.format_string("%1.2f", dfExcel[item, 14] , 0)
        df['vCausa']           =  valorCausa

        dataContratacao        = (dfExcel[item, 15])
        dataContratacao         = str(dataContratacao.strftime("%d/%m/%Y"))
        dataContratacao         = dataContratacao.replace("/", "")

        df['dataContratacao']  =  dataContratacao
        df['uf']               =  dfExcel[item, 16]

        time.sleep(3)            
        incluirProcesso(urlPage, df)

        item = item + 1

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


#============================PROGRAMA PRINCIPAL==============================
#executando python inturn.py "teste_db.xlsx" no TERMINAL
arquivoAbrirPasta = sys.argv[1]
arquivoAbrirPasta = arquivoAbrirPasta[:-5]

driver = rf.iniciaWebdriver()
rf.acessToIntegra(driver)

abrePasta(arquivoAbrirPasta)




