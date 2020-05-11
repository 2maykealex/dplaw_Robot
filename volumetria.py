# coding=utf-8

import sys
import os
import time
import glob
import shutil
import robot_functions as rf

class Volumetria (object):
    def inserirVolumetria(self, volumetriaMes, pasta, registro):
        rf.checkPopUps(self.driver)

        element = rf.waitinstance(self.driver, 'backgroundPopup', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#backgroundPopup').css('display', 'none');") # torna elemento visível

        element = rf.waitinstance(self.driver, 'carregando', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

        element = rf.waitinstance(self.driver, 'txtCampoLivre3', 1, 'show', 'id')
        print(element.text)
        print(element.get_attribute('value'))
        if (element.get_attribute('value') ==  ''):
            print("Preenchendo com '{}' na pasta {} - ARQUIVO {}.XLSX\n".format(volumetriaMes, pasta, volumetriaMes))
            time.sleep(2) 

            self.driver.execute_script("document.getElementById('txtCampoLivre3').value='{}' ".format(volumetriaMes) )
            time.sleep(2)

            # checando se o elemento CNJ está preenchido
            element = rf.waitinstance(self.driver, 'txtNroCnj', 1, 'show', 'id')
            if (element.get_attribute("value") != ''):
                # Segredo de Justiça  #por padrão, será marcado não
                element = rf.waitinstance(self.driver, 'segredoJusticaN', 1, 'show', 'id')
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(2)

                element = rf.waitinstance(self.driver, 'capturarAndamentosS', 1, 'show', 'id')
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(2) 

            # SALVAR ALTERAÇÃO
            time.sleep(2)
            element = rf.waitinstance(self.driver, 'btnSalvar', 1, 'click', 'id')
            element.click()

            # SALVAR ALTERAÇÃO - popup
            time.sleep(2)
            element = rf.waitinstance(self.driver, 'popup_ok', 1, 'click', 'id')
            element.click()

            rf.createLog(self.logFile, "REG {}: O dado '{}' foi preenchido na pasta '{}'\n".format(registro, volumetriaMes, pasta))
            time.sleep(1)
            return True

        else:
            print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
            log = "REG {}: ****** A volumetria para a pasta '{}' já foi preenchida! ******\n".format(registro, pasta)
            rf.createLog(self.logFile, log)
            time.sleep(1)
            return False

    def enviaParametros(self, volumetriaMes, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = rf.abreArquivo(volumetriaMes, extensao, path=path)
            count = dfExcel.number_of_rows()-1

            while (item <= count):         #looping dentro de cada arquivo
                pasta =  dfExcel[item, 7]
                trySearch = 1
                search = False
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
                while (trySearch < 2):
                    hora = time.strftime("%H:%M:%S")
                    print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                    try:
                        search, element = rf.pesquisarCliente(self.driver, pasta, 'pasta')
                    except:
                        return False

                    if (search == True):
                        try:
                            element.click()  # clica na pasta para inserir a volumetria
                        except:
                            search = False
                        break
                    trySearch = trySearch + 1
                print('\n')

                if (search == True):
                    try:
                        self.inserirVolumetria(volumetriaMes, pasta, item)
                    except:
                        return False
                else:
                    print("--- ARQUIVO {}.XLSX\n".format(volumetriaMes))
                    log  =  "REG {}: ========= A pasta '{}' NÃO EXISTE NO PROMAD!!! =========\n".format(item, pasta)
                    rf.createLog(self.logFile, log)
                    # print("Não encontrado")
                    # return False

                item = item + 1

            rf.createLog(self.logFile, '_________________________________________________________________\n')
            rf.createLog(self.logFile, 'FIM')
            return True
        except:
            return False

    def controle(self, file, path):
        pidNumber = str(os.getpid())
        print(pidNumber)
        infoLog = "EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
        logsPath = path + "\\logs"
        pathExecutados = path + "\\arquivos_executados"

        if (os.path.exists(pathExecutados) == False):
            os.mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado - 

        if (os.path.exists(logsPath) == False):
            os.mkdir(logsPath)   # Se o diretório \Volumetrias\files não existir, será criado - 

        driverIniciado = False
        self.driver = None
        executaVolumetria = None

        login, password = "robo@dplaw.com.br" ,"dplaw00612"

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        volumetriaMes = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(volumetriaMes)
        
        abreWebDriver = None
        if (os.path.isfile(self.logFile)):
            registro = rf.checkEndFile(self.logFile)

            if (registro == "FIM"): #ultima registro do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(volumetriaMes))
                executaVolumetria = True

            else: # continua o preenchimento do log já existente
                registro = int(registro.split(":")[0][4:]) + 1     #obtém o valor do último registro lançado para dar continuidade
                if (driverIniciado == False):
                    driverIniciado = True 
                    print("\nINICIANDO WebDriver")
                    rf.createPID(volumetriaMes.upper(), pidNumber)
                    self.driver = rf.iniciaWebdriver(False)
                    abreWebDriver = rf.acessToIntegra(self.driver, login, password)

                executaVolumetria = self.enviaParametros(volumetriaMes, registro, extensao=extensao, path=path)
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True 
                self.driver = rf.iniciaWebdriver(False)
                rf.createPID(volumetriaMes.upper(), pidNumber)
                abreWebDriver = rf.acessToIntegra(self.driver, login, password)
            if (abreWebDriver):
                executaVolumetria = self.enviaParametros(volumetriaMes, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.driver.quit()
                os.remove("{}\\{}".format(path, infoLog))

        
        if (executaVolumetria):
            if (file[0] != ""):
                os.remove("{}\\{}".format(path, infoLog))
                fileExecuted = pathExecutados + "\\{}.{}".format(volumetriaMes, extensao)
                if (os.path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    os.remove(fileExecuted)
                shutil.move("{}\\{}.{}".format(path, volumetriaMes, extensao), pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
        else:
            driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver

            try:
                self.driver.quit()
                os.remove("{}\\{}".format(path, infoLog))
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            rf.logoutIntegra(self.driver)

        return True