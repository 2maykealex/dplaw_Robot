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

class Atualizacao (object):

    def __init__(self):
        self.integra = IntegraFunctions()

    def fazerAtualizacao(self, dadosAtualizacao):
        self.integra.checkPopUps()
        element = self.integra.waitInstance(self.driver, 'carregando', 1, 'show', 'id')
        if (element.value_of_css_property('display') == 'block'):
            self.driver.execute_script("$('#carregando').css('display', 'none');") # torna elemento visível

        #ASSUNTO
        try:
            comboAssunto = self.integra.waitInstance(self.driver, "//*[@id='slcAssunto']", 1, 'show')
            select = self.integra.Select(comboAssunto)
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
                            elemCadastro = self.integra.waitInstance(self.driver, "//*[@id='slcAssunto']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                            elemCadastro.click()
                            self.driver.execute_script("document.getElementById('txtAssunto').value='{}' ".format(str(dadosAtualizacao['assunto'])))

        try:
            # comboAssunto.click()  # clica e abre as opções
            print("Preenchendo com assunto '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['assunto'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
        except:
            pass

        #DETALHES
        try:
            comboDetalhe = self.integra.waitInstance(self.driver, "//*[@id='slcDetalhes']", 1, 'show')
            select = self.integra.Select(comboDetalhe)
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
                            elemCadastro = self.integra.waitInstance(self.driver, "//*[@id='slcDetalhes']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                            elemCadastro.click()
                            self.driver.execute_script("document.getElementById('txtDetalhes').value='{}' ".format(str(dadosAtualizacao['detalhe'])))

        try:
            # comboDetalhe.click()  # clica e abre as opções
            print("Preenchendo com o detalhe '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['detalhe'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
        except:
            pass

        # SALVAR ALTERAÇÃO
        sleep(2)
        element = self.integra.waitInstance(self.driver, 'btnSalvar', 1, 'show', 'id')
        element.click()
        sleep(0.5)

        # # SALVAR ALTERAÇÃO - POP_UP
        try:
            element = self.integra.waitInstance(self.driver, 'popup_ok', 1, 'show', 'id')
            element.click()

            message = "REGISTRO {}: A Pasta '{}' foi atualizada com o ASSUNTO: '{}' e DETALHE: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['assunto'], dadosAtualizacao['detalhe'])
            self.integra.createLog(self.logFile, message)   #poderia acontecer de salvar, e não aparecer (por neste momento falhar a conexão)
        except:
            pass

    def enviaParametros(self, atualizacaoPasta, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = self.integra.abreArquivo(atualizacaoPasta, extensao, path=path)
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
                    hora = strftime("%H:%M:%S")
                    print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, pasta))

                    try:
                        search, element = self.integra.pesquisarCliente(pasta, 'pasta')
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
                    self.integra.createLog(self.logFile, log)

                item = item + 1

            self.integra.createLog(self.logFile, '_________________________________________________________________')
            self.integra.createLog(self.logFile, 'FIM')
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
        if (path.isfile(self.logFile)):
            linha, count = basic_functions.checkEndFile(self.logFile)

            if (linha == "FIM"): #ultima linha do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(atualizacaoPasta))
                executaAtualizacao = True

            else:  # continua o preenchimento do log já existente
                if (driverIniciado == False):
                    driverIniciado = True
                    print("\nINICIANDO WebDriver")
                    basic_functions.createPID(atualizacaoPasta.upper(), pidNumber)
                    abreWebDriver = self.integra.acessToIntegra(login, password)
                if (abreWebDriver):
                    executaAtualizacao = self.enviaParametros(atualizacaoPasta, count, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro - força o fechamento do Webdriver
                    self.integra.driver.quit()
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True
                basic_functions.createPID(atualizacaoPasta.upper(), pidNumber)
                abreWebDriver =  self.integra.acessToIntegra(login, password)
            if (abreWebDriver):
                executaAtualizacao = self.enviaParametros(atualizacaoPasta, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.integra.driver.quit()
                # break

        if (executaAtualizacao):
            if (file[0] != ""):
                remove("{}\\{}".format(path, infoLog))
                # fileExecuted = pathExecutados + "\\{}".format(file[0])
                fileExecuted = pathExecutados + "\\{}.{}".format(atualizacaoPasta, extensao)
                if (path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    remove(fileExecuted)
                move("{}\\{}.{}".format(path, atualizacaoPasta, extensao), pathExecutados)
        else:
            driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
            try:
                self.integra.driver.quit()
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            self.integra.logoutIntegra()