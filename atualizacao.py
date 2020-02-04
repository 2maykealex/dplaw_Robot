# coding=utf-8

import sys
import os
import time
import glob
import shutil
import robot_functions as rf

class Atualizacao (object):
    def fazerAtualizacao(self, dadosAtualizacao):
        rf.checkPopUps(self.driver)
        element = rf.waitinstance(self.driver, 'carregando', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

        #ASSUNTO
        try:
            comboAssunto = rf.waitinstance(self.driver, "//*[@id='slcAssunto']", 1, 'show')
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
                            elemCadastro = rf.waitinstance(self.driver, "//*[@id='slcAssunto']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                            elemCadastro.click()
                            self.driver.execute_script("document.getElementById('txtAssunto').value='{}' ".format(str(dadosAtualizacao['assunto'])))

        try:
            # comboAssunto.click()  # clica e abre as opções
            print("Preenchendo com assunto '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['assunto'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
        except:
            pass

        #DETALHES
        try:
            comboDetalhe = rf.waitinstance(self.driver, "//*[@id='slcDetalhes']", 1, 'show')
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
                            elemCadastro = rf.waitinstance(self.driver, "//*[@id='slcDetalhes']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                            elemCadastro.click()
                            self.driver.execute_script("document.getElementById('txtDetalhes').value='{}' ".format(str(dadosAtualizacao['detalhe'])))

        try:
            # comboDetalhe.click()  # clica e abre as opções
            print("Preenchendo com o detalhe '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['detalhe'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
        except:
            pass

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(self.driver, 'btnSalvar', 1, 'show', 'id')
        element.click()
        time.sleep(0.5)

        # # SALVAR ALTERAÇÃO - POP_UP
        try:
            element = rf.waitinstance(self.driver, 'popup_ok', 1, 'show', 'id')
            element.click() 
            
            message = "REGISTRO {}: A Pasta '{}' foi atualizada com o ASSUNTO: '{}' e DETALHE: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['assunto'], dadosAtualizacao['detalhe'])
            rf.createLog(self.logFile, message)   #poderia acontecer de salvar, e não aparecer (por neste momento falhar a conexão)
        except:
            pass

    def enviaParametros(self, atualizacaoPasta, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = rf.abreArquivo(atualizacaoPasta, extensao, path=path)
            count = dfExcel.number_of_rows()-1

            while (item <= count):         #looping dentro de cada arquivo
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
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
                        search, element = rf.pesquisarPasta(self.driver, pasta)
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
                        self.fazerAtualizacao(dadosAtualizacao)
                    except:
                        return False
                else:
                    print("--- ARQUIVO {}.XLSX\n".format(atualizacaoPasta))
                    log  =  "REGISTRO {}: ========= A pasta '{}' NÃO EXISTE NO PROMAD!!! =========".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'])
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
        executaAtualizacao = None

        login, password = "robo@dplaw.com.br" ,"dplaw00612"

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        atualizacaoPasta = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(atualizacaoPasta)
        
        abreWebDriver = None
        if (os.path.isfile(self.logFile)):
            linha, count = rf.checkEndFile(self.logFile)

            if (linha == "FIM"): #ultima linha do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(atualizacaoPasta))
                executaAtualizacao = True

            else:  # continua o preenchimento do log já existente 
                if (driverIniciado == False):
                    driverIniciado = True 
                    print("\nINICIANDO WebDriver")
                    rf.createPID(atualizacaoPasta.upper(), pidNumber)
                    self.driver = rf.iniciaWebdriver(False)
                    abreWebDriver = rf.acessToIntegra(self.driver, login, password)
                if (abreWebDriver):
                    executaAtualizacao = self.enviaParametros(atualizacaoPasta, count, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro - força o fechamento do Webdriver
                    self.driver.quit()
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True 
                self.driver = rf.iniciaWebdriver(False)
                rf.createPID(atualizacaoPasta.upper(), pidNumber)
                abreWebDriver =  rf.acessToIntegra(self.driver, login, password)
            if (abreWebDriver):
                executaAtualizacao = self.enviaParametros(atualizacaoPasta, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.driver.quit()
                # break

        if (executaAtualizacao):
            if (file[0] != ""):
                os.remove("{}\\{}".format(path, infoLog))
                # fileExecuted = pathExecutados + "\\{}".format(file[0])
                fileExecuted = pathExecutados + "\\{}.{}".format(atualizacaoPasta, extensao)
                if (os.path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    os.remove(fileExecuted)
                shutil.move("{}\\{}.{}".format(path, atualizacaoPasta, extensao), pathExecutados)
                # shutil.move(file[0], pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
        else:
            driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
            try:
                self.driver.quit()
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            rf.logoutIntegra(self.driver)