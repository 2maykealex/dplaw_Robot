# coding=utf-8
import sys
import os
import time
import glob
import shutil
import robot_functions as rf

class Contrato (object):

    def inserirContrato(self, contratoMes, pasta, registro):
        rf.checkPopUps(self.driver)

        element = rf.waitinstance(self.driver, 'backgroundPopup', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#backgroundPopup').css('display', 'none');") # torna elemento visível

        element = rf.waitinstance(self.driver, 'carregando', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

        element = rf.waitinstance(self.driver, 'txtCampoLivre4', 1, 'show', 'id')
        if (element.get_attribute('value') ==  ''):
            print("Preenchendo com '{}' na pasta/processo '{}' - ARQUIVO {}.XLSX\n".format(contratoMes, pasta, contratoMes))
            time.sleep(2) 

            self.driver.execute_script("document.getElementById('txtCampoLivre4').value='{}' ".format(contratoMes) )
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
            element = rf.waitinstance(self.driver, 'btnSalvar', 1, 'show', 'id')
            element.click()

            rf.createLog(self.logFile, "REGISTRO {}: '{}' foi preenchido na pasta/processo '{}'\n".format(registro, contratoMes.upper(), pasta))
            time.sleep(1)
            return True

        else:
            print("--- ARQUIVO {}.XLSX\n".format(contratoMes))
            log = "REGISTRO {}: ****** O contrato para a pasta/processo '{}' já foi preenchido! ******\n".format(registro, pasta)
            rf.createLog(self.logFile, log)
            time.sleep(1)
            return False

    def enviaParametros(self, contratoMes, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = rf.abreArquivo(contratoMes, extensao, path=path)
            count = dfExcel.number_of_rows()-1

            while (item <= count):         #looping dentro de cada arquivo
                pasta =  dfExcel[item, 0]
                trySearch = 1
                search = False
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
                while (trySearch < 4):
                    hora = time.strftime("%H:%M:%S")
                    print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                    try:
                        countChar = len(str(pasta))
                        if (countChar >= 14):
                            search, element = rf.pesquisarProcesso(self.driver, pasta)  #pesquisa por processo
                        else:
                            search, element = rf.pesquisarPasta(self.driver, pasta)  #pesquisa por pasta
                    except:
                        return False

                    if (search == True):
                        try:
                            element.click()  # clica na pasta para inserir o contrato
                        except:
                            search = False
                        break
                    trySearch = trySearch + 1
                print('\n')

                if (search == True):
                    try:
                        self.inserirContrato(contratoMes, pasta, item)
                    except:
                        return False
                else:
                    print("--- ARQUIVO {}.XLSX\n".format(contratoMes))
                    log  =  "REGISTRO {}: ========= A pasta {} NÃO EXISTE NO PROMAD!!! =========".format(item, pasta)
                    rf.createLog(self.logFile, log)

                item = item + 1

            rf.createLog(self.logFile, '_________________________________________________________________')
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
        executaContrato = None

        login, password = "robo@dplaw.com.br" ,"dplaw00612"

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        contratoMes = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(contratoMes)
        
        abreWebDriver = None
        if (os.path.isfile(self.logFile)):
            registro = rf.checkEndFile(self.logFile)

            if (linha == "FIM"): #ultima linha do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(contratoMes))
                executaContrato = True

            else: # continua o preenchimento do log já existente 
                registro = int(registro.split(":")[0][4:]) + 1     #obtém o valor do último registro lançado (+1) para dar continuidade
                if (driverIniciado == False):
                    driverIniciado = True 
                    print("\nINICIANDO WebDriver")
                    rf.createPID(contratoMes.upper(), pidNumber)
                    self.driver = rf.iniciaWebdriver(False)
                    abreWebDriver = rf.acessToIntegra(self.driver, login, password)
                if (abreWebDriver):
                    executaContrato = self.enviaParametros(contratoMes, count, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    self.driver.quit()                
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True 
                self.driver = rf.iniciaWebdriver(False)
                rf.createPID(contratoMes.upper(), pidNumber)
                abreWebDriver = rf.acessToIntegra(self.driver, login, password)
            if (abreWebDriver):
                executaContrato = self.enviaParametros(contratoMes, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.driver.quit()
                os.remove("{}\\{}".format(path, infoLog))

        
        if (executaContrato):
            if (file[0] != ""):
                os.remove("{}\\{}".format(path, infoLog))
                fileExecuted = pathExecutados + "\\{}.{}".format(contratoMes, extensao)
                if (os.path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    os.remove(fileExecuted)
                shutil.move("{}\\{}.{}".format(path, contratoMes, extensao), pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
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