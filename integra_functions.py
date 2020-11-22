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
import json

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
            sleep(1)
            self.driver.find_element_by_tag_name('button').click()
            sleep(1)
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

    def realizarPesquisa(self, search, tipoPesquisa):
        sleep(2)
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

            selecionaOpcao = self.waitingElement('{}'.format(xPathOption))
            selecionaOpcao.click()
            sleep(2)

            # valor do parâmetro
            textoPesquisa = self.waitingElement('txtPesquisa', 'show', 'id')
            textoPesquisa.send_keys(str(search))
            # self.driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(search))

            print("PESQUISANDO POR {}: {}".format(tipoPesquisa, search).upper())
            sleep(2)
            #botão pesquisar
            botaoPesquisar = self.waitingElement('btnPesquisar', 'click', 'id')
            botaoPesquisar.click()
            sleep(2)

            try:
                #Checa se não existe registros para essa pasta
                element = self.driver.find_element_by_id('loopVazio').is_displayed()
                hora = strftime("%H:%M:%S")
                print('{} - A/O {} {} NÃO FOI ENCONTRADO'.format(hora, tipoPesquisa, search).upper())
                retorno = False

            except:
                # SELECIONA O CLIENTE PESQUISADO        -  clica no primeiro item encontrado(não poderia ter duas pastas com o mesmo número)
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

        # TO DO FAZER LOOPING PARA ADD TODOS OS ARQUIVOS PERTINENTES AO PROCESSO/CLIENTE
        sleep(6)
        path = 'C:/Users/DPLAW-BACKUP/Desktop/dprobot/dpRobot/dplaw_Robot/pdf.pdf' # CAMINHO DO ARQUIVO
        # TO DO MONTAR CAMINHO DINAMICAMENTE # self.driver.send_keys(os.getcwd() + "/tests/sample_files/Figure1.tif")

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
                  '#card',
                  '#popup_content'
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

    def controle(self, registros, reg, logFileCSV):
        robo = None
        self.logFileCSV = logFileCSV
        self.isTest = basic_functions.checkIfTest()
        while True:
            if (reg != 'FIM' and reg != -1 and (reg < (len(registros['registros'])))):
                login, password = basic_functions.checkLogin(str(registros['tipo']))     #se for atualização - usa-se o login do robô
                print("\n-----------------------------------------")
                print("Login utilizado: {}".format(login))
                print("-----------------------------------------\n")
                print("\nINICIANDO WebDriver")
                _abreWebDriver = self.acessToIntegra(login, password)

                robo = self.abrePasta(registros, reg)
                print('ROBO = {}'.format(robo))
                if (robo):
                    basic_functions.createLog(self.logFileCSV, "FIM", printOut=False)
                    self.logoutIntegra()
                    break
                else:
                    self.driver.quit()
            else:
                print('NÃO HÁ MAIS REGISTROS NESSE ARQUIVO PARA IMPORTAR.'.upper())
                break
        return robo

    def abrePasta(self, registros, reg):
        clienteLocalizado = True
        ultimoCliente = ''
        elementoPesquisado = None

        while True:
            if (reg > len(registros['registros'])):
                break
            registro = registros['registros']['{}'.format(reg)]
            message = ''
            print('=========================================================')
            print('FALTAM {} DE {} REGISTROS PARA FINALIZAR!'.format((len(registros['registros']) -int(reg) + 1), len(registros['registros'])).upper())

            if ('abertura' in registros['tipo']):
                if (not(ultimoCliente) or (registro['razaoSocial'].upper() != ultimoCliente.upper())):
                    if not(self.isTest):
                        ultimoCliente = registro['razaoSocial']
                        self.driver.get(registro['urlCliente']) #redireciona p/ URL
                    else: #cliente teste
                        ultimoCliente = 'Cliente teste'
                        registro['razaoSocial'] = ultimoCliente
                        self.driver.get('https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=104330872&codigo2=104330872') #redireciona p/ URL

            tentativa = 1
            message = ''
            print('=========================================================')
            print('REG {}: INICIANDO: {}'.format(str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))

            try:
                print('REG {}: REALIZANDO PESQUISA: {}'.format(str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                if (self.isTest and 'abertura' in registros['tipo']):
                    searchFolder = False
                else:
                    try:
                        countChar = len(str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                        if (countChar >= 14):
                            searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else registro['pasta'], 'processo')  # INVERTIDO
                        else:
                            searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtPasta'], 'pasta')
                    except:
                        return False
                    # searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtPasta'], 'pasta')
            except:
                print('REG {}: NÃO FOI POSSÍVEL REALIZAR UMA BUSCA POR {}'.format(str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                return False

            if (not(searchFolder) and ('abertura' in registros['tipo'])): # SE NÃO EXISTE E FOR ABERTURA
                try:
                    sleep(2)
                    getClientName = self.waitingElement('//*[@id="txtNome"]', 'show')
                    if (getClientName.parent.title.upper() != registro['razaoSocial'].upper()):
                        clienteLocalizado, clienteEncontrado = self.realizarPesquisa(registro['razaoSocial'], 'cliente')
                        if (clienteLocalizado):
                            ultimoCliente = clienteEncontrado.text.strip().upper()
                            clienteEncontrado.click()
                            sleep(2)
                        else:
                            message = "REG {}; NÃO FOI LOCALIZADO NO PROMAD O CLIENTE {}. A PASTA {} NÃO FOI ABERTA! VERIFICAR!".format(str(reg), registro['razaoSocial'], str(registro['txtPasta']))
                            print(message)
                            continue

                    IncluirProcesso = self.waitingElement('//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 'click')
                    IncluirProcesso.click()
                    message = self.incluirProcesso(registro, reg, registros['tipo'])

                except:
                    print('REG {}: TENTATIVA {}: ERRO AO INCLUIR'.format(str(reg), tentativa))
                    if (tentativa > 5):
                        message = "REG {}; FOI REALIZADO {} TENTATIVAS E NÃO FOI POSSÍVEL REALIZAR A ABERTURA: {}".format(str(reg), tentativa, str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                        reg = reg + 1
                    tentativa = tentativa + 1
                    continue

                messageAgendamentos = ''
                if (('abertura' in registros['tipo']) and ('slcResponsavel' in registro) and message):
                    messageAgendamentos = self.criaAgendammentos(registro, reg)
                    if (self.isTest):
                        self.removeAgendamentos()
                else:
                    message = "{};;NÃO HÁ RESPONSÁVEIS PELA PASTA - NÃO FOI CRIADO NENHUM AGENDAMENTO! FAVOR VERIFICAR!".format(message)

                if (messageAgendamentos): message = '{}{}'.format(message, messageAgendamentos)

            elif (searchFolder) and ('atualizacao' in registros['tipo']):
                elementoPesquisado.click()
                message = self.incluirProcesso(registro, reg, registros['tipo'], itensExcluidosLoop = ['txtPasta'])
            elif not(searchFolder) and ('atualizacao' in registros['tipo']):
                message = "REG {};;A PASTA/PROCESSO {} NÃO EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'])
            else:
                message = "REG {};;A PASTA/PROCESSO {} JÁ EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'])
                print(message)

            basic_functions.createLog(self.logFileCSV, "{}\n".format(message), printOut=False)
            reg = reg + 1
        print('<<<<< NÃO HÁ MAIS REGISTROS PARA IMPORTAR. FINALIZANDO! >>>>>')
        return True

    def incluirProcesso(self, registro, reg, tipo, itensExcluidosLoop = []):

        def selecionaResponsaveis(respProcesso):
            #TODO em caso de alteração - desmarcar todas primeiro
            self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível
            comboResponsavel = self.waitingElement('//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button','click')
            comboResponsavel.click()  # clica e abre as opções
            sleep(.8)
            #recupera lista de RESPONSÁVEIS do PROMAD
            xInputs = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li'
            listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag
            # CARREGA LISTA DE RESPONSÁVEIS
            y = 1
            totalResp = len(respProcesso)
            countResp = 0
            respSelecionados = []
            for item in listInputs:  #itera inputs recuperados, checa e clica
                if (item.text in respProcesso):
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
            try:   # Segredo de Justiça  #por padrão, será marcado não
                element = self.driver.find_element_by_id("segredoJusticaN")
                self.driver.execute_script("arguments[0].click();", element)
                sleep(0.3)
                element = self.driver.find_element_by_id("capturarAndamentosS")
                self.driver.execute_script("arguments[0].click();", element)
            except:
                naoInserido['segredoCaptura'] = 'Segredo de Justiça e Andamentos'

        def recuperaIdIntegra():
            numIdPromad = ''
            try:
                numIdPromad = self.driver.find_element_by_class_name("idDoProcesso")
            except:
                try:
                    numIdPromad = self.driver.find_element_by_class_name("idDoCliente")
                except:
                    if (tipo == 'abertura'):
                        naoInserido['idDoProcessoINTEGRA'] = 'Não recuperado'
                    pass

            if (numIdPromad):
                numIdPromad = numIdPromad.get_attribute("innerHTML")
                numIdPromad = numIdPromad.split(' ')[-1].strip()
                print("REG {}: ID PROMAD: {}".format(reg, numIdPromad))
                return numIdPromad
            else:
                return numIdPromad

        def checkValueInCombo(texto, element):
            #TODO TRANSFORMAR EM FUNÇÃO GLOBAL
            try:
                select.select_by_visible_text(texto.title())
            except:
                try:
                    select.select_by_visible_text(texto.upper())
                except:
                    try:
                        select.select_by_visible_text(texto.lower())
                    except:
                        try:
                            select.select_by_visible_text(texto.lower().capitalize())
                        except:
                            listaElementos = self.driver.find_elements_by_xpath('//*[@id="{}"]/option'.format(k)) #recupera os inputs abaixo dessa tag
                            y = 1
                            found = False
                            while True:
                                try:
                                    for item in listaElementos:  #itera inputs recuperados, checa e clica
                                        if (item.text.upper() == v.upper()):
                                            xPathItem = '//*[@id="{}"]/option[{}]'.format(k, y)
                                            opcaoElemento = self.waitingElement(xPathItem, 'click')
                                            opcaoElemento.click()
                                            sleep(1)
                                            found=True
                                            break
                                        y = y + 1
                                    break
                                except:
                                    print('ERRO AO CARREGAR OU SELECIONAR TIPOS DE AGENDAMENTOS')
                                    continue

                            if (not(found)):
                                select.select_by_visible_text('--Cadastrar Novo Item--')
                                elemCadastro = self.waitingElement(element.replace('slc', 'txt'), 'click', form='id') # CADASTRAR NOVO ITEM
                                elemCadastro.clear()
                                elemCadastro.send_keys(str(texto).title())
            sleep(0.3)

        def _getURLpasta():
            link = self.driver.current_url
            linkbase = link.split('?')[0]
            codigos  = "{}&{}".format(link.split('&')[1], link.split('&')[2].replace('&paginaAnterior=',''))
            idNovaPasta = '=HIPERLINK("{}?{}")'.format(linkbase, codigos, idNovaPasta)
            #todo CHECAR IDNOVAPASTA

        self.checkPopUps()
        sleep(2)
        print('REG {}: INICIANDO INCLUSAO: {}'.format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
        naoInserido = {}
        camposInseridos = '|'

        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        message = ''
        message = "REG {};{} às {};".format(reg, hoje, hora)  #Insere a primeira linha do item no log

        print('REG {}: INICIANDO LOOPING'.format(reg))
        itensExcluidosLoop.extend(['razaoSocial', 'parteAdversa', 'sigla', 'agendamentos', 'urlCliente'])
        for k, v in registro.items():
            #todo salvar o valor antigo, no caso de atualização ou inserção em registro que já contém dados
            try:
                if (k in itensExcluidosLoop or v == None):
                    continue

                print ('REG {}: {} - "{}"'.format(reg, k, v))
                if (k == 'slcResponsavel'):
                    selecionaResponsaveis(v['Processo'])
                    camposInseridos = "{}{}: '{}' |".format(camposInseridos, k, v['Processo'])
                else:
                    element = self.waitingElement(k, 'click', form='id')
                    if (element.tag_name == 'select'):
                        try:
                            #todo TRATAR A STRING INTEIRA, CHECANDO SE É TODA MAIUSCULA OU MINUSCULA PRIMEIRO
                            valorElemento = str(v).title()
                            select = self.selenium.select(element)
                            select.select_by_visible_text(valorElemento)
                        except:
                            checkValueInCombo(str(v), k)
                    else: # (element.tag_name == 'input'): # inputs e textareas
                        element.clear()
                        element.send_keys(str(v))
                        if (k == 'txtNroCnj'):
                            segredoJusticaAndamentos()

                    camposInseridos = "{}{}: '{}' |".format(camposInseridos, k, v)
                    sleep(.8)
            except:
                naoInserido[k] = str(v)

        idNovaPasta = recuperaIdIntegra()
        complementoAdversa = ""
        if (tipo == 'abertura'):
            if ("parteAdversa" in registro):
                while True: # ABRE A PARTE ADVERSA
                    try:
                        menuCliente = self.waitingElement("//*[@id='div_menu17']", 'click')
                        menuCliente.click()
                        sleep(.8)
                        try: #checa se há mensagens que bloqueiam o salvamento #todo ver para demais elementos que não forem localizados
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
                complementoAdversa, naoInserido = self.inserirParteAdversa(registro, reg, naoInserido)

            print('REG {}: FINALIZADO O LOOPING'.format(reg))
            sleep(0.8)

        try: # Botão salvar
            print('REG {}: ANTES DE SALVAR'.format(reg))
            botaoSalvar = self.driver.find_element_by_id("btnSalvar")
            botaoSalvar.click()
            print('REG {}: SALVANDO'.format(reg))
            sleep(2)

            try:
                element = self.driver.find_element_by_class_name("confirm")
                complementoAdversa = "{} --> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA".format(complementoAdversa)
                print('REG {}: ADVERSA TEM OUTROS PROCESSOS'.format(reg))
            except:
                pass

            try:  #popup Ok em que a parte Adversa já possui outros processos.
                sleep(2)
                element = self.driver.find_element_by_id("popup_ok")
                self.driver.execute_script("arguments[0].click();", element)
            except:
                pass
            _checkElemento = self.waitingElement('idDoCliente', 'show', form='class') #aguarda carregamento da página depois de salvar.

            try:
                complementoNaoInseridos =''
                if (naoInserido):
                    complementoNaoInseridos = ''
                    for k1, v1 in naoInserido.items():
                        complementoNaoInseridos = '{} {}: "{}" | '.format(complementoNaoInseridos, k1, v1)

                hoje = "%s" % (strftime("%d-%m-%Y"))
                hora = strftime("%H:%M:%S")
                horaStr = hora.replace(':', '-')

                message = "{}{};".format(message, "'{}".format(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else ''))
                message = "{}{};".format(message, idNovaPasta)
                if (tipo == 'abertura'):
                    message = "{}{};".format(message, complementoAdversa)
                elif (tipo == 'atualizacao'):
                    message = "{}{};".format(message, camposInseridos)
                message = "{}{};".format(message, complementoNaoInseridos)

                print('REG {}: FINALIZADO às: {}'.format(reg, horaStr))
            except:
                pass
        except:
            message = "{}; NÃO FOI POSSÍVEL A ABERTURA/ATUALIZAÇÃO".format(message)
        return message

    def inserirParteAdversa(self, registro, reg, naoInserido):
        complementoAdversa = ""
        for k, v in registro['parteAdversa'].items():
            print ('REG {}: {} - {}'.format(reg, k, v))
            try:
                element = self.waitingElement(k, 'click', form='id')
                if (element.tag_name == 'input'):
                    element.clear()
                    element.send_keys(str(v))
                    print('REG {}: PREENCHENDO {} O VALOR: {}'.format(reg, k, v))

                elif (element.tag_name == 'select'):
                    try:
                        select = self.selenium.select(element)
                        select.select_by_visible_text(str(v))
                    except:
                        # checkValueInCombo(str(v), k)
                        pass
                sleep(.8)
            except:
                print('REG {}: ERRO AO INSERIR PARA {} O VALOR: {}'.format(reg, k, v))
                naoInserido[k] = str(v)
        complementoAdversa = "{}".format(str(registro['parteAdversa']['txtNome']))
        return (complementoAdversa, naoInserido)

    def criaAgendammentos(self, registro, reg):
        #TODO OS ITENS QUE NÃO FOREM CRIADOS OS SEUS AGENDAMENTOS: SALVA E OUTRO ARQUIVO PARA REFAZÊ-LOS
        print("REG {}: INICIANDO OS AGENDAMENTOS:".format(reg))
        self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
        agendNaoAbertos = list(registro['agendamentos'].keys())
        agendamentos    = registro['agendamentos'].copy()

        if ('HoraAudiencia' in agendNaoAbertos):
            agendNaoAbertos.remove('HoraAudiencia')
            del agendamentos['HoraAudiencia']

        message = ''
        messageFinal = ''
        messageNaoAbertos = ''
        refazAgendamento = 1

        for tipoAgendamento, agendamento in agendamentos.items():
            while True:
                self.checkPopUps()
                _formAgendamento = self.waitingElement('divAgendaCadastrar', 'show', 'id')
                print('ABRIU FORMULÁRIO DE AGENDAMENTOS')

                responsaveis = []
                textoAgendamento = ''

                print('REG {}: INICIANDO O AGENDAMENTO {}: {}'.format(reg, tipoAgendamento, agendamento))
                sleep(1)
                try:
                    xPathComboDestinatario = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                    elementComboDestinatario = self.waitingElement(xPathComboDestinatario, 'click')
                    elementComboDestinatario.click()
                except:
                    print('ERRO NO COMBO DESTINATÁRIO - INICIANDO NOVAMENTE')
                    break

                responsaveis    = registro['slcResponsavel'][tipoAgendamento]
                dataAgendamento = registro['agendamentos'][tipoAgendamento]

                if tipoAgendamento == 'Audiência':
                    if ('HoraAudiencia' in registro['agendamentos']):
                        HoraAudiencia = "{}".format(registro['agendamentos']['HoraAudiencia'])
                        textoAgendamento = "{} - Audiência designada para dia {} às {}".format(registro['sigla'], registro['agendamentos']['Audiência'], registro['agendamentos']['HoraAudiencia'])
                    else:
                        HoraAudiencia = "00:00"
                        textoAgendamento = "{} - Audiência designada para dia {}".format(registro['sigla'], registro['agendamentos']['Audiência'])
                    messageFinal = "{}".format(textoAgendamento.split('-')[1].strip().upper())

                elif tipoAgendamento == 'Ciencia de novo processo':
                    textoAgendamento = "{} - Certificar abertura, risco e promover agendamentos".format(registro['sigla'])

                elif tipoAgendamento == 'Anexar':
                    textoAgendamento = "ANEXAR"

                elif tipoAgendamento == 'Fotocópia':
                    textoAgendamento = "Fotocópia integral"

                totalResp = len(responsaveis)
                countResp = 0
                y = 1
                print('REG {}: SELECIONANDO OS RESPONSÁVEIS'.format(reg))
                listDestinatarios = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li')
                while True:
                    try:
                        for item in listDestinatarios:  #itera inputs recuperados, checa e clica
                            if (item.text in responsaveis ):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                element = self.waitingElement(xPathItem, 'click')
                                element.click()
                                sleep(1)
                                countResp = countResp + 1
                                if (countResp == totalResp):
                                    break
                            y = y + 1
                        break
                    except:
                        print('ERRO AO CARREGAR OU SELECIONAR DESTINATÁRIOS')
                        continue
                elementComboDestinatario.click()
                sleep(1)

                # combo TIPO - ABRIR
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button'
                comboTipoAgendamento = self.waitingElement(xPathElement, 'click')
                comboTipoAgendamento.click()
                sleep(1)

                print('REG {}: SELECIONANDO O TIPO TIPO DE AGENDAMENTO'.format(reg))
                listTiposAgendamentos = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li') #recupera os inputs abaixo dessa tag
                y = 1
                while True:
                    try:
                        for item in listTiposAgendamentos:  #itera inputs recuperados, checa e clica
                            if (item.text == tipoAgendamento):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(y)
                                element = self.waitingElement(xPathItem, 'click')
                                element.click()
                                sleep(1)
                                break
                            y = y + 1
                        break
                    except:
                        print('ERRO AO CARREGAR OU SELECIONAR TIPOS DE AGENDAMENTOS')
                        continue

                # CAMPO QUANDO  - SÓ SE A DATA FOR MAIOR QUE HOJE - se menor ou igual: mantém a data do sistema
                if (datetime.strptime(dataAgendamento, '%d/%m/%Y') > datetime.now()):
                    sleep(1)
                    xPathElement = '//*[@id="txtDataInicialAgendaProcesso1"]'
                    quandoElement = self.waitingElement(xPathElement, 'show')
                    quandoElement.clear()
                    sleep(1)
                    quandoElement.send_keys(dataAgendamento)
                    print('REG {}: SELECIONANDO A DATA DO AGENDAMENTO'.format(reg))

                    try: #se o calendário estiver aberto, será fechado
                        sleep(1)
                        self.driver.execute_script("$('#ui-datepicker-div').css('display', 'none');")
                    except:
                        print("ERRO CALENDÁRIO")

                    # COM HORA
                    try:
                        sleep(1)
                        if (tipoAgendamento == 'Audiência'):
                            print('REG {}: SELECIONANDO O HORÁRIO DA AUDIÊNCIA'.format(reg))
                            sleep(1)
                            xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso1"]'
                            checkComHora = self.waitingElement(xPathElement, 'click')
                            checkComHora.click()

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraInicialAgendaProcesso1"]'
                            horaInicial = self.waitingElement(xPathElement, 'click')
                            horaInicial.clear()
                            horaInicial.send_keys(HoraAudiencia)

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraFinalAgendaProcesso1"]'
                            horaFinal = self.waitingElement(xPathElement, 'show')
                            horaFinal.clear()
                            horaFinal.send_keys(HoraAudiencia)
                    except:
                        print('A audiência não tem HORARIO definido')
                        pass
                # campo textoAgendamento
                sleep(1)
                print('REG {}: PREENCHENDO O TEXTO DO AGENDAMENTO'.format(reg))
                xPathElement = '//*[@id="txtDescricaoAgendaProcesso1"]'
                campoAgendamento = self.waitingElement(xPathElement, 'show')
                campoAgendamento.clear()
                campoAgendamento.send_keys(textoAgendamento)

                # BOTÃO SALVAR
                try:
                    sleep(1)
                    print('REG {}: SALVANDO'.format(reg))
                    botaoSalvar = self.waitingElement('//*[@id="btnAgendarSalvar"]', 'click')
                    botaoSalvar.click()
                except:
                    print("ERRO AO CLICAR NO BOTÃO SALVAR!!!!")
                    pass

                sleep(1.5)
                # CHECA SE FALTOU INFORMAÇÕES NO INPUT
                validacaoCampos = self.waitingElement('idCampoValidateAgendar', 'show', 'id')
                if (validacaoCampos.text): # Se faltar informações nos inputs, dá um refresh na página e recomeça
                    print('REG {}: OS CAMPOS NÃO FORAM PREENCHIDOS CORRETAMENTE'.format(reg))
                    sleep(1)
                    self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #ATUALIZA A PÁGINA
                    print('TENTATIVA Nº {} DE 3'.format(refazAgendamento))
                    if (refazAgendamento <= 3): # 3 tentativas para o agendamento
                        refazAgendamento = refazAgendamento + 1
                        continue  #volta ao While TRUE e recomeça os preenchimentos
                    else:
                        refazAgendamento = 0
                        print("NÃO FOI POSSÍVEL REALIZAR O AGENDAMENTO DE {}!".format(tipoAgendamento))
                        break

                try: #Clicar no PopUp - Deseja salvar
                    sleep(1)
                    botaoPopUp = self.waitingElement('//*[@id="popup_ok"]', 'click')
                    botaoPopUp.click()
                    message = "{}|{}: '{}'".format(message, tipoAgendamento, agendamento) # add à message o tipo de agendamento REALIZADO.
                    print ("REG {}: CRIADO O AGENDAMENTO: |{}".format(reg, tipoAgendamento))
                    sleep(1.5)
                except:
                    print("erro POPUP SALVAR")
                    pass

                try: #remove agendamentos já executados
                    print('REG {}: REMOVENDO O AGENDAMENTO EXECUTADO'.format(reg))
                    agendNaoAbertos.remove(tipoAgendamento)
                except:
                    print('ERRO AgendNaoAbertos: {}'.format(tipoAgendamento))
                break # SE CHEGAR AQUI SEM ERRO - SAI DO LOOPING

        # APÓS O LOOPING
        sleep(1)
        if (agendNaoAbertos):
            for x in agendNaoAbertos:
                messageNaoAbertos = "{}|{}".format(messageNaoAbertos, x)

        if (messageFinal):
            print('REG {}: INSERINDO A MENSAGEM FINAL'.format(reg))
            message = "{};{}".format(message, messageFinal)

        if (messageNaoAbertos):
            print('REG {}: INSERINDO OS AGENDAMENTOS NÃO ABERTOS'.format(reg))
            message = "{};{}".format(message, messageNaoAbertos)
        print('FINALIZOU TODOS OS AGENDAMENTOS')

        return message

    def removeAgendamentos(self): # EXECUTA QUANDO ESTÁ EM MODO DE TESTE
        xInputs = '//*[@id="divAgendaListar"]/div/table/tbody/tr'
        tentativa = 1
        while True:
            try:
                sleep(2)
                listaAgendamentos = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag
                if (len(listaAgendamentos)>0):
                    agendItem = listaAgendamentos[-1].find_element_by_tag_name('a')
                    agendItem.click()
                    sleep(0.5)
                else:
                    break
            except:
                if (tentativa == 4):
                    print('ERRO AO REMOVER AGENDAMENTO')
                    break
                print('TENTATIVA {} DE REMOVER AGENDAMENTO'.format(tentativa))
                tentativa = tentativa + 1
                continue

            for _x in range(2):
                botaoPopup = self.waitingElement('popup_ok', 'click', 'id')
                botaoPopup.click()
                sleep(0.5)
            if (tentativa > 1): tentativa = 1

        print('OS AGENDAMENTOS DE TESTE FORAM EXCLUÍDOS COM SUCESSO!')

    def atualizacaoPasta(self, registros, reg):
        registros = registros['registros']
        for _k, registro in registros.items():
            tentativa = 1
            message = ''

            print('=========================================================')
            print('REG {}: INICIANDO'.format(str(reg), registro['txtPasta']))

            try:
                print('REG {}: REALIZANDO PESQUISA'.format(str(reg), registro['txtPasta']))
                if (self.isTest):
                    searchFolder = False
                else:
                    searchFolder, _element = self.realizarPesquisa(registro['txtPasta'], 'pasta')
            except:
                print('REG {}: NÃO FOI POSSÍVEL REALIZAR UMA BUSCA'.format(str(reg), registro['txtPasta']))
                return False

            print('NÃO HÁ MAIS REGISTROS PARA IMPORTAR. FINALIZANDO!')
            return True


#TODO  CRIAR UM GATILHO - PARA QUANDO A SESSÃO EXPIRAR OU O CHROME FECHAR - PRA VOLTAR PARA O ROBO MONITOR
#TODO MELHORAR OS LOGS - CAMPO SE EXISTE OUTROS PROCESSOS (P/MARCAR)   ERROS NÃO INSERIDOS PARA O FINAL (NOVO NOME: ITENS QUE NÃO FOI POSSÍVEL REALIZAR O PREENCHIMENTO)
#TODO PENSAR NA VOLTA DO pid PARA CHECAR NAS EXECUÇÕES SE O WEBDRIVER NÃO FOI FINALIZADO E RECOMEÇAR CASO TENHA SIDO.
#TODO ENVIAR OS ITENS PARA PESQUISA - CASO A PASTA EXISTA -> É FEITO O LOOPING SEM ATUALIZAR A PÁGINA