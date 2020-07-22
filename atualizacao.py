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
        self.isTest = basic_functions.checkIfTest()

    def fazerAtualizacao(self, dadosAtualizacao):
        self.integra.checkPopUps()
        sleep(4)
        # LOCALIZADOR

        element = self.integra.waitingElement('divParteAdversaVersos', 'click', form='id')
        element = element.text.split('\n')[1] ## OBTEM DADOS DO CLIENTE

        if (element ==  'Oi S.A (1644)'):
            element = self.integra.waitingElement('slcLocalizador', 'click', 'id')
            select = self.integra.selenium.select(element)
            primeiroItemSelecionado = select.first_selected_option.get_attribute("innerHTML")

            if (str(dadosAtualizacao['localizador'])):
                if (primeiroItemSelecionado == 'Selecione...'):  # SÓ PREENCHE SE NÃO TER ITEM SELECIONADO
                    try:
                        # element = self.integra.waitingElement('slcLocalizador', 'click', 'id')
                        select = self.integra.selenium.select(element)
                        select.select_by_visible_text(str(dadosAtualizacao['localizador']))
                        message = "\nREG {}: A Pasta '{}' foi atualizada com o LOCALIZADOR: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['localizador'])
                    except:
                        message = "\nREG {}: ERRO AO ATUALIZAR A PASTA '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'])
                else:
                    message = "\nREG {}: A Pasta '{}' é da OI S.A e já foi atualizada com o LOCALIZADOR: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['localizador'])
            else:
                message = "\nREG {}: ERRO AO ATUALIZAR A PASTA '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'])

            basic_functions.createLog(self.logFile, message)   #poderia acontecer de salvar, e não aparecer (por neste momento falhar a conexão)

        else:
            if (str(dadosAtualizacao['localizador'])):
                try:
                    element = self.integra.waitingElement('slcLocalizador', 'click', 'id')
                    select = self.integra.selenium.select(element)
                    select.select_by_visible_text('Selecione...')
                    # select.select_by_visible_text(str(dadosAtualizacao['localizador']))
                except:
                    pass



            # #ASSUNTO
            # try:
            #     comboAssunto = self.integra.waitingElement("//*[@id='slcAssunto']")
            #     select = self.integra.selenium.select(comboAssunto)
            #     if (select.first_selected_option.get_attribute("innerHTML")):
            #         if (select.first_selected_option.get_attribute("innerHTML") == str(dadosAtualizacao['assunto'])):
            #             isEmpty = False # se for igual, marca FALSE para não selecionar novamente.
            #         else:
            #             isEmpty = True # se não for igual, marca TRUE para selecionar o correto
            #     else:
            #         isEmpty = True
            # except:
            #     pass

            # if (isEmpty):
            #     try:
            #         select.select_by_visible_text(str(dadosAtualizacao['assunto']))
            #     except:
            #         try:
            #             select.select_by_visible_text(dadosAtualizacao['assunto'])
            #         except:
            #             try:
            #                 select.select_by_visible_text(dadosAtualizacao['assunto'].title())
            #             except:
            #                 try:
            #                     select.select_by_visible_text(dadosAtualizacao['assunto'].lower())
            #                 except:
            #                     try:
            #                         select.select_by_visible_text(dadosAtualizacao['assunto'].lower().capitalize())   #usado sem Tratamento para cair except externo
            #                     except:
            #                         comboAssunto.click()
            #                         elemCadastro = self.integra.waitingElement("//*[@id='slcAssunto']/option[2]") # CADASTRAR NOVO ITEM
            #                         elemCadastro.click()
            #                         self.integra.driver.execute_script("document.getElementById('txtAssunto').value='{}' ".format(str(dadosAtualizacao['assunto'])))
            #     try:
            #         print("Preenchendo com assunto '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['assunto'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
            #     except:
            #         pass

            # #DETALHES
            # try:
            #     comboDetalhe = self.integra.waitingElement("//*[@id='slcDetalhes']")
            #     select = self.integra.selenium.select(comboDetalhe)
            #     if (select.first_selected_option.get_attribute("innerHTML")):
            #         if (select.first_selected_option.get_attribute("innerHTML") == str(dadosAtualizacao['detalhe'])):
            #             isEmpty = False # se for igual, marca FALSE para não selecionar novamente.
            #         else:
            #             isEmpty = True # se não for igual, marca TRUE para selecionar o correto
            #     else:
            #         isEmpty = True
            # except:
            #     pass

            # if (isEmpty):
            #     try:
            #         select.select_by_visible_text(str(dadosAtualizacao['detalhe']))
            #     except:
            #         try:
            #             select.select_by_visible_text(dadosAtualizacao['detalhe'])
            #         except:
            #             try:
            #                 select.select_by_visible_text(dadosAtualizacao['detalhe'].title())
            #             except:
            #                 try:
            #                     select.select_by_visible_text(dadosAtualizacao['detalhe'].lower())
            #                 except:
            #                     try:
            #                         select.select_by_visible_text(dadosAtualizacao['detalhe'].lower().capitalize())   #usado sem Tratamento para cair except externo
            #                     except:
            #                         comboDetalhe.click()
            #                         elemCadastro = self.integra.waitingElement("//*[@id='slcDetalhes']/option[2]") # CADASTRAR NOVO ITEM
            #                         elemCadastro.click()
            #                         self.integra.driver.execute_script("document.getElementById('txtDetalhes').value='{}' ".format(str(dadosAtualizacao['detalhe'])))
            #     try:
            #         print("Preenchendo com o detalhe '{}' na pasta '{}' - ARQUIVO {}.XLSX\n".format(dadosAtualizacao['detalhe'], dadosAtualizacao['pasta'], dadosAtualizacao['atualizacaoPasta']))
            #     except:
            #         pass

            # SALVAR ALTERAÇÃO
            sleep(2)
            element = self.integra.waitingElement('btnSalvar', form='id')
            element.click()
            sleep(6)

            # # SALVAR ALTERAÇÃO - POP_UP
            try:
                element = self.integra.waitingElement('popup_ok', form='id')
                element.click()
                sleep(2)

                message = "\nREG {}: A Pasta '{}' NÃO É DA OI S.A - e foi atualizada com o LOCALIZADOR: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['localizador'])
                # message = "REG {}: A Pasta '{}' foi atualizada com o ASSUNTO: '{}' e DETALHE: '{}'".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'], dadosAtualizacao['assunto'], dadosAtualizacao['detalhe'])
                basic_functions.createLog(self.logFile, message)   #poderia acontecer de salvar, e não aparecer (por neste momento falhar a conexão)
            except:
                pass

    def enviaParametros(self, atualizacaoPasta, item = 1, extensao="xlsx", path=""):
        try:
            print('\n')
            dfExcel = basic_functions.abreArquivo(atualizacaoPasta, extensao, path=path)
            count = dfExcel.number_of_rows()-1

            while (item <= count):         #looping dentro de cada arquivo
                print('\n===================================================')
                print("ARQUIVO {}.XLSX".format(atualizacaoPasta))
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
                dadosAtualizacao = {}
                dadosAtualizacao['atualizacaoPasta']  = atualizacaoPasta
                dadosAtualizacao['item']     = item

                if (dfExcel[item, 0]):
                    dadosAtualizacao['pasta']    = dfExcel[item, 0]
                if (dfExcel[item, 1]):
                    dadosAtualizacao['assunto']  = dfExcel[item, 1]
                if (dfExcel[item, 2]):
                    dadosAtualizacao['detalhe']  = dfExcel[item, 2]
                if (dfExcel[item, 3]):
                    dadosAtualizacao['localizador']  = dfExcel[item, 3]

                trySearch = 1
                search = False
                while (trySearch < 4):
                    hora = strftime("%H:%M:%S")
                    # print('{} - {}ª tentativa de busca... pasta {}'.format(hora, trySearch, dadosAtualizacao['pasta']))

                    try:
                        search, element = self.integra.pesquisarCliente(dadosAtualizacao['pasta'], 'pasta')
                    except:
                        return False

                    if (search == True):
                        try:
                            element.click()  # clica na pasta para inserir a atualização
                        except:
                            search = False
                        break
                    trySearch = trySearch + 1
                if (search == True):
                    try:
                        self.fazerAtualizacao(dadosAtualizacao)
                    except:
                        return False
                else:
                    log  =  "\nREG {}: ========= A pasta '{}' NÃO EXISTE NO PROMAD!!! =========".format(dadosAtualizacao['item'], dadosAtualizacao['pasta'])
                    print(log)
                    basic_functions.createLog(self.logFile, log)

                item = item + 1

            basic_functions.createLog(self.logFile, '\nFIM')
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
        executaAtualizacao = None

        # login, password = "robo@dplaw.com.br" ,"dplaw00612"

        login="cgst@dplaw.com.br"
        password="gestao0"

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        atualizacaoPasta = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(atualizacaoPasta)

        abreWebDriver = None
        if (pathFolder.isfile(self.logFile)):
            registro = basic_functions.checkEndFile(self.logFile)

            if (registro == "FIM"): #ultima registro do arquivo
                print('O arquivo {}.xlsx já foi executado! Indo à próxima instrução!'.format(atualizacaoPasta))
                executaAtualizacao = True

            else:  # continua o preenchimento do log já existente
                registro = int(registro.split(":")[0][4:]) + 1     #obtém o valor do último registro lançado (+1) para dar continuidade
                if (driverIniciado == False):
                    driverIniciado = True
                    print("\nINICIANDO WebDriver")
                    basic_functions.createPID(atualizacaoPasta.upper(), pidNumber)
                    abreWebDriver = self.integra.acessToIntegra(login, password)
                if (abreWebDriver):
                    executaAtualizacao = self.enviaParametros(atualizacaoPasta, registro, extensao=extensao, path=path)
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
                fileExecuted = pathExecutados + "\\{}.{}".format(atualizacaoPasta, extensao)
                if (pathFolder.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    remove(fileExecuted)
                if (not(self.isTest)):
                    move("{}\\{}.{}".format(path, atualizacaoPasta, extensao), pathExecutados)
                remove("{}\\{}".format(path, infoLog))
        else:
            driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
            try:
                self.integra.driver.quit()
            except:
                pass

        if (driverIniciado == True):
            driverIniciado = False
            self.integra.logoutIntegra()