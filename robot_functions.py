# FUNÇÕES COMUNS QUE ATENDEM A VARIOS ARQUIVOS (INTURN.PY; VOLUMETRIA.PY; ETC...)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.common.exceptions import TimeoutException
import logging 
from selenium.webdriver.remote.remote_connection import LOGGER
import pyexcel as pe
import os
import time
import pandas as pd

def checkElement(driver, element):
    while True:
        if driver.find_elements_by_css_selector("{}".format(element)):  #AGUARDA O CARREGAMENTO DO ÚLTIMO ELEMENTO DA PÁGINA
            # print("A PÁGINA FOI CARREGADA")
            break
        else:
            print('---AGUARDANDO O CARREGAMENTO TOTAL DA PÁGINA---')

def getFile(arquivo): #TESTE PARA USAR O PANDAS
    fileName = (arquivo + '.xlsx')
    df = pd.read_excel(fileName)
    return df

def abreArquivo(arquivo):
    fileName = (arquivo + '.xlsx')
    dfExcel = pe.get_sheet(file_name=fileName) 
    return dfExcel

def createLog(arquivo, log, printOut = True):
    hoje = "%s" % (time.strftime("%Y-%m-%d"))
    hora = time.strftime("%H:%M:%S")
    horaStr = hora.replace(':', '-')
    writeLog = "{}__{}: {}\n".format(hoje, horaStr,log)
    if (arquivo != ""):
        arquivo.writelines(writeLog)
    if (printOut):
        print(writeLog)
    return writeLog
    
def iniciaWebdriver(modSilent = False):
    # acessando diretório do webdriver do chrome
    dirpath = os.path.dirname(os.path.realpath(__file__))
    chromepath = dirpath + '/chromedriver'
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    chrome_options.add_argument('--disable-gpu')

    if (modSilent == True):                   # Modo Silencioso: O Navegador fica oculto
        chrome_options.add_argument('--headless')

    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(executable_path = chromepath, chrome_options=chrome_options)
    
    return driver

def waitinstance(browser, object, timeOut, poll, type, form = 'xpath'):
    if type == 'click':
        if form == 'xpath':
            element = WebDriverWait(browser, timeOut, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, object)))
            return element
        elif form == 'id':
            element = WebDriverWait(browser, timeOut, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.ID, object)))
            return element
    elif type == 'show':
        if form == 'xpath':
            element = WebDriverWait(browser, timeOut, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.XPATH, object))) 
            return element
        elif form == 'id':
            element = WebDriverWait(browser, timeOut, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.ID, object)))
            return element

def acessToIntegra(arquivo, driver):
    # acessando a primeira página do sistema promad    
    driver.maximize_window()
    createLog(arquivo, '>>>>>>>>> ACESSANDO O SITE http://www.integra.adv.br/... <<<<<<<<<')
    driver.get('http://www.integra.adv.br/')

    # realizando o login no sistema
    element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    element.send_keys('robo@dplaw.com.br')
    driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    driver.find_element_by_tag_name('button').click()
    createLog(arquivo, 'FAZENDO LOGIN NO SITE')
    
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
    element = waitinstance(driver, "/html/body/div[3]/div/div[1]/select", 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str('Rondônia'))

    # selecionando o Tribunal
    element = waitinstance(driver, "/html/body/div[3]/div/div[2]/select", 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str('TJRO - 1º grau'))

    driver.find_element_by_tag_name('button').click()

    # TJRO - 1º grau
    # TJRO - 2º grau
    # TRF 1ª Região - 1º grau
    # TRF 1ª Região - 2º grau
    # TRT 14 - 1º grau
    # TRT 14 - 2º grau





    # # realizando o login no sistema
    # element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    # element.send_keys('robo@dplaw.com.br')
    # driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    
    # createLog("", 'FAZENDO LOGIN NO SITE')
