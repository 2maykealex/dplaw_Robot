# coding=utf-8
import sys
import os
import time
import glob
import shutil
import robot_functions as rf

class Contrato (object):





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
            linha, count = rf.checkEndFile(self.logFile)

            if (linha == "FIM"): #ultima linha do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(contratoMes))

            else: # continua o preenchimento do log já existente 
                if (driverIniciado == False):
                    driverIniciado = True 
                    print("\nINICIANDO WebDriver")
                    rf.createPID(contratoMes.upper(), pidNumber)
                    self.driver = rf.iniciaWebdriver(False)
                    abreWebDriver = rf.acessToIntegra(self.driver, login, password)

                executaContrato = self.enviaParametros(contratoMes, count, extensao=extensao, path=path)
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
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            rf.logoutIntegra(self.driver)

        return True