import datetime
from datetime import date
from datetime import timedelta
import calendar
import locale
import time
from time import strftime
import glob
import sys
import os
import shutil
import robot_functions as rf

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

def pesquisarCliente(cliente):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    rf.checkPopUps(driver)

    # buscando o cliente e acessando sua pasta
    driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(cliente) )
    time.sleep(0.5)
    print("pesquisar cliente {}".format(cliente))
    driver.find_element_by_id("btnPesquisar").click()

    # ATÉ A URL NÃO MUDAR
    time.sleep(0.5)
    # SELECIONA O CLIENTE PESQUISADO
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
    time.sleep(0.5)
    element.click()
    time.sleep(0.5)

def pesquisarPasta(pasta):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    rf.checkPopUps(driver)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 1, 'show')
    time.sleep(0.3)
    element.click()
    time.sleep(0.3)

    # buscando pasta
    driver.execute_script("document.getElementById('txtPesquisa').value={} ".format(pasta))
    time.sleep(0.3)
    print("pesquisar pasta {}".format(pasta))
    driver.find_element_by_id("btnPesquisar").click()
    time.sleep(1)

    try:
        # SELECIONA O CLIENTE PESQUISADO
        time.sleep(1)
        element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
        retorno = True

    except:
        # element = driver.find_element_by_id('loopVazio')  #se encontrar este elemento, é porque não há registros
        hora = time.strftime("%H:%M:%S")
        print('{} - Não encontrou a pasta'.format(hora))
        retorno = False
        
    return retorno

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
        select = rf.Select(element)
        select.select_by_visible_text(str(df['localTr']))
    time.sleep(0.5)
    element = rf.waitinstance(driver, '//*[@id="slcLocalTramite"]', 1, 'show')
    select = rf.Select(element)
    select.select_by_visible_text(str(df['localTramite']))
    time.sleep(0.5)

    # #PARA ATUALIZAR OS DADOS
    # logAtualizaPromad = os.getcwd() + "\\logs\\_Locais.txt"
    # rf.createLog(logAtualizaPromad)
    # for elemento in element.find_elements_by_tag_name('option'):
    #     texto = "{}\n".format(elemento.text)
    #     rf.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

    # Comarca
    if (str(df['comarca']) != ""):
        element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 1, 'show')
        select = rf.Select(element)
        select.select_by_visible_text(str(df['comarca']))
        time.sleep(0.5)
    else:
        element = rf.waitinstance(driver, '//*[@id="slcComarca"]', 1, 'show')
        select = rf.Select(element)
        select.select_by_visible_text("--Cadastrar Novo Item--")
        time.sleep(0.5)

        # #PARA ATUALIZAR OS DADOS
        # logAtualizaPromad = os.getcwd() + "\\logs\\_Comarcas.txt"
        # rf.createLog(logAtualizaPromad)
        # for elemento in element.find_elements_by_tag_name('option'):
        #     texto = "{}\n".format(elemento.text)
        #     rf.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

        element = rf.waitinstance(driver, '//*[@id="txtComarca"]', 1, 'show')
        element.send_keys(str(df['comarcaNova']))
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

    #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
    xInputs = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li'
    listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

    # RESPONSÁVEIS
    y = 1
    for item in listInputs:  #itera inputs recuperados, checa e clica
        if (item.text == df['responsavel']):
            xPathItem = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li[{}]'.format(y)
            element = rf.waitinstance(driver, xPathItem, 1, 'click')
            element.click()
            time.sleep(0.3)
            break
        y = y + 1
    
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

    rf.createLog(logFile, "REGISTRO {}: Gravando a nova pasta {}: id Promad: {}.{}".format(registro, str(df['pasta']), idNovaPasta, complemento))
    time.sleep(1.5)

def criarAgendamentos(dataAudiencia, dataAberturaPasta, horaAudienciaFormatada, sigla, responsavel, pasta, registro):
    # Agendamentos
    print("criando agendamentos")
    element = rf.waitinstance(driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu
    driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos

    element = rf.waitinstance(driver, "btnAgendarSalvar", 1, 'show', id)  #checa se redirecionamento ocorreu para agendamentos
    rf.checkPopUps(driver)

    dataAberturaPasta = datetime.datetime.strptime(dataAberturaPasta, "%d/%m/%Y")
    dataAberturaPasta = dataAberturaPasta.date() + timedelta(days=1)
    dataAberturaPasta = format(dataAberturaPasta, "%d/%m/%Y")

    complementoAgendamento = ""
    cont = 0
    for x in range(5):

        if (dataAudiencia != ""):  #PARA INICIAR NO 1º AGENDAMENTO
            cont = x + 1
        else:
            cont = (x + 1) - 2  #PARA INICIAR NO 3º AGENDAMENTO
            complementoAgendamento = " A audiência não foi marcada."

        if (x == 0):   #tipo audiencia
            if (dataAudiencia != ""):
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)
                
                # combo destinatário - abrir
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                tipoAgendamento = 'Audiência'              
                appointmentDate = dataAudiencia
                diaAudiencia = int(dataAudiencia.day)
                data = "{}/{}/{}".format(str(diaAudiencia), dataAudiencia.month, dataAudiencia.year)
                appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")                
                appointmentDate = format(appointmentDate, "%d/%m/%Y")

                agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, str(appointmentDate), horaAudienciaFormatada)

                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                # respons. pelo cliente
                y = 1
                found = 0
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text == 'GST' or item.text == 'operacoes' or item.text == '{}'.format(responsavel) ):
                        xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                        element = rf.waitinstance(driver, xPathItem, 1, 'click')
                        element.click()
                        found = found + 1
                        time.sleep(0.3)
                    if (found >= 3):
                        break

                    y = y + 1

                time.sleep(0.3)
            else:
                continue

        elif (x == 1): #tipo Instruções para a Audiência
            if (dataAudiencia != ""):
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)
                
                # combo destinatário - abrir
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.click()

                tipoAgendamento = 'Instruções para a Audiência'
                dAudiencia = "{}/{}/{}".format(str(dataAudiencia.day), dataAudiencia.month, dataAudiencia.year)
                data1 = datetime.datetime.strptime(dAudiencia, "%d/%m/%Y")
                dataIncrementada = data1.date() - timedelta(days=7)
                diaAudiencia = int(dataIncrementada.day)
                wDay = calendar.weekday(dataIncrementada.year, dataIncrementada.month, diaAudiencia)

                if (wDay == 5):   #sábado
                    diaAudiencia = diaAudiencia - 1
                elif (wDay == 6): #domingo
                    diaAudiencia = diaAudiencia - 2

                data = "{}/{}/{}".format(str(diaAudiencia), dataIncrementada.month, dataIncrementada.year)
                appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")                
                appointmentDate = format(appointmentDate, "%d/%m/%Y")
                agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, str(appointmentDate), horaAudienciaFormatada)
                
                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                # operações
                y = 1
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text == 'operacoes'):
                        xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                        element = rf.waitinstance(driver, xPathItem, 1, 'click')
                        element.click()
                        time.sleep(0.3)
                        break
                    y = y + 1
            else:
                continue

        elif (x == 2): #tipo Anexar
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = 'Anexar'            
            dataAbPasta = datetime.datetime.strptime(dataAberturaPasta, "%d/%m/%Y")
            dataIncrementada = dataAbPasta.date() + timedelta(days=1)
            diaAberturaPasta = int(dataIncrementada.day)
            wDay = calendar.weekday(dataIncrementada.year, dataIncrementada.month, diaAberturaPasta)

            if (wDay == 5):   #sábado
                diaAberturaPasta = diaAberturaPasta + 2
            elif (wDay == 6): #domingo
                diaAberturaPasta = diaAberturaPasta + 1

            data = "{}/{}/{}".format(str(diaAberturaPasta), dataIncrementada.month, dataIncrementada.year)
            appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")            
            appointmentDate = format(appointmentDate, "%d/%m/%Y")
            agendamento = "ANEXAR"

            #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
            xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
            listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

           # operações
            y = 1
            for item in listInputs:  #itera inputs recuperados, checa e clica
                if (item.text == 'operacoes'):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                    element = rf.waitinstance(driver, xPathItem, 1, 'click')
                    element.click()
                    time.sleep(0.3)
                    break
                y = y + 1 

        elif (x == 3): #tipo Fotocópia
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)
            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = 'Fotocópia'
            dataAbPasta = datetime.datetime.strptime(dataAberturaPasta, "%d/%m/%Y")
            dataIncrementada = dataAbPasta.date() + timedelta(days=1)
            diaAberturaPasta = int(dataIncrementada.day)
            wDay = calendar.weekday(dataIncrementada.year, dataIncrementada.month, diaAberturaPasta)

            if (wDay == 5):   #sábado
                diaAberturaPasta = diaAberturaPasta + 2
            elif (wDay == 6): #domingo
                diaAberturaPasta = diaAberturaPasta + 1

            data = "{}/{}/{}".format(str(diaAberturaPasta), dataIncrementada.month, dataIncrementada.year)
            appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")            
            appointmentDate = format(appointmentDate, "%d/%m/%Y")
            agendamento = "Fotocópia integral"

            #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
            xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
            listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

            # GST e OPERAÇÕES
            y = 1
            found = 0
            for item in listInputs:  #itera inputs recuperados, checa e clica
                if (item.text == 'GST' or item.text == 'operacoes'):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                    element = rf.waitinstance(driver, xPathItem, 1, 'click')
                    element.click()
                    found = found + 1
                    time.sleep(0.3)                  
                if (found >= 2):
                    break
                y = y + 1

        elif (x == 4): #tipo Ciencia de novo processo
            time.sleep(0.5)
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

            # combo destinatário - abrir
            element = rf.waitinstance(driver, xPathElement, 1, 'click')
            element.click()

            tipoAgendamento = 'Ciencia de novo processo'
            dataAbPasta = datetime.datetime.strptime(dataAberturaPasta, "%d/%m/%Y")
            dataIncrementada = dataAbPasta.date() + timedelta(days=1)
            diaAberturaPasta = int(dataIncrementada.day)
            wDay = calendar.weekday(dataIncrementada.year, dataIncrementada.month, diaAberturaPasta)

            if (wDay == 5):   #sábado
                diaAberturaPasta = diaAberturaPasta + 2
            elif (wDay == 6): #domingo
                diaAberturaPasta = diaAberturaPasta + 1

            data = "{}/{}/{}".format(str(diaAberturaPasta), dataIncrementada.month, dataIncrementada.year)
            appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")            
            appointmentDate = format(appointmentDate, "%d/%m/%Y")
            agendamento = "{} - Pasta aberta, certificar os agendamentos, agendar contestação e pedir OBF caso tenha liminar deferida.{}".format(sigla, complementoAgendamento)
            
            #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
            xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
            listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

            # respons. pelo cliente
            y = 1
            for item in listInputs:  #itera inputs recuperados, checa e clica
                if (item.text == '{}'.format(responsavel) ):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                    element = rf.waitinstance(driver, xPathItem, 1, 'click')
                    element.click()
                    time.sleep(0.3)
                    break
                y = y + 1

        time.sleep(0.3)

        # combo destinatário - fechar
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'click')
        element.click()
        time.sleep(0.3)

        # combo TIPO - ABRIR
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/button'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'click')
        element.click()

        # TIPO DE AGENDAMENTO  -  recupera lista de TIPOS cadastrados no PROMAD
        xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li'.format(cont)
        listInputs = driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag
        
        y = 1
        for item in listInputs:  #itera inputs recuperados, checa e clica
            if (item.text == tipoAgendamento):
                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(cont, y)
                element = rf.waitinstance(driver, xPathItem, 1, 'click')
                element.click()
                time.sleep(0.3)
                break
            y = y + 1

        # CAMPO QUANDO
        time.sleep(0.3)
        xPathElement = '//*[@id="txtDataInicialAgendaProcesso{}"]'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.clear()
        time.sleep(0.3)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(appointmentDate)
        time.sleep(0.3)
        
        try: #se o calendário estiver aberto, será fechado
            driver.execute_script("$('#ui-datepicker-div').css('display', 'none');") #torna elemento invisível novamente
        except:
            pass

        if (dataAudiencia != ""):
            if (x == 0):
                # com HORA
                time.sleep(0.3)
                xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso{}"]'.format(cont)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                time.sleep(0.3)
                element.click()
                
                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(cont)
                element = rf.waitinstance(driver, xPathElement, 1, 'click')
                element.clear()

                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(cont)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')
                element.send_keys(horaAudienciaFormatada)

                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(cont)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')
                element.clear()

                time.sleep(0.3)
                xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(cont)
                element = rf.waitinstance(driver, xPathElement, 1, 'show')

                time.sleep(0.3)
                element.send_keys(horaAudienciaFormatada)
        else:
            pass
            
        # campo agendamento
        time.sleep(0.3)
        xPathElement = '//*[@id="txtDescricaoAgendaProcesso{}"]'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(agendamento)

        # campo resumo
        time.sleep(0.3)
        xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.clear()
        time.sleep(0.3)
        xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(cont)
        element = rf.waitinstance(driver, xPathElement, 1, 'show')
        element.send_keys(agendamento[:30])

        if (x < 4):
            element = rf.waitinstance(driver, '//*[@id="divAgendaCadastrarIncluir"]/a', 1, 'show')  #abrir novo agendamento
            element.click()

    element = rf.waitinstance(driver, '//*[@id="btnAgendarSalvar"]', 1, 'click')
    element.click()

    try:
        element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 1, 'click')
        element.click()
        # rf.createLog(logFile, "REGISTRO {}: Não foi possível realizar os agendamentos para a pasta: {}".format(registro, pasta))
    except:
        pass

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

        if (dfExcel[item, 17]):
            df['horaAudiencia'] = dfExcel[item, 17]
            horaAudiencia = df['horaAudiencia'].strftime("%H:%M")
        else:
            df['horaAudiencia'] = "00:00"
            horaAudiencia = df['horaAudiencia']
        
        if (dfExcel[item, 18]):
            df['comarcaNova'] = dfExcel[item, 18]
        else:
            df['comarcaNova'] = ""

        time.sleep(1)
        urlBack = driver.current_url

        #PARA TESTES
        incluirProcesso(urlPage, df, item)
        criarAgendamentos(df['dataAudiencia'], df['dataContratacao'], horaAudiencia, df['sigla'], df['responsavel'], df['pasta'], item)
        driver.get(urlPage)   # Volta para a tela de pesquisa
        
        #VER POR QUE NÃO RECARREGA A PAGINA DEPOIS DE CONFERIR QUE NÃO EXISTE
        # if (pesquisarPasta(df['pasta']) == False):        #se NÃO existir a pasta, será feito sua abertura
        #     incluirProcesso(urlPage, df, item)
        #     criarAgendamentos(df['dataAudiencia'], df['dataContratacao'], df['horaAudiencia'], df['sigla'], df['responsavel'], df['pasta'], item)
        #     time.sleep(0.5)
        #     driver.get(urlPage)   # Volta para a tela de pesquisa
        # else:
        #     rf.createLog(logFile, "REGISTRO {}: A pasta {} já existe no Promad! Cliente {} - Adverso: {}.".format(item, str(df['pasta']), str(df['razaoSocial']), str(df['adversa'])) )
        #     time.sleep(1.5)
        #     driver.get(urlBack)
        
        item = item + 1
    
    rf.createLog(logFile, '_________________________________________________________________')
    rf.createLog(logFile, 'FIM')

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

while True:

    files =  []
    for file in glob.glob("*.xlsx"):
        files.append(file)

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
                        print("\nINICIANDO WebDriver")
                        driver = rf.iniciaWebdriver(False)
                        # rf.acessToIntegra(driver)
                        rf.acessToIntegra(driver, "cop@dplaw.com.br", "dplaw00612")
                    
                    abrePasta(arquivoAbrirPasta, count)
            else:
                print("\nINICIANDO WebDriver")
                if (driverIniciado == False):
                    driverIniciado = True
                    driver = rf.iniciaWebdriver(False)
                    # rf.acessToIntegra(driver)
                    rf.acessToIntegra(driver, "cop@dplaw.com.br", "dplaw00612")

                abrePasta(arquivoAbrirPasta)

            if (file != ""):
                os.remove(infoLog)
                shutil.move(file, pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'

    if (driverIniciado == True):
        driverIniciado = False
        rf.logoutIntegra(driver)

    time.sleep(1.5)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS\n'.format(hora))
    time.sleep(1.5)
#FIM DO WHILE