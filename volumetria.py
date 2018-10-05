'''
projeto   deeplaw: volumetria
automatizar a inserção da volumetria em pastas existentes no sistema dplaw
'''
import sys
import os
import time
import robot_functions as rf

def pesquisarPasta(pasta = '01700117977'):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 30, 1, 'show')
    element.click()

    # buscando pasta
    element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def inserirVolumetria(volumetriaMes):

    element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')

    if (element.get_attribute('value') ==  ''):
        element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')
        element.send_keys(volumetriaMes)

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
        element.click()

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 30, 1, 'show')
        element.click() 
        

#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL
volumetriaMes = sys.argv[1]
volumetriaMes = volumetriaMes[:-5]

driver = rf.iniciaWebdriver()
rf.acessToIntegra(driver)
dfExcel = rf.abreArquivo(volumetriaMes)
count = dfExcel.number_of_rows()-1
item = 1

while (item <= count):
    pasta =  dfExcel[item, 7]
    pesquisarPasta(pasta)
    inserirVolumetria(volumetriaMes)
    item = item + 1

rf.logoutIntegra(driver)
