# coding=utf-8

import sys
import os
import time
import glob
import shutil
import robot_functions as rf

def fazerAtualizacao(dadosAtualizacao):

    rf.checkPopUps(driver)

    element = rf.waitinstance(driver, 'carregando', 1, 'show', 'id')
    if (element.value_of_css_property('display') == 'block'):
        driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

    #ASSUNTO
    try:
        comboAssunto = rf.waitinstance(driver, "//*[@id='slcAssunto']", 1, 'show')
        select = rf.Select(comboAssunto)
        select.select_by_visible_text(str(dadosAtualizacao['assunto']))
    except:
        try:
            select.select_by_visible_text(dadosAtualizacao['assunto'])
        except:
            try:
                select.select_by_visible_text(dadosAtualizacao['assunto'].title())
            except:
                try:
                    select.select_by_visible_text(dadosAtualizacao['assunto'].lower())
                except:
                    try:
                        select.select_by_visible_text(dadosAtualizacao['assunto'].lower().capitalize())   #usado sem Tratamento para cair except externo
                    except:
                        comboAssunto.click()
                        elemCadastro = rf.waitinstance(driver, "//*[@id='slcAssunto']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                        elemCadastro.click()
                        driver.execute_script("document.getElementById('txtAssunto').value='{}' ".format(str(dadosAtualizacao['assunto'])))

    try:
        # comboAssunto.click()  # clica e abre as opções
        print("Preenchendo com assunto '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['assunto'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
    except:
        pass

    #DETALHES
    try:
        comboDetalhe = rf.waitinstance(driver, "//*[@id='slcDetalhes']", 1, 'show')
        select = rf.Select(comboDetalhe)
        select.select_by_visible_text(str(dadosAtualizacao['detalhe']))
    except:
        try:
            select.select_by_visible_text(dadosAtualizacao['detalhe'])
        except:
            try:
                select.select_by_visible_text(dadosAtualizacao['detalhe'].title())
            except:
                try:
                    select.select_by_visible_text(dadosAtualizacao['detalhe'].lower())
                except:
                    try:
                        select.select_by_visible_text(dadosAtualizacao['detalhe'].lower().capitalize())   #usado sem Tratamento para cair except externo
                    except:
                        comboDetalhe.click()
                        elemCadastro = rf.waitinstance(driver, "//*[@id='slcDetalhes']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                        elemCadastro.click()
                        driver.execute_script("document.getElementById('txtDetalhes').value='{}' ".format(str(dadosAtualizacao['detalhe'])))

    try:
        # comboDetalhe.click()  # clica e abre as opções
        print("Preenchendo com o detalhe '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['detalhe'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
    except:
        pass


    # SALVAR ALTERAÇÃO
    time.sleep(2)
    element = rf.waitinstance(driver, 'btnSalvar', 1, 'show', 'id')
    element.click()
    time.sleep(0.5)

    # # SALVAR ALTERAÇÃO - POP_UP
    try:
        element = rf.waitinstance(driver, 'popup_ok', 1, 'show', 'id')
        element.click() 
        
        message = "REGISTRO {}: Salvando alterações na pasta {} - ASSUNTO: {} - DETALHE: {}".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['assunto'], dadosAtualizacao['detalhe'])
        rf.createLog(logFile, message)   #poderia acontecer de salvar, e não aparecer (por neste momento falhar a conexão)
    except:
        pass

def enviaParametros(atualizacaoPasta, item = 1, extensao="xlsx"):
    try:
        print('\n')
        dfExcel = rf.abreArquivo(atualizacaoPasta, extensao)
        count = dfExcel.number_of_rows()-1

        while (item <= count):         #looping dentro de cada arquivo
            pasta   = dfExcel[item, 0]
            assunto = dfExcel[item, 1]
            detalhe = dfExcel[item, 2]

            dadosAtualizacao = {}
            dadosAtualizacao['atualizacaoPasta']  = atualizacaoPasta
            dadosAtualizacao['item']     = item
            dadosAtualizacao['pasta']    = pasta
            dadosAtualizacao['assunto']  = assunto
            dadosAtualizacao['detalhe']  = detalhe

            trySearch = 1
            search = False
            while (trySearch < 4):
                hora = time.strftime("%H:%M:%S")
                print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                try:
                    search = rf.pesquisarPasta(pasta)
                except:
                    return False

                if (search == True):
                    break
                trySearch = trySearch + 1
            print('\n')

            if (search == True):
                try:
                    fazerAtualizacao(dadosAtualizacao)
                except:
                    return False
            else:
                print("--- ARQUIVO {}.XLSX\n".format(atualizacaoPasta))
                log  =  "REGISTRO {}: ========= A pasta {} NÃO EXISTE NO PROMAD!!! =========".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'])
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

path = os.getcwd() + "\\files\\atualizacao" # obtem o caminho do script e add a pasta atualizacao
logsPath = os.getcwd() + "\\files\\atualizacao\\logs"

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

login, password = "robo@dplaw.com.br" ,"dplaw00612"

print("\n-----------------------------------------")
print("Login utilizado: {}".format(login))
print("-----------------------------------------\n")


while True:
    files = []
    for file in glob.glob("*.xls*"):
        files.append(file)
        
    if (files):

        for file in files:
            file = file.split('.')
            atualizacaoPasta = '.'.join(file[:-1])#file[0]
            extensao = file[-1]
            
            if (file != ""):
                infoLog = "EXECUTANDO {}.txt".format(file[0].upper())
                arquivo = open(infoLog, 'w+')
                arquivo.close() 
            
            logFile = logsPath + "\\_log_{}.txt".format(atualizacaoPasta)
            
            abreWebDriver = None
            executaAtualizacao = None
            if (os.path.isfile(logFile)):
                linha, count = rf.checkEndFile(logFile)
                              
                if (linha == "FIM"): #ultima linha do arquivo
                    print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(atualizacaoPasta))
                    
                else:                          # continua o preenchimento do log já existente 
                    if (driverIniciado == False):
                        driverIniciado = True 
                        print("\nINICIANDO WebDriver")
                        rf.createPID(atualizacaoPasta.upper(), pidNumber)
                        driver = rf.iniciaWebdriver(False)
                        rf.acessToIntegra(driver, login, password)

                    executaAtualizacao = enviaParametros(atualizacaoPasta, count, extensao=extensao)
            else:
                print("\nINICIANDO WebDriver")
                if (driverIniciado == False):
                    driverIniciado = True 
                    driver = rf.iniciaWebdriver(False)
                    rf.createPID(atualizacaoPasta.upper(), pidNumber)
                    abreWebDriver =  rf.acessToIntegra(driver, login, password)

                if (abreWebDriver):
                    executaAtualizacao = enviaParametros(atualizacaoPasta, )
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    driver.quit()
                    break
            
            if(executaAtualizacao):
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