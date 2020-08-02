from selenium_functions import SeleniumFunctions
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import sleep
import basic_functions
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
            self.driver.get('https://adv.br/login-asp')
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
            element = self.waitingElement('//*[@id="header"]/ul/li[1]', 'click')
            element.click()
        except:
            print("ERRO AO CLICAR NO MENU CLIENTES")
            return False

        #submenu PESQUISAR CLIENTE
        sleep(3)
        try:
            element = self.waitingElement('//*[@id="header"]/ul/li[1]/ul/lii[1]/p', 'click')
            element.click()
        except:
            print("ERRO AO CLICAR NO SUBMENU PESQUISAR CLIENTES")
            return False
        return True

    def pesquisarCliente(self, search, tipoPesquisa):
        sleep(4)
        try:
            self.driver.get('https://adv.br/integra4/modulo/21/default.asp')
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
        # _abreWebDriver = None
        driverIniciado = False
        self.isTest = basic_functions.checkIfTest()

        hoje = "%s" % (strftime("%Y-%m-%d"))
        hoje = hoje.replace('-', '_')
        hora = strftime("%H:%M:%S")
        hora = hora.replace(':', '_')

        # CRIANDO ARQUIVO DE LOG .CSV
        self.logBase = '{}\\logs\\{}'.format(pathFolder.dirname(__file__), registros['tipo'])
        self.logFileCSV = "{}\\_log_{}.csv".format(self.logBase, '{}_{}__{}__{}'.format(registros['tipo'], registros['sigla'], hoje, hora))
        basic_functions.createFolder(self.logBase) # CRIA DIRETÓRIO SE NÃO EXISTIR.
        reg = basic_functions.checkEndFile(self.logFileCSV)

        if (reg != 'FIM' and reg != -1):
            login, password = basic_functions.checkLogin()
            print("\n-----------------------------------------")
            print("Login utilizado: {}".format(login))
            print("-----------------------------------------\n")
            print("\nINICIANDO WebDriver")
            _abreWebDriver = self.acessToIntegra(login, password)
            driverIniciado == True

            if (registros['tipo'] == 'abertura'):
                robo = self.abrePasta(registros, reg)
            # elif (registros['tipo'] == 'volumetria'):
            #     robo = self.Volumetria(registros)
            # elif (registros['tipo'] == 'contrato'):
            #     robo = self.Contrato(registros)
            # elif (registros['tipo'] == 'atualizacao'):
            #     robo = self.Atualizacao(registros)

            if (robo):
                basic_functions.createLog(self.logFileCSV, "FIM", printOut=False)
                if (driverIniciado == True):
                    driverIniciado = False
                    self.logoutIntegra()
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.driver.quit()
        else:
            print('NÃO HÁ MAIS REGISTROS NESSE ARQUIVO.')

    def abrePasta(self, registros, reg):
        if (reg <= (len(registros) - 2)):
            try:
                searchClient, elemPesquisado = self.pesquisarCliente('Cliente teste', 'cliente')
            except:
                return False
            if (searchClient):
                elemPesquisado.click()
                sleep(.5)
                urlPage = self.driver.current_url
                while reg < (len(registros) - 2): # 2 itens são padrão do objeto (não itens para o looping)
                    registro = registros['{}'.format(reg)].copy()
                    del registro['agendamentos']
                    message = ''
                    print('=========================================================')
                    print('REG {}: INICIANDO'.format(str(reg+1)))

                    try:
                        registro['txtNroProcesso'] = basic_functions.ajustarNumProcessoCNJ(registro['txtNroProcesso'])
                    except:
                        pass
                    try:
                        registro['txtNroCnj'] = basic_functions.ajustarNumProcessoCNJ(registro['txtNroCnj'])
                    except:
                        pass

                    try:
                        print('REG {}: REALIZANDO PESQUISA'.format(str(reg+1)))
                        # if (not(self.isTest)): #se não é teste
                        searchFolder = False
                        # else:
                        #     searchFolder, _element = self.pesquisarCliente(registro['txtPasta'], 'pasta')
                    except:
                        print('REG {}: NÃO FOI POSSÍVEL REALIZAR UMA BUSCA'.format(str(reg+1)))
                        return False

                    if (reg == 0): # CABEÇALHO DO LOG
                        cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA;ID PROMAD;PARTE ADVERSA; ERRO: NÃO INSERIDOS; AGENDAMENTOS CRIADOS; AUDIÊNCIA; ERRO: AGENDAMENTOS NÃO CRIADOS;'
                        basic_functions.createLog(self.logFileCSV, "{}\n".format(cabeçalhoLog), printOut=False)

                    if (not(searchFolder)):   # A PASTA NÃO EXISTE NO SISTEMA, SERÁ CRIADA!
                        try:
                            sleep(0.5)
                            print('REG {}: REDIRECIONANDO À PÁGINA DO CLIENTE -'.format(str(reg+1)))
                            self.driver.get(urlPage)
                            sleep(0.5)
                            message = self.incluirProcesso(registro, reg) # k=item
                        except:
                            print('REG {}: ERRO AO INCLUIR A PASTA: {}'.format(str(reg+1), registro['txtPasta']))
                            #TODO ver log para esse erro  - ver comportamento nessa situação  - CONTABILIZAR TENTATIVAS Q OCORREU
                            return False

                        if (registro['slcResponsavel'] and message):
                            self.criaAgendammentos(registros['{}'.format(reg)], reg)
                        else:
                            message = "{};;NÃO FOI CRIADO NENHUM AGENDAMENTO! FAVOR VERIFICAR!".format(message) #TODO - ver quantos ; serão necessários
                    else:
                        message = "REG {};;A PASTA {} JÁ EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(reg, registro['txtPasta'])
                        print(message)

                    basic_functions.createLog(self.logFileCSV, "{}\n".format(message), printOut=False)
                    reg = reg + 1
                print('NÃO HÁ MAIS REGISTROS PARA IMPORTAR. FINALIZANDO!')
                return True
            else:
                return False
        else:
            print('NÃO HÁ MAIS REGISTROS NESSE ARQUIVO.') # CASO JÁ TENHA PASSADO O TOTAL DE REGISTROS E NÃO TER FINALIZADO O ARQUIVO
            return False

    def incluirProcesso(self, registro, reg):

        def selecionaResponsaveis():
            self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível
            comboResponsavel = self.waitingElement('//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button','click')
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
                        element = self.waitingElement(xPathItem, 'click')
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
            try:
                if (registro['txtNroCnj']):   #TODO VERIFICAR SE DÁ PARA INSERIR OS IDs NO OBJETO (REGISTROS)
                    # Segredo de Justiça  #por padrão, será marcado não
                    element = self.driver.find_element_by_id("segredoJusticaN")
                    self.driver.execute_script("arguments[0].click();", element)
                    sleep(0.3)
                    element = self.driver.find_element_by_id("capturarAndamentosS")
                    self.driver.execute_script("arguments[0].click();", element)
            except:
                naoInserido['segredoCaptura'] = 'Segredo de Justiça e Andamentos'

        def recuperaIdIntegra():
            #Obtém o ID do PROMAD da nova pasta a ser aberta
            try:
                element = self.waitingElement("idDoProcesso", 'show', 'class')
                idNovaPasta = element.get_attribute("innerHTML")
                idNovaPasta = idNovaPasta[14:].strip()
                print("REG {}: NOVA PASTA ABERTA: {}".format(reg, idNovaPasta))
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
        print('REG {}: INICIANDO INCLUSAO DE PASTA'.format(reg+1))
        element = self.waitInstance(self.driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
        element.click()
        naoInserido = {}

        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        message = ''
        message = "REG {};{} às {};".format(reg+1, hoje, hora)  #Insere a primeira linha do item no log

        print('REG {}: INICIANDO LOOPING'.format(reg+1))
        for k, v in registro.items():
            print ('REG {}: {} - {}'.format(reg+1, k, v))
            try:
                if (k == 'slcResponsavel'):
                    selecionaResponsaveis()
                elif (k != 'razaoSocial' and k != 'adversa' and k != 'sigla'):
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
        print('REG {}: FINALIZADO O LOOPING'.format(reg+1))
        segredoJusticaAndamentos()
        idNovaPasta = recuperaIdIntegra()

        try:
            complementoAdversa = ""
            if (registro['adversa']):
                print('REG {}: EXISTE PARTE ADVERSA'.format(reg+1))
                while True:
                    try:
                        element = self.waitingElement("//*[@id='div_menu17']", 'click')
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
                    element = self.waitingElement('//*[@id="txtNome"]', 'click')
                    element.send_keys(str(registro['adversa']))
                    print("REG {}: REGISTRADO A PARTE ADVERSA: {}".format(reg+1, str(registro['adversa'])))
                    complementoAdversa = "{}".format(str(registro['adversa']))
                except:
                    naoInserido['adversa'] = str(registro['adversa'])
            else:
                naoInserido['adversa'] = ''
        except:
            print('REG {}: NÃO EXISTE PARTE ADVERSA'.format(reg+1))
            pass

        sleep(0.8)

        complementoNaoInseridos =''
        if (naoInserido):
            complementoNaoInseridos = 'NÃO FORAM INSERIDOS OS ITENS: '
            for k1, v1 in naoInserido.items():
                complementoNaoInseridos = '{} {}: "{}" | '.format(complementoNaoInseridos, k1, v1)
                print(complementoNaoInseridos)

        try: # Botão salvar
            print('REG {}: ANTES DE SALVAR'.format(reg+1))
            element = self.waitingElement('//*[@id="btnSalvar"]', 'click')
            element.click()
            print('REG {}: SALVANDO'.format(reg+1))
            sleep(1.1)

            try:  #popup Ok em que a parte Adversa já possui outros processos.
                element = self.driver.find_element_by_id("popup_ok")
                self.driver.execute_script("arguments[0].click();", element)
                complementoAdversa = "{} --> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA".format(complementoAdversa)
                print('REG {}: ADVERSA TEM OUTROS PROCESSOS'.format(reg+1))
            except:
                print('REG {}: ADVERSA NÃO TEM PROCESSOS'.format(reg+1))
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

                print('REG {}: FINALIZADO às: {}'.format(reg+1, horaStr))
            except:
                pass
        except:
            message = "{}; NÃO FOI POSSÍVEL ABRIR A PASTA {}".format(message, str(registro['txtPasta']))
        return message

    def criaAgendammentos(self, registro, reg):
        print("REG {}: INICIANDO OS AGENDAMENTOS:".format(reg))
        self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
        elementComboDestinatario = self.waitingElement(xPathElement, 'show')
        self.checkPopUps()

        agendNaoAbertos = list(registro['agendamentos'].keys())
        agendamentos    = registro['agendamentos'].copy()

        if ('HoraAudiencia' in agendNaoAbertos):
            agendNaoAbertos.remove('HoraAudiencia')
            del agendamentos['HoraAudiencia']

        responsaveisAudiencia = ['GST']
        responsaveisAnexar    = ['ESTAGBRA']
        responsaveisFotocopia = ['GST','operacoes']
        # responsaveisCiencia = ['COI', 'cbradesco', 'CBV', ]

        #recupera listas
        listDestinatarios     = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li') #recupera os inputs abaixo dessa tag
        # listTiposAgendamentos = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li') #recupera os inputs abaixo dessa tag

        for tipoAgendamento, agendamento in agendamentos.items():
            responsaveis = []
            textoAgendamento = ''
            print(tipoAgendamento,' - ', agendamento)
            elementComboDestinatario.click()

            #TODO ADD NO OBJETO RESPONSÁVEIS POR CADA AGENDAMENTO - EVITANDO ESSA GAMBIARRA
            if tipoAgendamento == 'Audiência':
                dataAgendamento = registro['agendamentos']['Audiência']
                responsaveis = registro['slcResponsavel'] + responsaveisAudiencia
                if (registro['agendamentos']['HoraAudiencia']):
                    textoAgendamento = "{} - Audiência designada para dia {} às {}".format(registro['sigla'], registro['agendamentos']['Audiência'], registro['agendamentos']['HoraAudiencia'])
                else:
                    textoAgendamento = "{} - Audiência designada para dia {}".format(registro['sigla'], registro['agendamentos']['Audiência'])
            elif tipoAgendamento == 'Ciencia de novo processo':
                dataAgendamento = registro['agendamentos']['Ciencia de novo processo']
                textoAgendamento = "{} - Certificar abertura, risco e promover agendamentos".format(registro['sigla'])
            elif tipoAgendamento == 'Anexar':
                responsaveis = registro['slcResponsavel'] + responsaveisAnexar
                textoAgendamento = "ANEXAR"
            elif tipoAgendamento == 'Fotocópia':
                responsaveis = registro['slcResponsavel'] + responsaveisFotocopia
                textoAgendamento = "Fotocópia integral"

            totalResp = len(responsaveis)
            countResp = 0
            y = 1
            for item in listDestinatarios:  #itera inputs recuperados, checa e clica
                if (item.text in responsaveis ):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                    element = self.waitingElement(xPathItem, 'click')
                    element.click()
                    sleep(1.5)
                    countResp = countResp + 1
                    if (countResp == (totalResp + 1)):
                        break
                y = y + 1
            elementComboDestinatario.click()

            # combo TIPO - ABRIR
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button'
            comboTipoAgendamento = self.waitingElement(xPathElement, 'click')
            comboTipoAgendamento.click()
            sleep(1.5)

            listTiposAgendamentos = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li') #recupera os inputs abaixo dessa tag #TODO - VERIFICAR PRA COLOCAR ANTES DO LOOPING (NÃO ESTAVA RECUPERANDO)
            y = 1
            for item in listTiposAgendamentos:  #itera inputs recuperados, checa e clica
                if (item.text == tipoAgendamento):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(y)
                    element = self.waitingElement(xPathItem, 'click')
                    element.click()
                    sleep(1.5)
                    break
                y = y + 1

            # CAMPO QUANDO
            sleep(.5)
            xPathElement = '//*[@id="txtDataInicialAgendaProcesso1"]'
            element = self.waitingElement(xPathElement, 'show')
            element.clear()
            element.send_keys(dataAgendamento)
            sleep(.5)

            # COM HORA
            if (tipoAgendamento == 'Audiência' and registro['agendamentos']['HoraAudiencia']):
                sleep(.5)
                xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso1"]'
                element = self.waitingElement(xPathElement, 'click')
                element.click() # MARCA - COM HORA

                sleep(.5)
                xPathElement = '//*[@id="txtHoraInicialAgendaProcesso1"]'
                element = self.waitingElement(xPathElement, 'click')
                element.clear()
                element.send_keys(registro['agendamentos']['HoraAudiencia'])

                sleep(.5)
                xPathElement = '//*[@id="txtHoraFinalAgendaProcesso1"]'
                element = self.waitingElement(xPathElement, 'show')
                element.clear()
                element.send_keys(registro['agendamentos']['HoraAudiencia'])

            # campo textoAgendamento
            sleep(.5)
            xPathElement = '//*[@id="txtDescricaoAgendaProcesso1"]'
            element = self.waitingElement(xPathElement, 'show')
            element.clear()
            element.send_keys(textoAgendamento)

            # campo resumo
            sleep(.5)
            xPathElement = '//*[@id="txtTituloAgendaProcesso1"]'
            element = self.waitingElement(xPathElement, 'show')
            element.clear()
            sleep(.5)
            xPathElement = '//*[@id="txtTituloAgendaProcesso1"]'
            element = self.waitingElement(xPathElement, 'show')
            element.send_keys(textoAgendamento[:30])

            # BOTÃO SALVAR
            try:
                sleep(.5)
                botaoSalvar = self.waitingElement('//*[@id="btnAgendarSalvar"]', 'click')
                botaoSalvar.click()
            except:
                print("ERRO AO CLICAR NO BOTÃO SALVAR!!!!")
                pass

            sleep(.5)
            try: # CHECA SE FALTOU INFORMAÇÕES NO INPUT
                element = self.waitingElement('idCampoValidateAgendar', 'show', 'id')
                if (element.text): # Se faltar informações nos inputs, dá um refresh na página e recomeça
                    element = self.waitingElement("//*[@id='slcGrupo']", 'show')  #checa se redirecionamento ocorreu
                    self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
                    xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                    element = self.waitingElement(xPathElement, 'show')
                    if (element == False):
                        print("erro: Elemento da página não foi encontrado!")
                    self.checkPopUps()
                    sleep(.5)
                    if (refazAgendamento < 1): # limita a 5 tentativas para o agendamento
                        refazAgendamento = refazAgendamento + 1
                        break #continue      #volta ao While TRUE e recomeça os preenchimentos
                    else:
                        refazAgendamento = 0
                        break
            except:
                print("erro INFORMAÇÕES NO INPUT")
                pass

            try: #Clicar no PopUp - Deseja salvar
                sleep(.5)
                element = self.waitingElement('//*[@id="popup_ok"]', 'click')
                element.click()
                message = "{} |{}".format(message, tipoAgendamento) # add à message o tipo de agendamento REALIZADO.
                print ("REG {}: CRIADO O AGENDAMENTO: |{}".format(registro, tipoAgendamento))
                sleep(.5)
            except:
                print("erro POPUP SALVAR")
                pass

            try: #remove agendamentos já executados
                agendNaoAbertos.remove(tipoAgendamento)
            except:
                print('ERRO AgendNaoAbertos: {}'.format(tipoAgendamento))
            break #sai do While TRUE


        print('FINALIZOU TODOS OS AGENDAMENTOS')





