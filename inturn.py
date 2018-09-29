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
# import pandas as pd
import pyexcel as pe
import datetime
import locale

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

def acessToIntegra():
    # acessando a primeira página do sistema promad
    driver.get('http://www.integra.adv.br/')
    driver.maximize_window()

    # realizando o login no sistema

    element = waitinstance(driver, "login_email", 30, 1, 'show', 'id')
    element.send_keys('robo@dplaw.com.br')
    driver.find_element_by_id("login_senha").send_keys('dplaw00612')
    driver.find_element_by_tag_name('button').click()

def pesquisarCliente(cliente = 'Cliente teste'):
    # acessando a pesquisa de clientes no sistema
    element_over = waitinstance(driver, "//*[@id='header']/ul/li[1]/a", 30, 1, 'click')
    hover = ActionChains(driver).move_to_element(element_over)
    hover.perform()

    element = waitinstance(driver, "//*[@id='header']/ul/li[1]/ul/lii[1]/p", 30, 1, 'click')
    element.click()
    #driver.find_element_by_xpath("//*[@id='header']/ul/li[1]/ul/lii[1]/p").click()

    # buscando o cliente e acessando sua pasta
    element = waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(cliente)
    driver.find_element_by_id("btnPesquisar").click()

    # ATÉ A URL NÃO MUDAR
    time.sleep(3)
    # SELECIONA O CLIENTE PESQUISADO
    element = waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def incluirProcesso(urlPage, df={}):

    if (urlPage == ""):
        urlPage =  driver.current_url
        print (urlPage)

    # incluindo processo    
    driver.find_element_by_xpath("//*[@id='frmProcesso']/table/tbody/tr[2]/td/div[1]").click()

    # Grupo internodd
    element = waitinstance(driver, "//*[@id='slcGrupo']", 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['gpProcesso']))

    #Numero do CNJ e do Processo
    element = waitinstance(driver, '//*[@id="txtNroCnj"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))
    element = waitinstance(driver, '//*[@id="txtNroProcesso"]', 30, 1, 'show', 'xpath')
    element.send_keys(str(df['numProcesso']))

    # Status
    element = waitinstance(driver, '//*[@id="slcStatusProcessual"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['statusProcessual']))


    ########### COLUNA 2 DA PÁGINA

    # Pasta
    element = waitinstance(driver, '//*[@id="txtPasta"]', 30, 1, 'show')
    element.send_keys(str(df['pasta']))

    # Grupo Local trâmite
    element = waitinstance(driver, '//*[@id="slcNumeroVara"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['localTr']))
    element = waitinstance(driver, '//*[@id="slcLocalTramite"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['localTramite']))

    # Comarca
    element = waitinstance(driver, '//*[@id="slcComarca"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['comarca']))

    # UF
    element = waitinstance(driver, '//*[@id="txtUf"]', 30, 1, 'show')
    select = Select(element)
    select.select_by_visible_text(str(df['uf']))

    # RESPONSÁVEL    
    driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

    comboResponsavel = waitinstance(driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 30, 1, 'show')
    comboResponsavel.click()  # clica e abre as opções
    
    element = waitinstance(driver, responsavelXpath(df['responsavel']), 30, 1, 'show')
    element.click() # seleciona o item desejado

    comboResponsavel.click() # clica para fechar as opções do combo
    driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
    
    # Data da Contratação
    element = waitinstance(driver, '//*[@id="txtDataContratacao"]', 30, 1, 'show')
    element.send_keys(str(df['dataContratacao']))

    # Valor da Causa
    element = waitinstance(driver, '//*[@id="txtValorCausa"]', 30, 1, 'show')
    element.send_keys(str(df['vCausa']))

    # Abre a aba Parte Adversa
    element = waitinstance(driver, "//*[@id='div_menu17']", 30, 1, 'show')
    element.click()

    # Parte Adversa
    element = waitinstance(driver, '//*[@id="txtNome"]', 30, 1, 'show')
    element.send_keys(str(df['adversa']))

    # Botão salvar
    # element = waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
    # element.click()

    # Link Ficha do cliente (voltar)
    # pesquisarCliente()

    # element_over = waitinstance(driver, "//*[@id='header']/ul/li[1]/a", 30, 1, 'click')
    # hover = ActionChains(driver).move_to_element(element_over)
    # hover.perform()

    # element = waitinstance(driver, "//*[@id='header']/ul/li[1]/ul/lii[1]/p", 30, 1, 'click')
    # element.click()

    time.sleep(5)
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

urlPage = ""
dfExcel = pe.get_sheet(file_name='teste_db.xlsx') 

count = dfExcel.number_of_rows()-1
print ('contador ', count)
acessToIntegra()
pesquisarCliente()

item = 1

while (item <= count):
    print('item: ', item)

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