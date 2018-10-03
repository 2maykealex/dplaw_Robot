'''
projeto   deeplaw: volumetria
automatizar a inserção da volumetria em pastas existentes no sistema dplaw
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import *
import os
import time
# import pandas as pd
import pyexcel as pe
import datetime
import locale
import sys

# TODO DEIXAR O CÓDIGO MAIS LIMPO DISTRIBUINDO FUNÇÕES PARA OUTROS ARQUIVOS

def iniciaWebdriver():
    # acessando diretório do webdriver do chrome
    dirpath = os.path.dirname(os.path.realpath(__file__))
    chromepath = dirpath + '/chromedriver'
    driver = webdriver.Chrome(executable_path = chromepath)
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

def acessToIntegra():
    # acessando a primeira página do sistema promad
    driver.get('http://www.integra.adv.br/')
    driver.maximize_window()

    # realizando o login no sistema

    element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    element.send_keys('robo@dplaw.com.br')
    driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    driver.find_element_by_tag_name('button').click()

def abreArquivo(volumetriaMes):
    fileName = (volumetriaMes + '.xlsx')
    dfExcel = pe.get_sheet(file_name=fileName) 
    return dfExcel

def pesquisarPasta(pasta = '01700117977'):

    # acessando a pesquisa de clientes no sistema
    # element_over = waitinstance(driver, "//*[@id='header']/ul/li[1]/a", 30, 1, 'click')
    # hover = ActionChains(driver).move_to_element(element_over)
    # hover.perform()
    # element = waitinstance(driver, "//*[@id='header']/ul/li[1]/ul/lii[1]/p", 30, 1, 'click')
    # element.click()
    # driver.find_element_by_xpath("//*[@id='header']/ul/li[1]/ul/lii[1]/p").click()
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = waitinstance(driver, '//*[@id="chkPesquisa139"]', 30, 1, 'show')
    element.click()

    # buscando pasta
    element = waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def inserirVolumetria(volumetriaMes):

    # PREENCHE O CAMPO 3
    element = waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')
    element.send_keys(volumetriaMes)

    # SALVAR ALTERAÇÃO
    time.sleep(2)
    element = waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
    element.click()

    # SALVAR ALTERAÇÃO
    time.sleep(2)
    element = waitinstance(driver, '//*[@id="popup_ok"]', 30, 1, 'show')
    element.click() 


#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL
volumetriaMes = sys.argv[1]
volumetriaMes = volumetriaMes[:-5]

driver = iniciaWebdriver()
acessToIntegra()
dfExcel = abreArquivo(volumetriaMes)
count = dfExcel.number_of_rows()-1

#TODO FAZER LOOPING
pesquisarPasta()
inserirVolumetria(volumetriaMes)
