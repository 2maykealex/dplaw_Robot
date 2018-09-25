'''
projeto   deeplaw: intern
automatizar abertura de pastas no sistema dplaw
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
import os
import time
import pandas as pd
import pyexcel as pe

'''
variáveis
'''
cliente = {}
'''
------------
'''

'''
funções
'''
def acessToIntegra():
    # acessando a primeira página do sistema promad
    driver.get('http://www.integra.adv.br/')
    driver.maximize_window()

    # realizando o login no sistema

    element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    element.send_keys('robo@dplaw.com.br')
    driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    driver.find_element_by_tag_name('button').click()

    # acessando a pesquisa de clientes no sistema
    element_over = waitinstance(driver, "//*[@id='header']/ul/li[1]/a", 30, 1, 'click')
    hover = ActionChains(driver).move_to_element(element_over)
    hover.perform()

    element = waitinstance(driver, "//*[@id='header']/ul/li[1]/ul/lii[1]/p", 30, 1, 'click')
    element.click()
    #driver.find_element_by_xpath("//*[@id='header']/ul/li[1]/ul/lii[1]/p").click()

    # buscando o cliente e acessando sua pasta
    element = waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys('Cliente Teste')
    driver.find_element_by_id("btnPesquisar").click()

    # ATÉ A URL NÃO MUDAR
    time.sleep(3)
    element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def incluirProcesso(df={}):

    

    # incluindo processo
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]").click()

    # Grupo internodd
    element = waitinstance(driver, "//*[@id='slcGrupo']", 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))

    #Numero do CNJ e do Processo
    print(df['numProcesso'])
    element = waitinstance(driver, '//*[@id="txtNroCnj"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))
    element = waitinstance(driver, '//*[@id="txtNroProcesso"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))

    # Status
    print(df['statusProcessual'])
    element = waitinstance(driver, '//*[@id="slcStatusProcessual"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))

    

    # Comarca
    print(df['comarca'])
    element = waitinstance(driver, '//*[@id="slcComarca"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['comarca']))

    # UF
    element = waitinstance(driver, '//*[@id="txtUf"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['uf']))

    # Responsável
    element = waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/span/span', 30, 1, 'show')
    element.click()
    element_over = waitinstance(driver, "//option[contains(text(),'advbradesco')]", 30, 1, 'show')
    hover = ActionChains(driver).move_to_element(element_over)
    hover.perform()
    element_over.click()
    #format(df['responsavel'][0])

    # Pasta
    element = waitinstance(driver, "txtPasta", 30, 1, 'show', 'id')
    element.send_keys(str(df['pasta']))

    # Data da Contratação
    #element = waitinstance(driver, "txtDataContratacao", 30, 1, 'show', 'id')
    #element.send_keys(str(df['DataContratacao'][0]))

    # Valor da Causa
    element = waitinstance(driver, "txtValorCausa", 30, 1, 'show', 'id')
    element.send_keys(str(df['vCausa']))

    # Abre a aba Parte Adversa
    element = waitinstance(driver, "//*[@id='div_menu17']", 30, 1, 'show')
    element.click()

    # Parte Adversa
    element = waitinstance(driver, "txtNome", 30, 1, 'show', 'id')
    element.send_keys(str(df['adversa']))


    #===================

    # #OUTRA CONDIÇÃO !!!
    # element = waitinstance(driver, "//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]", 30, 5, 'click')
    # element.click()

    # #acessa
    # driver.get('http://www.integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=14421241&codigo2=14421241')
    # //*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]
    # jsbutton = ActionChains(driver).click(element)
    # jsbutton.perform()

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
'''
------------
'''

# acessando diretório do webdriver do chrome
dirpath = os.path.dirname(os.path.realpath(__file__))
chromepath = dirpath + '/chromedriver'
driver = webdriver.Chrome(executable_path = chromepath)
 
dfExcel = pe.get_sheet(file_name='teste_db.xlsx') 

count = dfExcel.number_of_rows()-1

item = 2

acessToIntegra()

# for x in range(1):

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
df['nomeAdversa']      =  dfExcel[item, 9]
df['tipoProcesso']     =  dfExcel[item, 10]
df['comarca']          =  dfExcel[item, 11]
df['localTramite']     =  dfExcel[item, 12]
df['responsavel']      =  dfExcel[item, 13]
df['vCausa']           =  dfExcel[item, 14]
df['dataContratacao']  =  dfExcel[item, 15]
df['uf']               =  dfExcel[item, 16]

# print(df['numProcesso'])
incluirProcesso(df)