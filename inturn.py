import datetime
import locale
import time
import glob
import sys
import os
import shutil
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

    rf.checkPopUps(driver)
    
    # buscando o cliente e acessando sua pasta
    driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(cliente) )
    time.sleep(1)

    driver.find_element_by_id("btnPesquisar").click()
    # rf.createLog(arquivo, 'Pesquisando pelo cliente {}'.format(cliente.upper()))
    # rf.checkElement(driver, "#loopVazio")

    # ATÉ A URL NÃO MUDAR
    time.sleep(1)
    # SELECIONA O CLIENTE PESQUISADO
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
    time.sleep(1)
    element.click()
    # rf.createLog(arquivo, 'Cliente {} localizado e selecionado'.format(cliente.upper()))
    time.sleep(1)

def incluirProcesso(urlPage, df, registro):    
    # incluindo processo    

    rf.checkPopUps(driver)

    element = rf.waitinstance(driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
    element.click()

    # rf.createLog(arquivo, "Incluindo novo processo para o cliente {}".format(df['razaoSocial']))

    # rf.checkElement(driver, "#aProximo")   #AGUARDA O CARREGAMENTO DO ÚLTIMO ELEMENTO DA PÁGINA

    # Grupo internodd
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))
    # rf.createLog(arquivo, "--- preenchendo Grupo {}".format(df['gpProcesso']))
    time.sleep(1)
    if (df['cnj'] != ''):
        #Numero do CNJ
        element = rf.waitinstance(driver, '//*[@id="txtNroCnj"]', 1, 'show', 'xpath')
        element.clear()
        element.send_keys(str(df['cnj']))
        # rf.createLog(arquivo, "--- preenchendo CNJ: {}".format(df['cnj']))

        # Segredo de Justiça  #por padrão, será marcado não
        element = driver.find_element_by_id("segredoJusticaN")
        driver.execute_script("arguments[0].click();", element)
        # rf.createLog(arquivo, "--- Marcando NÃO em Segredo de Justiça")

        time.sleep(1)
        element = driver.find_element_by_id("capturarAndamentosS")
        driver.execute_script("arguments[0].click();", element)
        # rf.createLog(arquivo, "--- Marcando NÃO em SEGREDO DE JUSTIÇA e SIM em CAPTURAR ANDAMENTOS")
    time.sleep(1)
    #Numero do Processo
    element = rf.waitinstance(driver, '//*[@id="txtNroProcesso"]', 1, 'show', 'xpath')
    element.clear()
    element.send_keys(str(df['numProcesso']))
    # rf.createLog(arquivo, "--- preenchendo num. Processo: {}".format(df['numProcesso']))
    time.sleep(1)
    # Status
    element = rf.waitinstance(driver, '//*[@id="slcStatusProcessual"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))
    # rf.createLog(arquivo, "--- preenchendo Status do proceso: {}".format(df['statusProcessual']))
    time.sleep(1)

    ########### COLUNA 2 DA PÁGINA
    # Pasta
    driver.execute_script("document.getElementById('txtPasta').value='{}' ".format(str(df['pasta'])) )
    time.sleep(1)
    # rf.createLog(arquivo, "--- preenchendo a pasta: {}".format(df['pasta']))
    time.sleep(1)
    # Grupo Local trâmite
    if (df['localTr'] != ''):
        element = rf.waitinstance(driver, '//*[@id="slcNumeroVara"]', 1, 'show')
        # element.click()
        select = rf.Select(element)
        select.select_by_visible_text(str(df['localTr']))
        # rf.createLog(arquivo, "--- preenchendo a Local trâmite: {}".format(df['localTr']))
    time.sleep(1)        
    element = rf.waitinstance(driver, '//*[@id="slcLocalTramite"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTramite']))
    # rf.createLog(arquivo, "--- preenchendo a Local trâmite: {}".format(df['localTramite']))
    time.sleep(1)
    # Comarca
    element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['comarca']))
    # rf.createLog(arquivo, "--- preenchendo a Comarca: {}".format(df['comarca']))
    time.sleep(1)
    # UF
    element = rf.waitinstance(driver, '//*[@id="txtUf"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['uf']))
    # rf.createLog(arquivo, "--- preenchendo a UF: {}".format(df['uf']))
    time.sleep(1)
    # RESPONSÁVEL    
    driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

    comboResponsavel = rf.waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 1, 'show')
    comboResponsavel.click()  # clica e abre as opções
    
    element = rf.waitinstance(driver, responsavelXpath(df['responsavel']), 1, 'show')
    time.sleep(1)
    element.click() # seleciona o item desejado
    # rf.createLog(arquivo, "--- preenchendo o responsável: {}".format(df['responsavel']))

    comboResponsavel.click() # clica para fechar as opções do combo
    driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
    time.sleep(1)
    # Data da Contratação
    driver.execute_script("document.getElementById('txtDataContratacao').value='{}' ".format(str(df['dataContratacao'])) )
    # rf.createLog(arquivo, "--- preenchendo a data de contratação: {}".format(df['dataContratacao']))
    time.sleep(1)
    # Valor da Causa
    driver.execute_script("document.getElementById('txtValorCausa').value='{}' ".format(str(df['vCausa'])) )
    # rf.createLog(arquivo, "--- preenchendo o valor da causa: {}".format(df['vCausa']))
    time.sleep(1)

    #Obtém o Num da nova pasta a ser aberta
    time.sleep(2)
    element = rf.waitinstance(driver, "idDoProcesso", 1, 'show', 'class')
    idNovaPasta = element.get_attribute("innerHTML")
    idNovaPasta = idNovaPasta[14:].strip()

    # Abre a aba Parte Adversa
    element = rf.waitinstance(driver, "//*[@id='div_menu17']", 1, 'show')
    element.click()
    # rf.createLog(arquivo, "--- Abrindo aba - Parte adversa")

    # Parte Adversa
    element = rf.waitinstance(driver, '//*[@id="txtNome"]', 1, 'show')
    element.send_keys(str(df['adversa']))
    # rf.createLog(arquivo, "--- preenchendo parte adversa: {}".format(df['adversa']))

    # Botão salvar
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 1, 'show')
    element.click() 

    time.sleep(1)

    try:
        # element = rf.waitinstance(driver, 'popup_ok', 1, 'click', 'id')

        element = driver.find_element_by_id("popup_ok")
        driver.execute_script("arguments[0].click();", element)
        
        # element.click
        print('pop up OK')
        time.sleep(1)
    except:
        pass
    
    rf.createLog(arquivo, "REGISTRO {}: Gravando a nova pasta {} ".format(registro, idNovaPasta))
    # rf.createLog(arquivo, "--- SALVANDO OS DADOS PREENCHIDOS ")
    
    time.sleep(3)

    
    # Agendamentos
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu 
    driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos

    element = rf.waitinstance(driver, "btnAgendarSalvar", 1, 'show', id)  #checa se redirecionamento ocorreu para agendamentos
    
    rf.checkPopUps(driver)

    for x in range(4):
        time.sleep(0.5)
        element = rf.waitinstance(driver, '//*[@id="divAgendaCadastrarIncluir"]/a', 1, 'show')
        element.click()

    for x in range(5):
        xPath = '//*[@id="tableAgendamentoCadastroProcesso{x}"]/tbody/tr[3]/td[1]/button'.format
        element = rf.waitinstance(driver, xPath, 1, 'show')
        element.click()




    #agendamento 1
    #destinatário  //*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button
    #tipo  //*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button
    #quando   //*[@id="txtDataInicialAgendaProcesso1"]
    
    #com hora //*[@id="chkDiaInteiroAgendaProcesso1"]
    #hora1  //*[@id="txtHoraInicialAgendaProcesso1"]
    #hora2  //*[@id="txtHoraFinalAgendaProcesso1"]

    #repetiçao  //*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[6]/td[1]/button
    #agendamento  //*[@id="txtDescricaoAgendaProcesso1"]
    #resumo   //*[@id="txtTituloAgendaProcesso1"]

           
    #agendamento 2
    #destinatário  //*[@id="tableAgendamentoCadastroProcesso2"]/tbody/tr[3]/td[1]/button
    #tipo  //*[@id="tableAgendamentoCadastroProcesso2"]/tbody/tr[4]/td/button
    #quando   //*[@id="txtDataInicialAgendaProcesso2"]
    
    #com hora //*[@id="chkDiaInteiroAgendaProcesso2"]
    #hora1  //*[@id="txtHoraInicialAgendaProcesso2"]
    #hora2  //*[@id="txtHoraFinalAgendaProcesso2"]

    #repetiçao  //*[@id="tableAgendamentoCadastroProcesso2"]/tbody/tr[6]/td[1]/button
    #agendamento  //*[@id="txtDescricaoAgendaProcesso2"]
    #resumo   //*[@id="txtTituloAgendaProcesso2"]


        

    
    # clickAdicionarAgendarCadastrar()


    # driver.get(urlPage)   # Volta para a tela de inclusão de nova pasta

def abrePasta(arquivoAbrirPasta, item = 1):
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    
    dfExcel = rf.abreArquivo(arquivoAbrirPasta)
    count = dfExcel.number_of_rows()-1

    cliente = ''
    cliente = dfExcel[1, 0]

    pesquisarCliente(cliente) #Pesquisa cliente, depois faz looping no seu arquivo adicionando os seus processos

    urlPage = driver.current_url
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
            # df['localTr'] = df['localTr'].replace('ª', ' ª')       # Em casa funciona sem o replace.. no escritorio tive que usar  replace('ª', ' ª')  

            df['localTramite']  = dfExcel[item, 12][position+1: ]

        else:
            df['localTr']       = ''
            df['localTramite']  = dfExcel[item, 12]

        df['responsavel']      =  dfExcel[item, 13]

        valorCausa             = locale.format_string("%1.2f", dfExcel[item, 14] , 0)
        df['vCausa']           =  valorCausa.replace('.',',')

        dataContratacao        = (dfExcel[item, 15])
        dataContratacao         = str(dataContratacao.strftime("%d/%m/%Y"))

        df['dataContratacao']  =  dataContratacao
        df['uf']               =  dfExcel[item, 16]

        time.sleep(2)            
        incluirProcesso(urlPage, df, item)

        item = item + 1
    
    rf.createLog(arquivo, '_________________________________________________________________')
    arquivo.writelines('FIM')

def uploadFile():

    rf.checkPopUps(driver)

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
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 1, 'show')
    element.click()
    # POP UP (OK)
    time.sleep(2)  
    element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 1, 'show')
    element.click()

def pesquisarPasta(pasta):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)
    rf.checkPopUps(driver)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 1, 'show')
    element.click()

    # buscando pasta
    element = rf.waitinstance(driver, "txtPesquisa", 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
    element.click()

#============================PROGRAMA PRINCIPAL==============================

path     = os.getcwd() + "\\files\\abertura_pastas" # obtem o caminho do script e add a pasta abertura_pastas
logsPath = os.getcwd() + "\\files\\abertura_pastas\\logs"

pathExecutados = path + "\\arquivos_executados"

if (os.path.exists(pathExecutados) == False):
    os.mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado - 

if (os.path.exists(path) == False):
    os.mkdir(path)   # Se o diretório Abertura_pastas não existir, será criado - 

if (os.path.exists(logsPath) == False):
    os.mkdir(logsPath)   # Se o diretório Abertura_pastas não existir, será criado - 

os.chdir(path) # seleciona o diretório do script

driverIniciado = False

logFile = logsPath + "\\_log_Arquivo_teste_db.txt"
if (os.path.isfile(logFile)):
    os.remove(logFile)

while True:

    files =  []
    for file in glob.glob("*.xlsx"):
        files.append(file)
        # print(len(files), ' => ', files[-1])    

    if (files):
     
        for file in files:
            arquivoAbrirPasta = file
            arquivoAbrirPasta = arquivoAbrirPasta[:-5]
            
            if (file != ""):
                infoLog = "EXECUTANDO {}.txt".format(file.upper())
                arquivo = open(infoLog, 'w+')  

            logFile = logsPath + "\\_log_{}.txt".format(arquivoAbrirPasta)

            if (os.path.isfile(logFile)):
                arquivoOriginal = open(logFile, 'r')  
                conteudo = arquivoOriginal.readlines()
                count = len(open(logFile).readlines())
                linha = ""

                arquivo = open(logFile, 'w+')  
                for linha in conteudo:
                    arquivo.writelines(linha)
                              
                if (linha == "FIM"): #ultima linha do arquivo
                    print('O arquivo {}.xlsx já foi executado!\n'.format(arquivoAbrirPasta.upper()))
                    
                else:                              # continua o preenchimento do log já existente
                    if (driverIniciado == False):       
                        driverIniciado = True 
                        driver = rf.iniciaWebdriver(False)                        
                        rf.acessToIntegra(driver)
                    
                    abrePasta(arquivoAbrirPasta, count) 

                arquivoOriginal.close()

            else:
                arquivo = open(logFile, 'w+')      
                log = "_________ARQUIVO DE LOG CRIADO DO ARQUIVO {}.xlsx_________".format(arquivoAbrirPasta.upper())
                rf.createLog(arquivo, log)

                if (driverIniciado == False):       
                    driverIniciado = True 
                    driver = rf.iniciaWebdriver(False)                        
                    rf.acessToIntegra(driver)

                abrePasta(arquivoAbrirPasta)            
            
            arquivo.close()

            if (file != ""):
                os.remove(infoLog)

            shutil.move(file, pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'

    if (driverIniciado == True):       
        driverIniciado = False
        rf.logoutIntegra(driver)

    time.sleep(3)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS\n'.format(hora))
    time.sleep(3)
#FIM DO WHILE


# rf.createLog(arquivo, '>>>>>>>>> SCRIPT ENCERRADO! <<<<<<<<<')
# rf.createLog(arquivo, '_________________________________________________________________')
# rf.logoutIntegra(driver)