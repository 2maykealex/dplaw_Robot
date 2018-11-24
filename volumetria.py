# coding=utf-8

import sys
import os
import time
import glob
import robot_functions as rf

def pesquisarPasta(pasta):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 1, 'show')
    element.click()
    time.sleep(1)
    
    # buscando pasta    
    driver.execute_script("document.getElementById('txtPesquisa').value={} ".format(pasta))
    time.sleep(1)

    driver.find_element_by_id("btnPesquisar").click()
    log = "Pesquisando pela pasta '{}' ".format(pasta)
    rf.createLog(arquivo, log)

    time.sleep(3)    
    # element = rf.waitinstance(driver, '//*[@id="loopVazio"]', 1, 'show')

    try:
        element = driver.find_element_by_id('loopVazio')  #se encontrar este elemento, é porque não há registros 
        return False
    except:
        # SELECIONA O CLIENTE PESQUISADO
        time.sleep(3)    
        element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
        element.click()
        return True

def inserirVolumetria(volumetriaMes, pasta):

    element = rf.waitinstance(driver, 'backgroundPopup', 1, 'show', 'id')

    if (element.value_of_css_property('display') == 'block'):
        driver.execute_script("$('#backgroundPopup').css('display', 'none');") # torna elemento visível

    element = rf.waitinstance(driver, 'carregando', 1, 'show', 'id')
    if (element.value_of_css_property('display') == 'block'):
        driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível


    element = rf.waitinstance(driver, 'txtCampoLivre3', 1, 'show', 'id')
    if (element.get_attribute('value') ==  ''):
        log = "Preenchendo com '{}' na pasta {}".format(volumetriaMes, pasta)
        rf.createLog(arquivo, log)
        time.sleep(2) 

        driver.execute_script("document.getElementById('txtCampoLivre3').value='{}' ".format(volumetriaMes) )
        time.sleep(2)

        # checando se o elemento CNJ está preenchido
        element = rf.waitinstance(driver, 'txtNroCnj', 1, 'show', 'id')
        if (element.get_attribute("value") != ''):
            # Segredo de Justiça  #por padrão, será marcado não
            element = rf.waitinstance(driver, 'segredoJusticaN', 1, 'show', 'id')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2) 
            rf.createLog(arquivo, "--- Marcando NÃO em Segredo de Justiça")
            time.sleep(2)

            element = rf.waitinstance(driver, 'capturarAndamentosS', 1, 'show', 'id')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2) 
            rf.createLog(arquivo, "--- Marcando SIM em Capturar andamentos")

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, 'btnSalvar', 1, 'show', 'id')
        element.click()

        # SALVAR ALTERAÇÃO - POP_UP
        time.sleep(2)
        element = rf.waitinstance(driver, 'popup_ok', 1, 'show', 'id')
        element.click() 
        rf.createLog(arquivo, "--- Salvando alterações na pasta {}".format(pasta))
        time.sleep(1)

    else:
        log = "A pasta {} já está com a volumetria correspondente preenchida! ******".format(pasta)
        rf.createLog(arquivo, log)
        time.sleep(1)
       
def enviaParametros(volumetriaMes):
    print('\n')
    log = ">>>>>>>>> ACESSANDO ARQUIVO {}.xlsx".format(volumetriaMes)
    rf.createLog(arquivo, log)
    dfExcel = rf.abreArquivo(volumetriaMes)
    count = dfExcel.number_of_rows()-1
    item = 1

    while (item <= count):         #looping dentro de cada arquivo
        pasta =  dfExcel[item, 7]
        print("\nLinha => {} do ARQUIVO {}.xlsx".format(item, volumetriaMes))
        if (pesquisarPasta(pasta) == True):
            log  =  "Acessando a pasta {}".format(pasta)
            rf.createLog(arquivo, log)
            inserirVolumetria(volumetriaMes, pasta)
        else:
            log  =  "========= A pasta {} NÃO EXISTE NO PROMAD!!! =========".format(pasta)
            rf.createLog(arquivo, log)
        item = item + 1


#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL

path = os.getcwd() + "/volumetrias" # obtem o caminho do script e add a pasta volumetrias
logsPath = os.getcwd() + "/logs"

if (os.path.exists(path) == False):
    os.mkdir(path)   # Se o diretório Volumetrias não existir, será criado - 

os.chdir(path) # seleciona o diretório do script

print('\n========== SELECIONE UMA DAS OPÇÕES ABAIXO ==========\n')
files =  []
print('0  =>  EXECUTAR TODOS OS ARQUIVOS DA PASTA  "VOLUMETRIAS" ')
print('-------------------------------------------')
for file in glob.glob("*.xlsx"):
    # print('-------------------------------------------')
    files.append(file)
    print(len(files), ' => ', files[-1])    
print('-------------------------------------------')

selectedFile = int(input('Digite sua opção: '))

hoje = "%s" % (time.strftime("%Y_%m_%d"))
hora = time.strftime("%H:%M:%S")
horaStr = hora.replace(':', '-')
logFile = logsPath + "/_{}_{}_log_volumetrias.txt".format(hoje, horaStr)

if (os.path.exists(logsPath) == False):
    os.mkdir(logsPath)   # Se o diretório Logs não existir, será criado

arquivo = open(logFile, 'w+')

print('\n\n\n')
rf.createLog(arquivo, '______________________ARQUIVO DE LOG CRIADO______________________')

driver = rf.iniciaWebdriver(False)
print('\n')
rf.acessToIntegra(arquivo, driver)

if (selectedFile-1 < 0):
    # opção 0 selecionada
    for file in files:
        volumetriaMes = file
        volumetriaMes = volumetriaMes[:-5]
        enviaParametros(volumetriaMes)
else:
    volumetriaMes = files[selectedFile -1]
    volumetriaMes = volumetriaMes[:-5]
    enviaParametros(volumetriaMes)

rf.createLog(arquivo, '> > > NÃO HÁ MAIS ARQUIVOS PARA EXECUÇÃO! SCRIPT ENCERRADO!')
rf.createLog(arquivo, '_________________________________________________________________')
arquivo.close()
rf.logoutIntegra(driver)