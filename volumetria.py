# coding=utf-8

import sys
import os
import time
import glob
import shutil
import robot_functions as rf

def pesquisarPasta(pasta):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    rf.checkPopUps(driver)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 1, 'show')
    element.click()
    time.sleep(0.5)
    # buscando pasta    
    driver.execute_script("document.getElementById('txtPesquisa').value={} ".format(pasta))
    # element = rf.waitinstance(driver, 'txtPesquisa', 1, 'show', 'id')
    # element.send_keys(str(pasta))
    
    time.sleep(0.5)

    driver.find_element_by_id("btnPesquisar").click()
    time.sleep(1)    

    retorno = False

    try:
        # SELECIONA O CLIENTE PESQUISADO
        time.sleep(2)    
        element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 1, 'click')
        element.click()
        retorno = True

    except:
        # element = driver.find_element_by_id('loopVazio')  #se encontrar este elemento, é porque não há registros 
        hora = time.strftime("%H:%M:%S")
        print('{} - Não encontrou a pasta'.format(hora))
        
    return retorno

def inserirVolumetria(volumetriaMes, pasta, registro):

    rf.checkPopUps(driver)

    element = rf.waitinstance(driver, 'backgroundPopup', 1, 'show', 'id')

    if (element.value_of_css_property('display') == 'block'):
        driver.execute_script("$('#backgroundPopup').css('display', 'none');") # torna elemento visível

    element = rf.waitinstance(driver, 'carregando', 1, 'show', 'id')
    if (element.value_of_css_property('display') == 'block'):
        driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

    element = rf.waitinstance(driver, 'txtCampoLivre3', 1, 'show', 'id')
    if (element.get_attribute('value') ==  ''):
        print("Preenchendo com '{}' na pasta {} - ARQUIVO {}.XLSX\n".format(volumetriaMes, pasta, volumetriaMes))
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

            element = rf.waitinstance(driver, 'capturarAndamentosS', 1, 'show', 'id')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(2) 

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, 'btnSalvar', 1, 'show', 'id')
        element.click()

        # # SALVAR ALTERAÇÃO - POP_UP
        # time.sleep(2)
        # element = rf.waitinstance(driver, 'popup_ok', 1, 'show', 'id')
        # element.click() 
        rf.createLog(arquivo, "REGISTRO {}: Salvando alterações na pasta {}".format(registro, pasta))
        time.sleep(1)

    else:
        print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
        log = "REGISTRO {}: A pasta {} já está com a volumetria correspondente preenchida! ******".format(registro, pasta)
        rf.createLog(arquivo, log)
        time.sleep(1)
       
def enviaParametros(volumetriaMes, item = 1):
    print('\n')
    dfExcel = rf.abreArquivo(volumetriaMes)
    count = dfExcel.number_of_rows()-1

    trySearch = 1

    while (item <= count):         #looping dentro de cada arquivo
        pasta =  dfExcel[item, 7]

        search = False
        while (trySearch < 3):
            hora = time.strftime("%H:%M:%S")
            print('{} - {}ª tentativa de busca...'.format(hora, trySearch))
            search = pesquisarPasta(pasta)
            if (search == True):
                break
            trySearch = trySearch + 1
        
        if (search == True):
            inserirVolumetria(volumetriaMes, pasta, item)            
        else:
            print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
            log  =  "REGISTRO {}: ========= A pasta {} NÃO EXISTE NO PROMAD!!! =========".format(item, pasta)
            rf.createLog(arquivo, log)
        
        item = item + 1

    rf.createLog(arquivo, '_________________________________________________________________')
    arquivo.writelines('FIM')
    arquivo.close()

#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL

path = os.getcwd() + "\\files\\volumetrias" # obtem o caminho do script e add a pasta volumetrias
logsPath = os.getcwd() + "\\files\\volumetrias\\logs"

pathExecutados = path + "\\arquivos_executados"

if (os.path.exists(pathExecutados) == False):
    os.mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado - 

if (os.path.exists(path) == False):
    os.mkdir(path)   # Se o diretório Volumetrias não existir, será criado - 

if (os.path.exists(logsPath) == False):
    os.mkdir(logsPath)   # Se o diretório \Volumetrias\files não existir, será criado - 

os.chdir(path) # seleciona o diretório do script

driverIniciado = False

while True:

    files =  []
    
    for file in glob.glob("*.xlsx"):        
        files.append(file)
        
    if (files):
       
        for file in files:
            volumetriaMes = file
            volumetriaMes = volumetriaMes[:-5]
            
            if (file != ""):
                infoLog = "EXECUTANDO {}.txt".format(file.upper())
                arquivo = open(infoLog, 'w+')  
            
            logFile = logsPath + "\\_log_{}.txt".format(volumetriaMes)
            
            if (os.path.isfile(logFile)):
                arquivoOriginal = open(logFile, 'r')  
                conteudo = arquivoOriginal.readlines()
                count = len(open(logFile).readlines())
                linha = ""

                arquivo = open(logFile, 'w+')  
                for linha in conteudo:
                    arquivo.writelines(linha)
                              
                if (linha == "FIM"): #ultima linha do arquivo
                    print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(volumetriaMes))
                    
                else:                          # continua o preenchimento do log já existente 
                    if (driverIniciado == False):       
                        driverIniciado = True 
                        driver = rf.iniciaWebdriver(False)                        
                        rf.acessToIntegra(driver)
                    
                    if (count >= 1):
                        enviaParametros(volumetriaMes, count)
                    else:
                        enviaParametros(volumetriaMes, 1)
                
                arquivoOriginal.close()

            else:
                arquivo = open(logFile, 'w+')                
                log = "_________ARQUIVO DE LOG CRIADO DO ARQUIVO {}.xlsx_________".format(volumetriaMes)
                rf.createLog(arquivo, log)

                if (driverIniciado == False):       
                    driverIniciado = True 
                    driver = rf.iniciaWebdriver(False)                        
                    rf.acessToIntegra(driver)

                enviaParametros(volumetriaMes)

            arquivo.close()

            if (file != ""):
                os.remove(infoLog)
            
            shutil.move(file, pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
        
    if (driverIniciado == True):  
        driverIniciado = False
        rf.logoutIntegra(driver)


    time.sleep(3)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS\n'.format(hora))
    time.sleep(3)