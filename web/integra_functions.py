from selenium_functions import SeleniumFunctions
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import sleep
import basic_functions

# from datetime import date
# from datetime import datetime
# from datetime import timedelta
# from time import strftime
# from time import sleep
from os import mkdir
from os import remove
from os import path as pathFolder
from os import getcwd as osGetCWD
from os import getpid

from pprint import pprint
class IntegraFunctions(object):

    def __init__(self):
        self.selenium = SeleniumFunctions()
        self.waitInstance = self.selenium.waitInstance
        self.driver = None

    def acessToIntegra(self, login, password):
        try:
            self.driver = self.selenium.iniciaWebdriver()
            self.driver.maximize_window()
            self.driver.get('https://integra.adv.br/login-integra.asp')
            self.driver.execute_script("document.getElementById('login_email').value='{}'".format(login))
            self.driver.execute_script("document.getElementById('login_senha').value='{}'".format(password))
            sleep(1.5)
            self.driver.find_element_by_tag_name('button').click()
            sleep(1.5)
            self.checkPopUps()
            return True
        except:
            return False

    def acessaMenuPesquisa(self):
        #menu CLIENTES
        sleep(3)
        try:
            element = self.waitingElement('//*[@id="header"]/ul/li[1]', 'click', form='xpath')
            element.click()
        except:
            print("ERRO AO CLICAR NO MENU CLIENTES")
            return False

        #submenu PESQUISAR CLIENTE
        sleep(3)
        try:
            element = self.waitingElement('//*[@id="header"]/ul/li[1]/ul/lii[1]/p', 'click', form='xpath')
            element.click()
        except:
            print("ERRO AO CLICAR NO SUBMENU PESQUISAR CLIENTES")
            return False
        return True

    def pesquisarCliente(self, search, tipoPesquisa):
        sleep(4)
        try:
            self.driver.get('https://integra.adv.br/integra4/modulo/21/default.asp')
            abriuPesquisa = True
        except:
            abriuPesquisa = self.acessaMenuPesquisa()

        if (abriuPesquisa):
            sleep(2)
            self.checkPopUps()
            xPathOption = ''

            #tipo de pesquisa (opções)
            if (tipoPesquisa == 'pasta'):
                xPathOption = '//*[@id="chkPesquisa139"]'
                xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[6]'
            elif (tipoPesquisa == 'cliente'):
                xPathOption = '//*[@id="chkPesquisa133"]'
                xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[4]'
            elif (tipoPesquisa == 'processo'):
                xPathOption = '//*[@id="chkPesquisa137"]'
                xPathClick = '//*[@id="divCliente"]/div[3]/table/tbody/tr/td[6]'

            element = self.waitingElement('{}'.format(xPathOption))
            element.click()
            sleep(2)

            # valor do parâmetro
            self.driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(search))
            sleep(2)
            print("pesquisando pasta {}".format(search))
            #botão pesquisar
            self.driver.find_element_by_id("btnPesquisar").click()
            sleep(4)

            try:
                #Checa se não existe registros para essa pasta
                element = self.driver.find_element_by_id('loopVazio').is_displayed()
                hora = strftime("%H:%M:%S")
                print('{} - Não encontrou a pasta'.format(hora))
                retorno = False

            except:
                # SELECIONA O CLIENTE PESQUISADO        -  clica no primeiro item encontrado(não poderia ter duas pastas com o mesmo número)
                try:
                    element = self.waitingElement("{}/div".format(xPathClick))
                except:
                    try:
                        element = self.waitingElement("{}/div".format(xPathClick))
                    except:
                        pass
                        # element = self.waitingElement('//*[@id="divCliente"]/div[3]/table/tbody/tr')  #clica no registro -> abre a pasta
                retorno = True

        else:
            retorno = False
            element = ''

        return retorno, element

    def uploadFile(self):
        self.checkPopUps()
        # ACESSAR ÁREA DE DOWNLOADS
        self.driver.execute_script("clickMenuCadastro(108,'processoDocumento.asp');")

        # TODO FAZER LOOPING PARA ADD TODOS OS ARQUIVOS PERTINENTES AO PROCESSO/CLIENTE
        sleep(6)
        path = 'C:/Users/DPLAW-BACKUP/Desktop/dprobot/dpRobot/dplaw_Robot/pdf.pdf' # CAMINHO DO ARQUIVO
        # TODO MONTAR CAMINHO DINAMICAMENTE # self.driver.send_keys(os.getcwd() + "/tests/sample_files/Figure1.tif")

        # self.driver.switch_to.frame(1)
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe")) #ACESSANDO CONTEUDO DE UM FRAME

        element = self.driver.find_element_by_xpath('//*[@id="realupload"]')
        element.send_keys(path)

        self.driver.switch_to.default_content()   #VOLTAR PARA O CONTEUDO PRINCIPAL

        #Botão salvar
        sleep(6)
        element = self.waitingElement('//*[@id="btnSalvar"]', 1, 'show')
        element.click()
        # POP UP (OK)
        sleep(1.5)
        element = self.waitingElement('//*[@id="popup_ok"]', 1, 'show')
        element.click()

    def logoutIntegra(self):
        self.driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
        sleep(1.5)
        self.driver.quit()

    def checkPopUps(self):
        popupOk = False
        popUps = ['.popup_block',
                  '#menuvaimudar',
                  '#divFecharAvisoPopUp',
                  '#backgroundPopup',
                  '#carregando',
                  '#card'
                  ]
        for popUp in popUps:
            script = "$('{}').css('display', 'none');".format(popUp)
            try:
                self.driver.execute_script(script)
                popupOk = True
            except:
                pass

        if (popupOk == True):
            sleep(1.5)

    def waitingElement(self, elementName, tipo='click', form='xpath'):
        # tempo = datetime.now().second + 15
        while True:
            try:
                element = self.waitInstance(self.driver, elementName, 2, tipo, form)
                return element
            except:
                # if (datetime.now().second <= tempo):
                #     print('Tempo Esgotado!!! Saindo!')
                #     return False
                # else:
                #     print('teste  - não encontrado ainda!!!!')
                pass

    def controle(self, registros):
        robo = None
        abreWebDriver = None
        driverIniciado = False

        hoje = "%s" % (strftime("%Y-%m-%d"))
        hoje = hoje.replace('-', '_')
        hora = strftime("%H:%M:%S")
        hora = hora.replace(':', '_')

        # CRIANDO ARQUIVO DE LOG .CSV
        self.logBase = '{}\\logs\\{}'.format(pathFolder.dirname(__file__), registros['tipo'])
        self.logFileCSV = "{}\\_log_{}.csv".format(self.logBase, '{}_{}__{}__{}'.format(registros['tipo'], registros['sigla'], hoje, hora))
        basic_functions.createFolder(self.logBase) # CRIA DIRETÓRIO SE NÃO EXISTIR.

        login, password = basic_functions.checkLogin()
        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")
        print("\nINICIANDO WebDriver")
        abreWebDriver = self.acessToIntegra(login, password)

        if (registros['tipo'] == 'abertura'):
            print(registros['tipo'])
            robo = self.abrePasta(registros)
        # elif (registros['tipo'] == 'volumetria'):
        #     robo = self.Volumetria(registros)
        # elif (registros['tipo'] == 'contrato'):
        #     robo = self.Contrato(registros)
        # elif (registros['tipo'] == 'atualizacao'):
        #     robo = self.Atualizacao(registros)

    def abrePasta(self, registros):
        count =  len(registros) -1
        isTest = basic_functions.checkIfTest()

        try:
            searchClient, elemPesquisado = self.pesquisarCliente('Cliente teste', 'cliente')
        except:
            return False

        if (searchClient):
            elemPesquisado.click()
            sleep(.5)
            urlPage = self.driver.current_url
            for k, registro in registros.items():
                if (k in ['tipo', 'sigla']):
                    continue
                print('REG {}: INICIANDO'.format(str(int(k)+1)))
                registro['txtNroProcesso'] = basic_functions.ajustarNumProcessoCNJ(registro['txtNroProcesso'])
                registro['txtNroCnj']      = basic_functions.ajustarNumProcessoCNJ(registro['txtNroCnj'])
                try:
                    print('REG {}: REALIZANDO PESQUISA'.format(str(int(k)+1)))
                    if (not(isTest)): #se não é teste
                        searchFolder = False
                    else:
                        searchFolder, _element = self.pesquisarCliente(registro['txtPasta'], 'pasta')
                except:
                    print('REG {}: NÃO FOI POSSÍVEL REALIZAR UMA BUSCA -'.format(str(int(k)+1)))
                    return False

                if (int(k)== 0): # CABEÇALHO DO LOG
                    cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA;ID PROMAD;PARTE ADVERSA; ERRO: NÃO INSERIDOS; AGENDAMENTOS CRIADOS; AUDIÊNCIA; ERRO: AGENDAMENTOS NÃO CRIADOS;'
                    basic_functions.createLog(self.logFileCSV, "{}\n".format(cabeçalhoLog))

                if (not(searchFolder)):   # se não foi encontrado no sistema, será inserido
                    try:
                        sleep(0.5)
                        print('REG {}: REDIRECIONANDO À PG DO CLIENTE -'.format(str(int(k)+1)))
                        self.driver.get(urlPage)
                        sleep(0.5)
                        message = self.incluirProcesso(registro, int(k)+1) # k=item

                    except:
                        print('REG {}: ERRO AO INCLUIR A PASTA: {}'.format(str(int(k)+1), registro['txtPasta']))
                        #TODO ver log para esse erro
                else:
                    message = "REG {}; A PASTA {} JÁ EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(int(k)+1, registro['txtPasta'])

                basic_functions.createLog(self.logFileCSV, "{}\n".format(message))

    def incluirProcesso(self, registro, item):

        def selecionaResponsaveis():
            self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível
            comboResponsavel = self.waitingElement('//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button','click', form='xpath')
            comboResponsavel.click()  # clica e abre as opções
            sleep(.8)
            #recupera lista de RESPONSÁVEIS do PROMAD
            xInputs = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li'
            listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag
            # CARREGA LISTA DE RESPONSÁVEIS
            y = 1
            totalResp = len(registro[k])
            countResp = 0
            respSelecionados = []
            for item in listInputs:  #itera inputs recuperados, checa e clica
                if (item.text in registro[k]):
                    try:
                        xPathItem = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li[{}]'.format(y)
                        element = self.waitingElement(xPathItem, 'click', form='xpath')
                        element.click()
                        respSelecionados.append(item.text)
                    except:
                        naoInserido['{}-{}'.format(k, countResp + 1)] = item.text
                    sleep(0.8)
                    countResp = countResp + 1
                    if (countResp == totalResp):
                        break
                y = y + 1
            comboResponsavel.click()  # clica e Fecha as opções
            self.driver.execute_script("$('#slcResponsavel').css('display', 'none');") # torna elemento visível

        def segredoJusticaAndamentos():
            #Numero do CNJ
            if (registro['txtNroCnj']):      #VERIFICAR DEPOIS, DE INSERIR OS IDs NO OBJETO (REGISTROS)
                try:
                    # Segredo de Justiça  #por padrão, será marcado não
                    element = self.driver.find_element_by_id("segredoJusticaN")
                    self.driver.execute_script("arguments[0].click();", element)

                    sleep(0.3)
                    element = self.driver.find_element_by_id("capturarAndamentosS")
                    self.driver.execute_script("arguments[0].click();", element)
                except:
                    naoInserido['segredoCaptura'] = 'segredo-andamentos'

        def recuperaIdIntegra():
            #Obtém o ID do PROMAD da nova pasta a ser aberta
            try:
                element = self.waitingElement("idDoProcesso", 'show', 'class')
                idNovaPasta = element.get_attribute("innerHTML")
                idNovaPasta = idNovaPasta[14:].strip()
                print("REG {}: NOVA PASTA ABERTA: {}".format(item, idNovaPasta))
                return idNovaPasta
            except:
                naoInserido['idDoProcessoINTEGRA'] = 'Não recuperado'

        def checkValueInCombo(texto, element):
            try:
                select.select_by_visible_text(texto.title())
            except:
                try:
                    select.select_by_visible_text(texto.lower())
                except:
                    try:
                        select.select_by_visible_text(texto.lower().capitalize())
                    except:
                        pass
                        select.select_by_visible_text('--Cadastrar Novo Item--')
                        elemCadastro = self.waitingElement(element.replace('slc', 'txt'), 'click', form='id') # CADASTRAR NOVO ITEM
                        elemCadastro.clear()
                        elemCadastro.send_keys(str(texto).title())
            sleep(0.3)

        self.checkPopUps()
        sleep(1.5)
        print('REG {}: INICIANDO INCLUSAO DE PASTA'.format(item))
        element = self.waitInstance(self.driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
        element.click()
        naoInserido = {}

        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        message = ''
        message = "REG {};{} às {};".format(item, hoje, hora)  #Insere a primeira linha do item no log

        print('REG {}: INICIANDO LOOPING'.format(item))
        for k, v in registro.items():
            print ('REG {}: {} - {}'.format(item, k, v))
            try:
                if (k == 'slcResponsavel'):
                    selecionaResponsaveis()
                elif (k != 'razaoSocial' and k != 'adversa'):
                    element = self.waitingElement(k, 'click', form='id')
                    if (element.tag_name == 'input'):
                        element.clear()
                        element.send_keys(str(v))
                    elif (element.tag_name == 'select'):
                        try:
                            select = self.selenium.select(element)
                            select.select_by_visible_text(str(v))
                        except:
                            checkValueInCombo(str(v), k)
                    sleep(.8)
            except:
                naoInserido[k] = str(v)
        print('REG {}: FINALIZADO O LOOPING'.format(item))
        segredoJusticaAndamentos()
        idNovaPasta = recuperaIdIntegra()

        try:
            complementoAdversa = ""
            if (registro['adversa']):
                print('REG {}: EXISTE PARTE ADVERSA'.format(item))
                while True:
                    try:
                        element = self.waitingElement("//*[@id='div_menu17']", 'click', form='xpath')
                        element.click()
                        sleep(.8)
                        try:
                            element = self.driver.find_element_by_id('div_txtComarca').is_displayed()
                            self.driver.execute_script("verificarComboNovo('-1','txtComarca','slcComarca');")
                            naoInserido['comarcaNova'] = str(registro['comarcaNova'])
                            sleep(.8)
                            continue
                        except:
                            break
                    except:
                        pass

                self.checkPopUps()

                # Preenchendo Parte Adversa
                try:
                    element = self.waitingElement('//*[@id="txtNome"]', 'click', form='xpath')
                    element.send_keys(str(registro['adversa']))
                    print("REG {}: REGISTRADO A PARTE ADVERSA: {}".format(item, str(registro['adversa'])))
                    complementoAdversa = "{}".format(str(registro['adversa']))
                except:
                    naoInserido['adversa'] = str(registro['adversa'])
            else:
                naoInserido['adversa'] = ''
        except:
            print('REG {}: NÃO EXISTE PARTE ADVERSA'.format(item))
            pass

        sleep(0.8)

        complementoNaoInseridos =''
        if (naoInserido):
            complementoNaoInseridos = 'NÃO FORAM INSERIDOS OS ITENS: '
            for k1, v1 in naoInserido.items():
                complementoNaoInseridos = '{} {}: "{}" | '.format(complementoNaoInseridos, k1, v1)
                print(complementoNaoInseridos)

        try: # Botão salvar
            print('REG {}: ANTES DE SALVAR'.format(item))
            element = self.waitingElement('//*[@id="btnSalvar"]', 'click', form='xpath')
            element.click()
            print('REG {}: SALVANDO'.format(item))
            sleep(1.1)

            try:  #popup Ok em que a parte Adversa já possui outros processos.
                element = self.driver.find_element_by_id("popup_ok")
                self.driver.execute_script("arguments[0].click();", element)
                complementoAdversa = "{} --> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA".format(complementoAdversa)
                print('REG {}: ADVERSA TEM OUTROS PROCESSOS'.format(item))
            except:
                print('REG {}: ADVERSA NÃO TEM PROCESSOS'.format(item))
                pass
            _checkElemento = self.waitingElement('idDoCliente', 'show', form='class') #aguarda carregamento da página depois de salvar.

            try:
                hoje = "%s" % (strftime("%d-%m-%Y"))
                hora = strftime("%H:%M:%S")
                horaStr = hora.replace(':', '-')

                message = "{}{};".format(message, registro['txtPasta'])
                message = "{}{};".format(message, idNovaPasta)
                message = "{}{};".format(message, complementoAdversa)
                message = "{}{};".format(message, complementoNaoInseridos)

                print('REG {}: FINALIZADO às: {}'.format(item, horaStr))
            except:
                pass
        except:
            message = "{}; NÃO FOI POSSÍVEL ABRIR A PASTA {}".format(message, str(registro['txtPasta']))
        return message
















