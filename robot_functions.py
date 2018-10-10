# FUNÇÕES COMUNS QUE ATENDEM A VARIOS ARQUIVOS (INTURN.PY; VOLUMETRIA.PY; ETC...)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
import logging 
from selenium.webdriver.remote.remote_connection import LOGGER
import pyexcel as pe
import os
import time
import pandas as pd

def getFile(arquivo): #TESTE PARA USAR O PANDAS
    fileName = (arquivo + '.xlsx')
    df = pd.read_excel(fileName)
    # df = pd.DataFrame.to_dict (df)

    return df

    # df.to_dict()
        
    # myDict = {}    
    # item = 0
    # for key, val in df.items():
    #     myDict[item] = val
    #     item = item + 1

    
    # for x in myDict.values():
    #     print (x[1])
    # print (myDict[4][0])  # col - lin
    # print (myDict[4][0])

    # return myDict


    # print (df['pasta'][0])

def iniciaWebdriver(modSilent = False):
    # acessando diretório do webdriver do chrome
    dirpath = os.path.dirname(os.path.realpath(__file__))
    chromepath = dirpath + '/chromedriver'
    
    chrome_options = webdriver.ChromeOptions()
    if (modSilent == True):                   # Modo Silencioso: O Navegador fica oculto
        chrome_options.add_argument('--headless')            

    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(executable_path = chromepath, chrome_options=chrome_options)
    
    return driver

def waitinstance(browser, object, time, poll, type, form = 'xpath'):
    if type == 'click':
        if form == 'xpath':
            element = WebDriverWait(browser, time, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, object)))
            return element
        elif form == 'id':
            element = WebDriverWait(browser, time, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.ID, object)))
            return element
    elif type == 'show':
        if form == 'xpath':
            element = WebDriverWait(browser, time, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.XPATH, object)))
            return element
        elif form == 'id':
            element = WebDriverWait(browser, time, poll_frequency = poll,
                                    ignored_exceptions=[NoSuchElementException,
                                    ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.ID, object)))
            return element

def acessToIntegra(driver):
    # acessando a primeira página do sistema promad
    driver.maximize_window()
    driver.get('http://www.integra.adv.br/')    

    # realizando o login no sistema
    element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    element.send_keys('robo@dplaw.com.br')
    driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    driver.find_element_by_tag_name('button').click()

def logoutIntegra(driver):
    driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
    time.sleep(2)
    driver.quit()

def abreArquivo(arquivo):
    fileName = (arquivo + '.xlsx')
    dfExcel = pe.get_sheet(file_name=fileName) 
    return dfExcel
