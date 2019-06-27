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
        retorno = False
        
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
        rf.createLog(logFile, "REGISTRO {}: Salvando alterações na pasta {}".format(registro, pasta))
        time.sleep(1)
        return True

    else:
        print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
        log = "REGISTRO {}: A pasta {} já está com a volumetria correspondente preenchida! ******".format(registro, pasta)
        rf.createLog(logFile, log)
        time.sleep(1)
        return False
       
def enviaParametros(volumetriaMes, item = 1, extensao="xlsx"):
    try:
        print('\n')
        dfExcel = rf.abreArquivo(volumetriaMes, extensao)
        count = dfExcel.number_of_rows()-1

        while (item <= count):         #looping dentro de cada arquivo
            pasta =  dfExcel[item, 7]
            trySearch = 1
            search = False
            while (trySearch < 4):
                hora = time.strftime("%H:%M:%S")
                print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                try:
                    search = pesquisarPasta(pasta)
                except:
                    return False

                if (search == True):
                    break
                trySearch = trySearch + 1
            print('\n')

            if (search == True):
                try:
                    inserirVolumetria(volumetriaMes, pasta, item)
                except:
                    return False
            else:
                print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
                log  =  "REGISTRO {}: ========= A pasta {} NÃO EXISTE NO PROMAD!!! =========".format(item, pasta)
                rf.createLog(logFile, log)
            
            item = item + 1

        rf.createLog(logFile, '_________________________________________________________________')
        rf.createLog(logFile, 'FIM')
        return True
    except:
        return False

#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL
pidNumber = str(os.getpid())
print(pidNumber)

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
driver = None

while True:
    files = []
    for file in glob.glob("*.xlsx"):
        files.append(file)
        
    if (files):
        for file in files:
            file = file.split('.')
            volumetriaMes = '.'.join(file[:-1])#file[0]
            extensao = file[-1]
            
            if (file != ""):
                infoLog = "EXECUTANDO {}.txt".format(file[0].upper())
                arquivo = open(infoLog, 'w+')
                arquivo.close() 
            
            logFile = logsPath + "\\_log_{}.txt".format(volumetriaMes)
            
            abreWebDriver = None
            executaVolumetria = None
            if (os.path.isfile(logFile)):
                linha, count = rf.checkEndFile(logFile)
                              
                if (linha == "FIM"): #ultima linha do arquivo
                    print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(volumetriaMes))
                    
                else:                          # continua o preenchimento do log já existente 
                    if (driverIniciado == False):
                        driverIniciado = True 
                        print("\nINICIANDO WebDriver")
                        rf.createPID(volumetriaMes.upper(), pidNumber)
                        driver = rf.iniciaWebdriver(False)
                        rf.acessToIntegra(driver)

                    executaVolumetria = enviaParametros(volumetriaMes, count, extensao=extensao)
            else:
                print("\nINICIANDO WebDriver")
                if (driverIniciado == False):
                    driverIniciado = True 
                    driver = rf.iniciaWebdriver(False)
                    rf.createPID(volumetriaMes.upper(), pidNumber)
                    abreWebDriver = rf.acessToIntegra(driver)

                if (abreWebDriver):
                    executaVolumetria = enviaParametros(volumetriaMes, extensao=extensao)
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    driver.quit()
                    break
            
            if(executaVolumetria):
                if (file[0] != ""):
                    os.remove(infoLog)
                    fileExecuted = pathExecutados + "\\{}".format(file[0])
                    if (os.path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                        os.remove(fileExecuted)

                    shutil.move(file[0], pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                driver.quit()
                break
        
    if (driverIniciado == True):  
        driverIniciado = False
        rf.logoutIntegra(driver)

    time.sleep(3)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS\n'.format(hora))
    time.sleep(3)
#FIM DO WHILE