import datetime
from datetime import date
from datetime import timedelta
import locale
import time
from time import strftime
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
    time.sleep(0.5)
    print("pesquisar cliente")
    driver.find_element_by_id("btnPesquisar").click()

    # ATÉ A URL NÃO MUDAR
    time.sleep(0.5)
    # SELECIONA O CLIENTE PESQUISADO
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
    time.sleep(0.5)
    element.click()
    time.sleep(0.5)

def incluirProcesso(urlPage, df, registro):    
    # incluindo processo 
    print("incluindo processo")
    rf.checkPopUps(driver)

    element = rf.waitinstance(driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
    element.click()

    # Grupo internodd
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))
    time.sleep(0.5)

    if (df['cnj'] != ''):
        #Numero do CNJ
        element = rf.waitinstance(driver, '//*[@id="txtNroCnj"]', 1, 'show', 'xpath')
        element.clear()
        element.send_keys(str(df['cnj']))

        # Segredo de Justiça  #por padrão, será marcado não
        element = driver.find_element_by_id("segredoJusticaN")
        driver.execute_script("arguments[0].click();", element)

        time.sleep(0.5)
        element = driver.find_element_by_id("capturarAndamentosS")
        driver.execute_script("arguments[0].click();", element)
    time.sleep(0.5)
    #Numero do Processo
    element = rf.waitinstance(driver, '//*[@id="txtNroProcesso"]', 1, 'show', 'xpath')
    element.clear()
    element.send_keys(str(df['numProcesso']))
    time.sleep(0.5)
    # Status
    element = rf.waitinstance(driver, '//*[@id="slcStatusProcessual"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))
    time.sleep(0.5)

    ########### COLUNA 2 DA PÁGINA
    # Pasta
    driver.execute_script("document.getElementById('txtPasta').value='{}' ".format(str(df['pasta'])) )
    time.sleep(0.5)
    # Grupo Local trâmite
    if (df['localTr'] != ''):
        element = rf.waitinstance(driver, '//*[@id="slcNumeroVara"]', 1, 'show')
        # element.click()
        select = rf.Select(element)
        select.select_by_visible_text(str(df['localTr']))
    time.sleep(0.5)        
    element = rf.waitinstance(driver, '//*[@id="slcLocalTramite"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTramite']))
    time.sleep(0.5)
    # Comarca
    element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['comarca']))
    time.sleep(0.5)
    # UF
    element = rf.waitinstance(driver, '//*[@id="txtUf"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['uf']))
    time.sleep(0.5)
    # RESPONSÁVEL    
    driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

    comboResponsavel = rf.waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 1, 'show')
    comboResponsavel.click()  # clica e abre as opções
    
    element = rf.waitinstance(driver, responsavelXpath(df['responsavel']), 1, 'show')
    time.sleep(0.5)
    element.click() # seleciona o item desejado
    
    comboResponsavel.click() # clica para fechar as opções do combo
    driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
    time.sleep(0.5)
    # Data da Contratação
    driver.execute_script("document.getElementById('txtDataContratacao').value='{}' ".format(str(df['dataContratacao'])))
    time.sleep(0.5)
    # Valor da Causa
    driver.execute_script("document.getElementById('txtValorCausa').value='{}' ".format(str(df['vCausa'])) )
    time.sleep(0.5)

    #Obtém o Num da nova pasta a ser aberta
    time.sleep(1)
    element = rf.waitinstance(driver, "idDoProcesso", 1, 'show', 'class')
    idNovaPasta = element.get_attribute("innerHTML")
    idNovaPasta = idNovaPasta[14:].strip()

    # Abre a aba Parte Adversa
    element = rf.waitinstance(driver, "//*[@id='div_menu17']", 1, 'show')
    element.click()
    # Parte Adversa
    element = rf.waitinstance(driver, '//*[@id="txtNome"]', 1, 'show')
    element.send_keys(str(df['adversa']))

    time.sleep(0.5)
    # Botão salvar
    element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 1, 'show')
    element.click() 

    time.sleep(0.5)
    complemento = ""

    try:
        element = driver.find_element_by_id("popup_ok")
        driver.execute_script("arguments[0].click();", element)
        
        print('pop up OK')
        complemento = " | A Parte adversa - {} - tem outros processos registrados no sistema!".format(str(df['adversa']))
        time.sleep(0.5)
    except:
        pass

    # rf.createLog(logFile, "REGISTRO {}: Gravando a nova pasta {}: id Promad: {}.{}".format(registro, str(df['pasta']), idNovaPasta, complemento))
    time.sleep(1.5)

def criarAgendamentos(dataAudiencia, horaAudienciaFormatada, sigla):
    # Agendamentos
    print("criar agendamentos")
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu 
    driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos

    element = rf.waitinstance(driver, "btnAgendarSalvar", 1, 'show', id)  #checa se redirecionamento ocorreu para agendamentos
    
    rf.checkPopUps(driver)

    for x in range(5):

        if (x == 0):   #tipo audiencia
            if (dataAudiencia != ""):
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
                # combo destinatário - abrir
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                tipoAgendamento = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[2]/label'.format(x+1) 
                appointmentDate = dataAudiencia
                agendamento = "{} - Audiência designada para dia {}".format(sigla, appointmentDate)

                # respons. pelo cliente
                time.sleep(0.3)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[2]/label'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                # GST
                time.sleep(0.3)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[30]/label'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                # operações
                time.sleep(0.3)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[34]/label'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()
                
            else:
                continue

        elif (x == 1): #tipo Instruções para a Audiência
            if (dataAudiencia != ""):
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
                # combo destinatário - abrir
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                tipoAgendamento = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[75]/label/span'.format(x+1)
        
                appointmentDate = datetime.datetime.strptime(dataAudiencia, "%d/%m/%Y")
                appointmentDate = appointmentDate.date() - timedelta(days=2)
                appointmentDate = format(appointmentDate, "%d/%m/%Y")

                agendamento = "{} - Audiência designada para dia {}".format(sigla, appointmentDate)
                
                # operações
                time.sleep(0.3)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[34]/label'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()
            else:
                continue

        elif (x == 2): #tipo Anexar
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[22]/label/span'.format(x+1)
            appointmentDate = datetime.datetime.strptime(dataAudiencia, "%d/%m/%Y")
            appointmentDate = appointmentDate.date() - timedelta(days=2)
            appointmentDate = format(appointmentDate, "%d/%m/%Y")

            agendamento = "ANEXAR"
            # operações
            time.sleep(0.3)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[34]/label'.format(x+1)
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

        elif (x == 3): #tipo Fotocópia
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[71]/label'.format(x+1)
            # dataAudiencia = dataAudiencia + timedelta(days=1)
            appointmentDate = datetime.datetime.strptime(dataAudiencia, "%d/%m/%Y")
            appointmentDate = appointmentDate.date() + timedelta(days=1)
            appointmentDate = format(appointmentDate, "%d/%m/%Y")
            
            agendamento = "Fotocópia integral"
            # GST
            time.sleep(0.3)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[30]/label'.format(x+1)
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()
            # operações
            time.sleep(0.3)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[34]/label'.format(x+1)
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

        elif (x == 4): #tipo Certificar abertura de pasta
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[34]/label/span'.format(x+1)
            dataAudiencia = dataAudiencia + timedelta(days=1)
            agendamento = "{} - Pasta aberta, certificar os agendamentos, agendar contestação e pedir OBF caso tenha liminar deferida.".format(sigla)
            # respons. pelo cliente
            time.sleep(0.3)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[2]/label'.format(x+1)
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

        time.sleep(0.3)
        # combo destinatário - fechar
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'click')
        element.click()

        # combo TIPO - ABRIR
        time.sleep(0.3)
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/button'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'click')
        element.click()

        #TIPO
        time.sleep(0.3)
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[2]/label'.format(x+1)
        element = rf.waitinstance(driver, tipoAgendamento, 1, 'click')
        element.click()

        # combo TIPO - FECHAR
        time.sleep(0.3)
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/button'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'click')
        element.click()

        # CAMPO QUANDO
        time.sleep(0.3)
        # dataAudiencia = str(dataAudiencia.strftime("%d/%m/%Y"))
        xPathElement = '//*[@id="txtDataInicialAgendaProcesso{}"]'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.clear()
        time.sleep(0.3)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(dataAudiencia)

        if (dataAudiencia != ""):        
            if (x == 0):        
                # com HORA
                time.sleep(0.3)
                xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso{}"]'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                time.sleep(0.3)
                
                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.clear()

                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')
                
                hora = horaAudienciaFormatada.strftime("%H:%M")
                element.send_keys(hora)

                time.sleep(0.3)    
                xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')
                element.clear()

                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(x+1)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')

                time.sleep(0.3)
                element.send_keys(hora)
                agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, dataAudiencia, hora)
        else:
            agendamento = "AUDIÊNCIA NÃO MARCADA!"
            # agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, dataAudiencia, horaAudienciaFormatada)
            
        # campo agendamento
        time.sleep(0.3)        
        xPathElement = '//*[@id="txtDescricaoAgendaProcesso{}"]'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(agendamento)

        # campo resumo
        time.sleep(0.3)
        xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.clear()
        time.sleep(0.3)
        xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(x+1)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(agendamento[:30])

        if (x < 4):
            element = rf.waitinstance(driver, '//*[@id="divAgendaCadastrarIncluir"]/a', 1, 'show')  #abrir novo agendamento
            element.click()

def abrePasta(arquivoAbrirPasta, item = 1):
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    
    dfExcel = rf.abreArquivo(arquivoAbrirPasta)
    count = dfExcel.number_of_rows()-1

    cliente = ''
    cliente = dfExcel[1, 12]

    pesquisarCliente(cliente) #Pesquisa cliente, depois faz looping no seu arquivo adicionando os seus processos

    urlPage = driver.current_url
    while (item <= count):
        df = {}

        df['pasta']            = dfExcel[item, 0]
        df['adversa']          = dfExcel[item, 1]

        dataContratacao        = (dfExcel[item, 2])
        dataContratacao        = str(dataContratacao.strftime("%d/%m/%Y"))
        df['dataContratacao']  = dataContratacao

        df['cnj']              = dfExcel[item, 3]

        numProcesso = dfExcel[item, 4]
        numProcesso = '{}-{}.{}.{}.{}.{}'.format(numProcesso[:7], numProcesso[7:9], numProcesso[9:13], numProcesso[13:14], numProcesso[14:16], numProcesso[16:20])
        
        df['numProcesso']      = numProcesso
        df['gpProcesso']       = dfExcel[item, 5]

        df['localTr']          = dfExcel[item, 6]
        df['localTramite']     = dfExcel[item, 7]
        df['comarca']          = dfExcel[item, 8]
        df['uf']               = dfExcel[item, 9]
        
        valorCausa             = locale.format_string("%1.2f", dfExcel[item, 10] , 0)
        df['vCausa']           = valorCausa.replace('.',',')
        
        df['statusProcessual'] = dfExcel[item, 11]

        df['razaoSocial']      = dfExcel[item, 12]
        df['gpCliente']        = dfExcel[item, 13]

        df['responsavel']      = dfExcel[item, 14]
        df['sigla']            = dfExcel[item, 15]
        df['dataAudiencia']    = dfExcel[item, 16]

        if (dfExcel[item, 17] != ""):
            df['horaAudiencia']    = dfExcel[item, 17]
        else:
            df['horaAudiencia']    = "00:00"    #checar no teste
        
        time.sleep(1)

        incluirProcesso(urlPage, df, item)
        # criarAgendamentos(df['dataAudiencia'], df['horaAudiencia'], df['sigla'])
        driver.get(urlPage)   # Volta para a tela de inclusão de nova pasta

        item = item + 1
    
    rf.createLog(logFile, '_________________________________________________________________')
    rf.createLog(logFile, 'FIM')

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
    time.sleep(1)  
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
    print("pesquisar pasta")
    element = rf.waitinstance(driver, "txtPesquisa", 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(1.5)
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

# logFile = logsPath + "\\_log_Arquivo_teste_db.txt"
# if (os.path.isfile(logFile)):
#     os.remove(logFile)

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
                infoLog = "EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
                arquivo = open(infoLog, 'w+')
                arquivo.close()

            logFile = logsPath + "\\_log_{}.txt".format(arquivoAbrirPasta)

            if (os.path.isfile(logFile)):
                linha, count = rf.checkEndFile(logFile)
                              
                if (linha == "FIM"): #ultima linha do arquivo
                    print('O arquivo {}.xlsx já foi executado!\n'.format(arquivoAbrirPasta.upper()))
                    
                else:                              # continua o preenchimento do log já existente
                    if (driverIniciado == False):
                        driverIniciado = True
                        print("INICIANDO WebDriver")
                        driver = rf.iniciaWebdriver(False)
                        rf.acessToIntegra(driver)
                    
                    abrePasta(arquivoAbrirPasta, count)
            else:
                print("INICIANDO WebDriver")
                if (driverIniciado == False):       
                    driverIniciado = True 
                    driver = rf.iniciaWebdriver(False)                        
                    rf.acessToIntegra(driver)

                abrePasta(arquivoAbrirPasta)            

            if (file != ""):
                os.remove(infoLog)                
                # shutil.move(file, pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'

    if (driverIniciado == True):       
        driverIniciado = False
        rf.logoutIntegra(driver)

    time.sleep(1.5)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS\n'.format(hora))
    time.sleep(1.5)
#FIM DO WHILE


# rf.createLog(arquivo, '>>>>>>>>> SCRIPT ENCERRADO! <<<<<<<<<')
# rf.createLog(arquivo, '_________________________________________________________________')
# rf.logoutIntegra(driver)