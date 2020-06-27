# coding=utf-8
from time import strftime
from time import sleep
from os import mkdir
from os import remove
from os import path as pathFolder
from os import getpid
from shutil import move
from integra_functions import IntegraFunctions
import basic_functions #uso completo nesse módulo

class Contrato (object):

    def __init__(self):
        self.integra = IntegraFunctions()

    def inserirContrato(self, contratoMes, pasta, registro):
        self.integra.checkPopUps()

        element = self.integra.waitingElement('txtCampoLivre4', 'id')
        if (element.get_attribute('value') ==  ''):
            # element.clear()
            print("Preenchendo com '{}' na pasta/processo '{}' - ARQUIVO {}.XLSX\n".format(contratoMes, pasta, contratoMes))
            sleep(2)

            self.integra.driver.execute_script("document.getElementById('txtCampoLivre4').value='{}' ".format(contratoMes) )
            sleep(2)

            # checando se o elemento CNJ está preenchido
            element = self.integra.waitingElement('txtNroCnj', 'id')
            if (element.get_attribute("value") != ''):
                # Segredo de Justiça  #por padrão, será marcado não
                element = self.integra.waitingElement('segredoJusticaN', 'id')
                self.integra.driver.execute_script("arguments[0].click();", element)
                sleep(2)

                element = self.integra.waitingElement('capturarAndamentosS', 'id')
                self.integra.driver.execute_script("arguments[0].click();", element)
                sleep(2)

            # SALVAR ALTERAÇÃO
            sleep(2)
            element = self.integra.waitingElement('btnSalvar', 'id')
            element.click()
            sleep(2)

            # SALVAR ALTERAÇÃO - popup
            try:
                element = self.integra.waitingElement('popup_ok', 1, 'click', 'id')
                element.click()
            except:
                pass

            basic_functions.createLog(self.logFile, "REG {}: '{}' foi preenchido na pasta/processo '{}'\n".format(registro, contratoMes.upper(), pasta))
            sleep(1)
            return True

        else:
            print("--- ARQUIVO {}.XLSX\n".format(contratoMes))
            log = "REG {}: ****** O contrato para a pasta/processo '{}' já foi preenchido! ******\n".format(registro, pasta)
            basic_functions.createLog(self.logFile, log)
            sleep(1)
            return False

    def enviaParametros(self, contratoMes, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = basic_functions.abreArquivo(contratoMes, extensao, path=path)
            count = dfExcel.number_of_rows()-1

            while (item <= count):         #looping dentro de cada arquivo
                pasta =  dfExcel[item, 0]
                trySearch = 1
                search = False
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
                while (trySearch < 4):
                    hora = strftime("%H:%M:%S")
                    print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                    try:
                        countChar = len(str(pasta))
                        if (countChar >= 14):
                            search, element = self.integra.pesquisarCliente(pasta, 'processo')  #pesquisa por processo
                        else:
                            search, element = self.integra.pesquisarCliente(pasta, 'pasta')  #pesquisa por pasta
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
                    log  =  "REG {}: ========= A pasta {} NÃO EXISTE NO PROMAD!!! =========\n".format(item, pasta)
                    basic_functions.createLog(self.logFile, log)

                item = item + 1

            basic_functions.createLog(self.logFile, '_________________________________________________________________\n')
            basic_functions.createLog(self.logFile, 'FIM')
            return True
        except:
            return False

    def controle(self, file, path):
        pidNumber = str(getpid())
        print(pidNumber)
        infoLog = "EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
        logsPath = path + "\\logs"
        pathExecutados = path + "\\arquivos_executados"

        if (pathFolder.exists(pathExecutados) == False):
            mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado -

        if (pathFolder.exists(logsPath) == False):
            mkdir(logsPath)   # Se o diretório \Volumetrias\files não existir, será criado -

        driverIniciado = False
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
        if (pathFolder.isfile(self.logFile)):
            registro = basic_functions.checkEndFile(self.logFile)

            if (registro == "FIM"): #ultimo registro do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(contratoMes))
                executaContrato = True

            else: # continua o preenchimento do log já existente
                registro = int(registro.split(":")[0][4:]) + 1     #obtém o valor do último registro lançado (+1) para dar continuidade
                if (driverIniciado == False):
                    driverIniciado = True
                    print("\nINICIANDO WebDriver")
                    basic_functions.createPID(contratoMes.upper(), pidNumber)
                    abreWebDriver = self.integra.acessToIntegra(login, password)
                if (abreWebDriver):
                    executaContrato = self.enviaParametros(contratoMes, registro, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    self.integra.driver.quit()
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True
                basic_functions.createPID(contratoMes.upper(), pidNumber)
                abreWebDriver = self.integra.acessToIntegra(login, password)
            if (abreWebDriver):
                executaContrato = self.enviaParametros(contratoMes, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.integra.driver.quit()
                remove("{}\\{}".format(path, infoLog))

        if (executaContrato):
            if (file[0] != ""):
                remove("{}\\{}".format(path, infoLog))
                fileExecuted = pathExecutados + "\\{}.{}".format(contratoMes, extensao)
                if (pathFolder.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    remove(fileExecuted)
                move("{}\\{}.{}".format(path, contratoMes, extensao), pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
        else:
            driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
            try:
                self.integra.driver.quit()
                remove("{}\\{}".format(path, infoLog))
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            self.integra.logoutIntegra()

        return True