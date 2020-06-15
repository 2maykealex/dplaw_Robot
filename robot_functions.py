#coding=utf-8
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import *
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.remote.remote_connection import LOGGER

from selenium_functions import SeleniumFunctions

import pyexcel as pe
import logging
import os
import platform
import time
import psutil  # to check pIDs

def acessToIntegra(driver, login, password):
    # acessando a primeira página do sistema promad
    try:
        driver.maximize_window()
        driver.get('https://integra.adv.br/login-integra.asp')
        # realizando o login no sistema
        driver.execute_script("document.getElementById('login_email').value='{}'".format(login))
        driver.execute_script("document.getElementById('login_senha').value='{}'".format(password))
        time.sleep(0.2)
        driver.find_element_by_tag_name('button').click()
        time.sleep(0.2)
        checkPopUps(driver)
        return True
    except:
        return False

def checkPopUps(driver):
    popupOk = False
    try:
        driver.execute_script("$('.popup_block').css('display', 'none');")
        popupOk = True
    except:
        pass

    try:
        driver.execute_script("$('#menuvaimudar').css('display', 'none');")
        popupOk = True
    except:
        pass

    try:
        driver.execute_script("$('#divFecharAvisoPopUp').css('display', 'none');")
        popupOk = True
    except:
        pass

    try:
        driver.execute_script("$('#backgroundPopup').css('display', 'none');")
        popupOk = True
    except:
        pass

    try:
        driver.execute_script("$('#carregando').css('display', 'none');")
        popupOk = True
    except:
        pass

    try:
        driver.execute_script("$('#card').css('display', 'none');")
        popupOk = True
    except:
        pass

    if (popupOk == True):
        time.sleep(2)

    # print('\nPOPUPS OK!!!!\n')

def abreArquivo(arquivo, extensao, path=""):
    fileName = "{}\\{}.{}".format(path, arquivo, extensao)
    # fileName = (arquivo + '.' + extensao)
    dfExcel = pe.get_sheet(file_name=fileName)
    return dfExcel

def checkEndFile(log):
    arquivo =  open(log, 'r')
    message = arquivo.readlines()
    arquivo.close()

    lastLine = message[len(message)-1]
    # count = len(open(log).readlines()) + 1
    return (lastLine)

def createLog(logFile, message = "", tipo = 'w+', printOut = True, onlyText=False):

    if (os.path.isfile(logFile)): #se o log não existir, cria-se
        arquivo =  open(logFile, 'a')
    else:
        arquivo = open(logFile, tipo)

    writeLog = "{}".format(message)

    # if (message == "FIM"):
    #     writeLog = "{}".format(message)
    # else:
        # message = "{}".format(message)
        # if (onlyText == False):
        #     # writeLog = "{}__{}: {}\n".format(hoje, horaStr, message)
        #     writeLog = "{}".format(message)
        # else:
        #     writeLog = "{}".format(message)

    if (arquivo != ""):
        arquivo.writelines(writeLog)
    if (printOut):
        print(writeLog)

    arquivo.close()

def logoutIntegra(driver):
    driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
    time.sleep(2)
    driver.quit()

def createPID(pidName, pidNumber):
    logsPath = "{}\\pIDs".format(os.getcwd())
    logFile = logsPath +"\\{}__{}.pid".format(pidName, pidNumber)

    if (os.path.exists(logsPath) == False):
        os.mkdir(logsPath)   # Se o diretório pIDs não existir, será criado

    if (not(os.path.isfile(logFile))): #se o log não existir, cria-se
        arquivo =  open(logFile, 'w')
        arquivo.close()
        return True

def checkPID(pidNumber):
    if psutil.pid_exists(pidNumber):
        print ("pid {} existe".format(pidNumber))
        return True
    return False

def acessaMenuPesquisa(driver):
    #menu CLIENTES
    time.sleep(1)
    try:
        element = waitinstance(driver, '//*[@id="header"]/ul/li[1]', 2, 'click')
        time.sleep(1.5)
        element.click()
    except:
        print("ERRO AO CLICAR NO MENU CLIENTES")
        return False

    #submenu PESQUISAR CLIENTE
    try:
        element = waitinstance(driver, '//*[@id="header"]/ul/li[1]/ul/lii[1]/p', 2, 'click')  # ==>> https://www.integra.adv.br/integra4/modulo/21/default.asp
        time.sleep(1.5)
        element.click()
    except:
        print("ERRO AO CLICAR NO SUBMENU PESQUISAR CLIENTES")
        return False
    return True

def pesquisarCliente(driver, search, tipoPesquisa):

    menuPesquisa = acessaMenuPesquisa(driver)

    if (menuPesquisa):
        time.sleep(2)
        checkPopUps(driver)
        xPathOption = ''

        #tipo de pesquisa (opções)
        if (tipoPesquisa == 'pasta'):
            xPathOption = '//*[@id="chkPesquisa139"]'
            xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[6]'
        elif (tipoPesquisa == 'cliente'):
            xPathOption = '//*[@id="chkPesquisa133"]'
            xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[4]'
        elif (tipoPesquisa == 'processo'):
            xPathOption = '//*[@id="chkPesquisa137"]'
            xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[6]'

        element = waitinstance(driver, '{}'.format(xPathOption), 1, 'click')
        element.click()
        time.sleep(0.5)

        # valor do parâmetro
        driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(search))
        time.sleep(2)
        print("pesquisar pasta {}".format(search))
        #botão pesquisar
        driver.find_element_by_id("btnPesquisar").click()
        time.sleep(2)

        try:
            #Checa se não existe registros para essa pasta
            element = driver.find_element_by_id('loopVazio').is_displayed()
            hora = time.strftime("%H:%M:%S")
            print('{} - Não encontrou a pasta'.format(hora))
            retorno = False

        except:
            # SELECIONA O CLIENTE PESQUISADO        -  clica no primeiro item encontrado(não poderia ter duas pastas com o mesmo número)
            try:
                element = waitinstance(driver, "{}/div".format(xPathClick), 1, 'click')
            except:
                try:
                    element = waitinstance(driver, "{}/div".format(xPathClick), 1, 'click')
                except:
                    pass
                    # element = waitinstance(driver, '//*[@id="divCliente"]/div[3]/table/tbody/tr', 1, 'click')  #clica no registro -> abre a pasta
            retorno = True

    else:
        retorno = False
        element = ''

    return retorno, element

def uploadFile(driver):
    checkPopUps(driver)
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
    element = waitinstance(driver, '//*[@id="btnSalvar"]', 1, 'show')
    element.click()
    # POP UP (OK)
    time.sleep(1)
    element = waitinstance(driver, '//*[@id="popup_ok"]', 1, 'show')
    element.click()

def checkIfTest():
    pathRootScript = os.path.abspath(os.path.dirname(__file__))
    pathFileTeste = pathRootScript + "\\teste.txt"
    if (os.path.isfile(pathFileTeste)):
        return True
    else:
        return False

def pprint(message, tName):
    print('{} - {}'.format(tName, message))


# PJE - FAZER EM OUTRO ARQUIVO

    # def acessToPJE(arquivo, driver):
#     # acessando a primeira página do sistema promad
#     # TODO VER LOGS
#     driver.maximize_window()
#     createLog(arquivo, '>>>>>>>>> ACESSANDO O SITE http://www.integra.adv.br/...')
#     driver.get('http://www.pje.jus.br/navegador/')

#     # selecionando o estado
#     element = waitinstance(driver, "/html/body/div[3]/div/div[1]/select", 1, 'show')
#     select = Select(element)
#     select.select_by_visible_text(str('Rondônia'))

#     # selecionando o Tribunal
#     element = waitinstance(driver, "/html/body/div[3]/div/div[2]/select", 1, 'show')
#     select = Select(element)
#     select.select_by_visible_text(str('TJRO - 1º grau'))

#     driver.find_element_by_tag_name('button').click()

    # TJRO - 1º grau
    # TJRO - 2º grau
    # TRF 1ª Região - 1º grau
    # TRF 1ª Região - 2º grau
    # TRT 14 - 1º grau
    # TRT 14 - 2º grau