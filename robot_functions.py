#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import logging 
from selenium.webdriver.remote.remote_connection import LOGGER
import pyexcel as pe
import os
import platform
import time
import psutil  # to check pIDs

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
    
    if (popupOk == True):
        time.sleep(2)

    # print('\nPOPUPS OK!!!!\n')

def waitinstance(driver, object, poll, type, form = 'xpath'):

    timeOut = 40 #segundos
    count = 1
    while (count < 8):
        try:
            if type == 'click':
                if form == 'xpath':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, object)))
                    # return element
                elif form == 'id':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.ID, object)))
                elif form == 'class':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.CLASS_NAME, object)))
                    # return element
            elif type == 'show':
                if form == 'xpath':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.XPATH, object))) 
                    # return element
                elif form == 'id':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.ID, object)))
                elif form == 'class':
                    element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                            ignored_exceptions=[NoSuchElementException,
                                            ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.CLASS_NAME, object)))
            return element
        except:
            count = count + 1
            hora = time.strftime("%H:%M:%S")
            print('{} - {} - Elemento ainda não foi encontrado!'.format(count, hora))
    
def iniciaWebdriver(modSilent = False, monitor = 2):

    sistemaOperacional = platform.system()

    if (sistemaOperacional == 'Windows'):
        # acessando diretório do webdriver do chrome no WINDOWS
        dirpath = os.path.dirname(os.path.realpath(__file__))
        chromepath = dirpath + '/chromedriver.exe'
    elif (sistemaOperacional == 'Linux'):
        # acessando diretório do webdriver do chrome no LINUX
        dirpath = '/usr/bin'
        chromepath = dirpath + '/chromedriver'
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    #chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    if (modSilent == True):                   # Modo Silencioso: O Navegador fica oculto
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument("--log-level=3")
        
    slow = False # True - Internet Lenta  / False - Internet normal

    if (slow):
        chrome_options.add_argument("--disable-application-cache")
    
    driver = webdriver.Chrome(executable_path = chromepath, chrome_options=chrome_options)
    
    if (monitor == 2):
        driver.set_window_position(2000,0)   # ATIVA A EXECUÇÃO NO SEGUNDO MONITOR
    
    slowInternet(driver, slow)    
    return driver

def abreArquivo(arquivo, extensao, path=""):
    fileName = "{}\\{}.{}".format(path, arquivo, extensao)
    # fileName = (arquivo + '.' + extensao)
    dfExcel = pe.get_sheet(file_name=fileName) 
    return dfExcel

def checkEndFile(log):
    arquivo =  open(log, 'r')
    arquivoLinhas = arquivo.readlines() 
    arquivo.close()

    lastLine = arquivoLinhas[len(arquivoLinhas)-1]
    count = len(open(log).readlines()) + 1
    return (lastLine, count)

def createLog(logFile, message = "", tipo = 'w+', printOut = True, onlyText=False):
    
    if (os.path.isfile(logFile)): #se o log não existir, cria-se
        arquivo =  open(logFile, 'a')
    else:
        arquivo = open(logFile, tipo)

    hoje = "%s" % (time.strftime("%Y-%m-%d"))
    hora = time.strftime("%H:%M:%S")
    horaStr = hora.replace(':', '-')
    
    if (message == "FIM"):
        writeLog = "{}".format(message) 
    else:
        if (onlyText == False):
            writeLog = "{}__{}: {}\n".format(hoje, horaStr, message)
        else:
            writeLog = "{}".format(message)
    
    if (arquivo != ""):
        arquivo.writelines(writeLog)
    if (printOut):
        print(writeLog)
    
    arquivo.close()
 
def slowInternet(driver, active = False):   # Para simular internet Lenta
    if (active == True):
        driver.set_network_conditions(
        offline=False,
        latency=3,  # additional latency (ms)
        download_throughput= 50 * 1024,  # maximal throughput
        upload_throughput= 50 * 1024)  # maximal throughput

def acessToIntegra(driver, login, password):
    # acessando a primeira página do sistema promad    
    try:
        driver.maximize_window()
        # createLog(arquivo, '>>>>>>>>> ACESSANDO O SITE http://www.integra.adv.br/... <<<<<<<<<')
        driver.get('http://www.integra.adv.br/')

        # realizando o login no sistema
        element = waitinstance(driver, "login_email", 1, 'show', 'id')
        element.send_keys("{}".format(login))
        driver.execute_script("document.getElementById('login_senha').value='{}'".format(password))
        time.sleep(1)
        # createLog(arquivo, 'FAZENDO LOGIN NO SITE')
        element = driver.find_element_by_tag_name('button')
        element.click()

        time.sleep(1)    # Verifica se existe um pop-up no início e o fecha

        checkPopUps(driver)
        return True
    except:
        return False
    
def logoutIntegra(driver):
    driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
    time.sleep(2)
    driver.quit()

def acessToPJE(arquivo, driver):
    # acessando a primeira página do sistema promad
    # TODO VER LOGS
    driver.maximize_window()
    createLog(arquivo, '>>>>>>>>> ACESSANDO O SITE http://www.integra.adv.br/...')
    driver.get('http://www.pje.jus.br/navegador/')        

    # selecionando o estado
    element = waitinstance(driver, "/html/body/div[3]/div/div[1]/select", 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str('Rondônia'))

    # selecionando o Tribunal
    element = waitinstance(driver, "/html/body/div[3]/div/div[2]/select", 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str('TJRO - 1º grau'))

    driver.find_element_by_tag_name('button').click()

    # TJRO - 1º grau
    # TJRO - 2º grau
    # TRF 1ª Região - 1º grau
    # TRF 1ª Região - 2º grau
    # TRT 14 - 1º grau
    # TRT 14 - 2º grau

def createPID(pidName, pidNumber):
    logsPath = os.getcwd()+"\\pIDs"
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

def pesquisarPasta(driver, pasta):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    checkPopUps(driver)

    # selecionar opção pesquisa por pasta
    element = waitinstance(driver, '//*[@id="chkPesquisa139"]', 1, 'show')
    element.click()
    time.sleep(0.5)

    # buscando pasta
    driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(pasta))
    time.sleep(2)
    print("pesquisar pasta {}".format(pasta))
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
            element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[6]", 1, 'click')
        except:
            element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[6]/div", 1, 'click')
        retorno = True

    return retorno, element

def pesquisarProcesso(driver, processo):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    checkPopUps(driver)

    # selecionar opção pesquisa por processo
    element = waitinstance(driver, '//*[@id="chkPesquisa137"]', 1, 'show')
    element.click()
    time.sleep(0.5)

    # buscando processo
    driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(processo))
    time.sleep(2)
    print("pesquisar processo {}".format(processo))
    driver.find_element_by_id("btnPesquisar").click()
    time.sleep(2)

    try:
        #Checa se não existe registros para essa processo
        element = driver.find_element_by_id('loopVazio').is_displayed()
        hora = time.strftime("%H:%M:%S")
        print('{} - Não encontrou a processo'.format(hora))
        retorno = False

    except:
        # SELECIONA O CLIENTE PESQUISADO        -  clica no primeiro item encontrado(não poderia ter duas pastas com o mesmo número)
        try:
            element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[6]", 1, 'click')
        except:
            element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[6]/div", 1, 'click')
        retorno = True

    return retorno, element

def pesquisarCliente(driver, cliente):
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    try:
        urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
        driver.get(urlPage)

        checkPopUps(driver)

        # buscando o cliente e acessando sua pasta
        driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(cliente) )
        time.sleep(2)
        print("pesquisar cliente {}".format(cliente))
        driver.find_element_by_id("btnPesquisar").click()

        # ATÉ A URL NÃO MUDAR
        time.sleep(2)
        # SELECIONA O CLIENTE PESQUISADO
        element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 2, 'click')
        time.sleep(2)
        element.click()
        time.sleep(2)
        return True
    except:
        return False

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