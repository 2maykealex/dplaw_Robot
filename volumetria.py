# coding=utf-8

import sys
import os
import time
import glob
import robot_functions as rf

def pesquisarPasta(pasta = '01700117977'):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 30, 1, 'show')
    element.click()

    # buscando pasta
    # element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    # element.send_keys(pasta)
    
    time.sleep(1)
    driver.execute_script("document.getElementById('txtPesquisa').value={} ".format(pasta))
    time.sleep(1)

    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def inserirVolumetria(volumetriaMes, pasta):

    element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')

    if (element.get_attribute('value') ==  ''):
        log = "Preenchendo com '{}' na pasta {}".format(volumetriaMes, pasta)
        rf.createLog(arquivo, log)

        volumetriaMes = volumetriaMes.replace('.','-')

        element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')
        time.sleep(1)
        print(volumetriaMes)
        element.send_keys('')
        element.send_keys(volumetriaMes)

        time.sleep(3)
        # driver.execute_script("document.getElementById('txtCampoLivre3').value=volumetriaMes " )
        # time.sleep(1)

        # checando se o elemento CNJ está preenchido
        element = rf.waitinstance(driver, '//*[@id="txtNroCnj"]', 30, 1, 'show', 'xpath')
        if (element.get_attribute("value") != ''):
            # Segredo de Justiça  #por padrão, será marcado não
            element = rf.waitinstance(driver, 'segredoJusticaN', 30, 1, 'show', 'id')
            element.click()
            rf.createLog(arquivo, "--- Marcando NÃO em Segredo de Justiça")

            time.sleep(3)
            element = rf.waitinstance(driver, 'capturarAndamentosS', 30, 1, 'show', 'id')  #só funciona com o browser visivel e maximizado
            element.click()
            rf.createLog(arquivo, "--- Marcando SIM em Capturar andamentos")

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
        element.click()

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 30, 1, 'show')
        element.click() 
    else:
        log = "A pasta {} já está com a volumetria correspondente preenchida! ******".format(pasta)
        rf.createLog(arquivo, log)
        time.sleep(2)
       
def enviaParametros(volumetriaMes):
    log = ">>>>>>>>> ACESSANDO ARQUIVO {}.xlsx".format(volumetriaMes)
    rf.createLog(arquivo, log)
    dfExcel = rf.abreArquivo(volumetriaMes)
    count = dfExcel.number_of_rows()-1
    item = 1

    while (item <= count):         #looping dentro de cada arquivo
        pasta =  dfExcel[item, 7]
        pesquisarPasta(pasta)
        log  =  "Acessando a pasta {}".format(pasta)
        rf.createLog(arquivo, log)
        inserirVolumetria(volumetriaMes, pasta)
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