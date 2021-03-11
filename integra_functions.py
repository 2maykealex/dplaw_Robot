from selenium_functions import SeleniumFunctions
from datetime import datetime
from time import strftime
from time import sleep
from sys import exc_info
from os import path
import basic_functions

class IntegraFunctions(object):

    def __init__(self):
        self.selenium = SeleniumFunctions()
        self.waitInstance = self.selenium.waitInstance
        self.driver = None
        self.login = None
        self.password = None

    def acessToIntegra(self, login, password):
        try:
            print("\nINICIANDO WebDriver")
            self.driver = self.selenium.iniciaWebdriver()
            self.driver.maximize_window()
            self.driver.get('https://integra.adv.br/login-integra.asp')
            self.driver.execute_script("document.getElementById('login_email').value='{}'".format(login))
            self.driver.execute_script("document.getElementById('login_senha').value='{}'".format(password))
            sleep(1)
            self.driver.find_element_by_tag_name('button').click()
            sleep(1)
            self.checkPopUps()
            print('LOGIN REALIZADO NO INTEGRA')
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
        sleep(3)
        contErro = 0
        while True:
            try:
                try:
                    self.driver.get('https://integra.adv.br/integra4/modulo/21/default.asp')
                    abriuPesquisa = True
                except:
                    abriuPesquisa = self.acessaMenuPesquisa()

                tabelaRegistro = ''
                retorno = None
                if (abriuPesquisa):
                    sleep(3)
                    self.checkPopUps()
                    xPathOption = ''

                    #tipo de pesquisa (opções)
                    if (tipoPesquisa == 'pasta'):
                        xPathOption = '//*[@id="chkPesquisa139"]'
                    elif (tipoPesquisa == 'cliente'):
                        xPathOption = '//*[@id="chkPesquisa133"]'
                    elif (tipoPesquisa == 'processo'):
                        xPathOption = '//*[@id="chkPesquisa137"]'

                    selecionaOpcao = self.waitingElement('{}'.format(xPathOption))
                    selecionaOpcao.click()
                    sleep(3)

                    # valor do parâmetro
                    textoPesquisa = self.waitingElement('txtPesquisa', 'show', 'id')
                    textoPesquisa.send_keys(str(search))

                    # print("\n{}PESQUISA -  {}: {}".format(self.fileName, tipoPesquisa, search).upper())
                    sleep(3)
                    botaoPesquisar = self.waitingElement('btnPesquisar', 'click', 'id')
                    botaoPesquisar.click()

                    #AGUARDA PELO CARREGAMENTO
                    while True:
                        element = self.driver.find_element_by_id('backgroundPopup').is_displayed()
                        if (not (element)):
                            break

                    contPesquisa = 0
                    while True:
                        try:
                            tabelaRegistro = self.waitingElement('divCliente', 'click', 'id')
                            sleep(2)
                            try:
                                tabelaRegistro = tabelaRegistro.find_element_by_class_name('tablesorter')
                                tabelaRegistro = tabelaRegistro.find_element_by_tag_name('tbody')
                                tabelaRegistro = tabelaRegistro.find_elements_by_tag_name('tr')[0]
                                tabelaRegistro = tabelaRegistro.find_elements_by_tag_name('td')[4]
                                # print('{}PESQUISA -  {}: {} - FOI ENCONTRADO'.format(self.fileName, tipoPesquisa, search).upper())
                                retorno = True
                            except:
                                try:
                                    loopVazio = tabelaRegistro.find_element_by_id('loopVazio')
                                except:
                                    continue
                                if (loopVazio.text.strip() == 'Nenhum registro foi encontrado.'):
                                    # print('{}PESQUISA -  {}: {} - NÃO FOI ENCONTRADO'.format(self.fileName, tipoPesquisa, search).upper())
                                    retorno = False
                                else:
                                    print('{} <<< ERRO!!! REFAZENDO A PESQUISA! >>>'.format(self.fileName))
                                    continue
                            break
                        except:
                            contPesquisa = contPesquisa + 1
                            print('\n{}AGUARDANDO CARREGAMENTO DA PESQUISA...{}'.format(self.fileName, contPesquisa+1))
                            sleep(1)
                            if (contPesquisa > 15):
                                retorno = False
                                break
                else:
                    retorno = False

                sleep(1.5)
                return retorno, tabelaRegistro

            except Exception as err:
                exception_type, exception_object, exception_traceback = exc_info()
                line_number = exception_traceback.tb_lineno
                print('{}\n ERRO EM {} na linha {} >>>'.format(self.fileName, err, line_number))
                contErro = contErro + 1
                if (contErro >= 3):
                    print('{}\n<<< FOI TENTADO REALIZAR A PESQUISA {} VEZES SEM SUCESSO. SAINDO!>>> '.format(self.fileName, contErro))
                    return False, False

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
        try:
            self.driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
        except:
            pass

        try:
            sleep(1.5)
            self.driver.quit()
        except:
            pass

    def checkPopUps(self):
        popUps = ['.popup_block',
                  '#menuvaimudar',
                  '#divFecharAvisoPopUp',
                  '#backgroundPopup',
                  '#carregando',
                  '#card',
                  '#popup_content'
                  ]
        for popUp in popUps:
            popUpElement = popUp.replace('.','').replace('#','')
            mostrar = True
            element = None
            try:
                element = self.driver.find_element_by_id(popUpElement)
            except:
                try:
                    element = self.driver.find_element_by_class_name(popUpElement)
                except:
                    mostrar = False

            if (mostrar):
                if (element.is_displayed()):
                    script = "$('{}').css('display', 'none');".format(popUp)
                    try:
                        self.driver.execute_script(script)
                        # print('POPUP "{}" FECHADO!'.format(popUp))
                        sleep(1.5)
                    except:
                        pass

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
        try:
            robo = None
            self.logFileCSV = logFileCSV
            self.fileName  = "\n===========================================================\n{}\n".format(logFileCSV.split('\\')[-1].upper())
            self.fileNameFim = "==========================================================="
            self.isTest = basic_functions.checkIfTest()
            self.login, self.password = basic_functions.checkLogin(str(registros['tipo']))     #se for atualização - usa-se o login do robô
            isCheck = True if ('CONF REG' in reg) else False
            reg = int(reg.replace('CONF ','').replace('REG ', ''))
            while True:
                if (not(isCheck)):
                    if (reg != -1 and (reg <= (len(registros['registros'])))):
                        robo = self.painelCliente(registros, reg)
                        reg = 1
                    else:
                        print('{} <<<NÃO HÁ MAIS REGISTROS NESSE ARQUIVO PARA IMPORTAR! >>>'.format(self.fileName).upper())
                        basic_functions.createLog(self.logFileCSV, "\n\nCONFERENCIA", printOut=False)
                        isCheck = True

                if (robo or isCheck):
                    from shutil import copy
                    logBackup = "{}LOGS\\backups\\{}".format(logFileCSV.split('LOGS')[0], logFileCSV.split('\\')[-1])
                    basic_functions.createFolder("{}backups".format(logBackup.split('backups')[0]))
                    if (not(path.isfile(logBackup))):
                        copy(logFileCSV, logBackup)

                    # print('\n=============== CONFERÊNCIA DE DADOS ===============')
                    # _abreWebDriver = self.acessToIntegra(self.login, self.password)
                    # while True:
                    #     if (reg > len(registros['registros'])):
                    #         break
                    #     registro = registros['registros']['{}'.format(reg)]
                    #     try:
                    #         countChar = len(str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                    #         if (countChar >= 14):
                    #             searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtNroProcesso'] if (registro['txtPasta'] in registro) else registro['txtPasta'], 'processo')  # INVERTIDO
                    #         else:
                    #             searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtPasta'], 'pasta')
                    #     except:
                    #         return False

                    #     basic_functions.createLog(self.logFileCSV, "\n", printOut=False)
                    #     if (searchFolder):
                    #         elementoPesquisado.click() # Na conferência, sempre vai clicar
                    #         message = self.incluiAlteraProcesso(registro, reg, registros['tipo'], check=True)
                    #         # confereAgendamentos = self.criaAgendammentos(registro, reg, True)
                    #         # if (confereAgendamentos): message = '{}{}'.format(message, confereAgendamentos)

                    #         if (message):
                    #             if (message == True): message = 'NENHUM ITEM PRECISOU DE CORREÇÃO!'
                    #             basic_functions.createLog(self.logFileCSV, "CONF REG {};;{};{};{}".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'], "FOI CHECADO", message), printOut=False)
                    #         else:
                    #             basic_functions.createLog(self.logFileCSV, "CONF REG {};;{};{}".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'], "NÃO FOI POSSIVEL CHECAR ESSA PASTA - CHECAR MANUALMENTE!"), printOut=False)
                    #     else:
                    #         basic_functions.createLog(self.logFileCSV, "CONF REG {};;{};{}".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'], "NÃO FOI POSSIVEL CHECAR ESSA PASTA - CHECAR MANUALMENTE!"), printOut=False)
                    #     reg = reg + 1

                    basic_functions.createLog(self.logFileCSV, "\nFIM;", printOut=False)
                    self.logoutIntegra()
                    return True
                else:
                    try:
                        self.logoutIntegra()
                        if (reg == 'FIM'):
                            print('{} <<<NÃO HÁ MAIS REGISTROS NESSE ARQUIVO PARA IMPORTAR! >>>'.format(self.fileName).upper())
                        else:
                            print('{} <<<HOUVE ALGUM ERRO NAS TENTATIVAS DE INSERIR/ALTERAR REGISTRO: {} >>>'.format(self.fileName).upper(), reg)
                        break
                    except:
                        pass

        except Exception as err:
            exception_type, exception_object, exception_traceback = exc_info()
            line_number = exception_traceback.tb_lineno
            print('{}\n ERRO EM {} na linha {} >>>'.format(self.fileName, err, line_number))
            self.driver.quit()
            return False

    def painelCliente(self, registros, reg):
        clienteLocalizado = True
        urlCliente = None
        ultimoCliente = ''
        elementoPesquisado = None
        _abreWebDriver = self.acessToIntegra(self.login, self.password)
        tentativa = 1
        try:
            while True:
                if (reg > len(registros['registros'])):
                    break
                registro = registros['registros']['{}'.format(reg)]
                message = ''

                try:
                    print('{}TOTAL DE {} REGISTROS => PARA FINALIZAR, FALTAM  => {}'.format(self.fileName, len(registros['registros']), len(registros['registros']) - int(reg) + 1))
                    print('{}REG {}: INICIANDO: {}'.format(self.fileName, str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))

                    if (not(ultimoCliente) or (registro['razaoSocial'].upper() != ultimoCliente.upper())):
                        if not(self.isTest):
                            ultimoCliente = registro['razaoSocial']
                            urlCliente = registro['urlCliente']
                        else:
                            ultimoCliente = 'Cliente teste'
                            registro['razaoSocial'] = ultimoCliente
                            urlCliente = 'https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=104330872&codigo2=104330872'

                    sleep(3)
                    self.driver.get(urlCliente)
                    sleep(3)
                    getClientName = self.waitingElement('//*[@id="txtNome"]', 'show')
                    if (getClientName.parent.title.upper() != registro['razaoSocial'].upper()):
                        clienteLocalizado, clienteEncontrado = self.realizarPesquisa(registro['razaoSocial'], 'cliente')
                        if (clienteLocalizado):
                            ultimoCliente = clienteEncontrado.text.strip().upper()
                            clienteEncontrado.click()
                            sleep(3)
                        else:
                            message = "REG {}; NÃO FOI LOCALIZADO NO PROMAD O CLIENTE {}. A PASTA {} NÃO FOI ABERTA! VERIFICAR!".format(str(reg), registro['razaoSocial'], str(registro['txtPasta']))
                            print("{}{}".format(self.fileName, message))
                            reg = reg + 1
                            continue

                    #pesquisa pasta/processo
                    campoPpesquisa = self.waitingElement('txtPesquisaProcesso', 'click', 'id')
                    if ('txtNroProcesso' in registro):
                        paramsPesquisa = registro['txtNroProcesso']
                    else:
                        self.waitingElement('chkPesquisaTipoProcessoPasta', 'click', 'id').click()
                        paramsPesquisa = registro['txtPasta']
                    campoPpesquisa.send_keys(str(paramsPesquisa))

                    botaoPesquisa = self.waitingElement('btnPesquisarProcesso', 'click', 'id')
                    botaoPesquisa.click()
                    sleep(2)

                    try:
                        selecionarProcesso = self.waitingElement('divProcesso', 'click', 'id')
                        selecionarProcesso = selecionarProcesso.find_elements_by_class_name('trPai')[0] #CHECA SE HÁ REGISTROS
                        searchFolder = True
                    except:
                        searchFolder = False

                    sleep(2)
                    if (not(searchFolder)): #se não há registros
                        if ('abertura' in registros['tipo']):
                            linkIncluiProcesso = self.waitingElement('//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 'click')
                            linkIncluiProcesso.click()
                            message = self.incluiAlteraProcesso(registro, reg, registros['tipo'])

                            if ('slcResponsavel' in registro and message):
                                messageAgendamentos = ''
                                messageAgendamentos = self.criaAgendammentos(registro, reg)
                                if (messageAgendamentos): message = '{}{}\n'.format(message, messageAgendamentos)
                                if (self.isTest):
                                    self.removeAgendamentos(reg)
                            else:
                                message = "{};;NÃO HÁ RESPONSÁVEIS PELA PASTA - NÃO FOI CRIADO NENHUM AGENDAMENTO! FAVOR VERIFICAR!".format(message)

                        elif ('atualizacao' in registros['tipo']):
                            message = "REG {};;A PASTA/PROCESSO {} NÃO EXISTE NO SISTEMA! FAVOR VERIFICAR!\n".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'])

                    elif (searchFolder): #se há registros
                        if ('atualizacao' in registros['tipo']):
                            selecionarProcesso.click()
                            message = '{}\n'.format(self.incluiAlteraProcesso(registro, reg, registros['tipo'], itensExcluidosLoop = ['txtPasta', 'txtNroProcesso']))

                        elif ('abertura' in registros['tipo']):
                            message = "REG {};;A PASTA/PROCESSO {} JÁ EXISTE NO SISTEMA! FAVOR VERIFICAR!\n".format(reg, registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else registro['txtPasta'])

                except Exception as err:
                    exception_type, exception_object, exception_traceback = exc_info()
                    line_number = exception_traceback.tb_lineno
                    print('{}REG {}: TENTATIVA {}: ERRO AO INCLUIR - linha:{} - erro: {}'.format(self.fileName, str(reg), tentativa, line_number, err))
                    if (tentativa > 5):
                        message = "REG {}; FOI REALIZADO {} TENTATIVAS E NÃO FOI POSSÍVEL REALIZAR A ABERTURA: {}".format(str(reg), tentativa, str(registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else registro['txtPasta']))
                        basic_functions.createLog(self.logFileCSV, "\n{}".format(message), printOut=False)
                        self.logoutIntegra()
                        return False

                    tentativa = tentativa + 1
                    continue

                basic_functions.createLog(self.logFileCSV, "{}".format(message), printOut=False)
                reg = reg + 1

            print('{}<<<<< NÃO HÁ MAIS REGISTROS PARA IMPORTAR. FINALIZANDO! >>>>>'.format(self.fileName))
            basic_functions.createLog(self.logFileCSV, "\n\nCONFERENCIA;", printOut=False)

        except Exception as err:
            exception_type, exception_object, exception_traceback = exc_info()
            line_number = exception_traceback.tb_lineno
            print('{}REG {}: <<< HOUVE UM ERRO: {} - na linha {} >>>'.format(self.fileName, reg, err, line_number))
            pass

        self.logoutIntegra()
        return True

    def incluiAlteraProcesso(self, registro, reg, tipo, itensExcluidosLoop = [], check=False):

        def selecionaResponsaveis():
            totalResp = len(respProcesso)
            countResp = 0
            respSelecionados = []
            for item in selectResponsaveis.options:
                if (item.text in respProcesso):
                    try:
                        item.click()
                        # print('{}REG {}: -> ITEM PREENCHIDO : {} -> RESPONSÁVEL "{}"'.format(self.fileName, reg, k, item.text))
                        respSelecionados.append(item.text)
                    except:
                        naoInserido['{}-{}'.format(k, countResp + 1)] = item.text
                    sleep(1)
                    countResp = countResp + 1
                    if (countResp == totalResp):
                        break
            self.driver.execute_script("$('#slcResponsavel').css('display', 'none');") # torna elemento visível

        def segredoJusticaAndamentos():
            try:   # Segredo de Justiça  #por padrão, será marcado não
                element = self.driver.find_element_by_id("segredoJusticaN")
                self.driver.execute_script("arguments[0].click();", element)
                sleep(0.5)
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
                # print("{}REG {}: -> ID PROMAD: {}".format(self.fileName, reg, numIdPromad))
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
                                    print('{}ERRO AO CARREGAR OU SELECIONAR TIPOS DE AGENDAMENTOS'.format(self.fileName))
                                    continue

                            if (not(found)):
                                select.select_by_visible_text('--Cadastrar Novo Item--')
                                elemCadastro = self.waitingElement(element.replace('slc', 'txt'), 'click', form='id') # CADASTRAR NOVO ITEM
                                elemCadastro.clear()
                                elemCadastro.send_keys(str(texto).title())
            sleep(0.5)

        def _getURLpasta():
            link = self.driver.current_url
            linkbase = link.split('?')[0]
            codigos  = "{}&{}".format(link.split('&')[1], link.split('&')[2].replace('&paginaAnterior=',''))
            idNovaPasta = '=HIPERLINK("{}?{}")'.format(linkbase, codigos, idNovaPasta)
            #todo CHECAR IDNOVAPASTA

        self.checkPopUps()
        # sleep(.5)
        print('{}REG {}: -> INICIANDO {}: {}'.format(self.fileName, reg, 'CHECAGEM' if (check) else tipo.upper() ,registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
        naoInserido = {}
        camposInseridos = '|'

        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        message = ''
        message = "REG {};{} às {};".format(reg, hoje, hora)  #Insere a primeira linha do item no log

        self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento slcResponsavel visível
        itensExcluidosLoop.extend(['razaoSocial', 'parteAdversa', 'sigla', 'agendamentos', 'urlCliente'])
        for k, v in registro.items():
            valorAntigo = ''
            #TODO salvar o valor antigo no LOG
            try:
                if (k in itensExcluidosLoop or v == None):
                    continue

                sleep(.5) #por segurança
                dadoCorrigido = ''
                if (check):
                    dadoCorrigido = ' (CORRIGIDO)'
                    if (k in ['txtNroCnj']):
                        v = basic_functions.ajustarNumProcessoCNJ(v)
                    # print ('{}REG {}: -> CHECANDO VALORES: {} - "{}"'.format(self.fileName, reg, k, v))

                element = self.waitingElement(k, 'click', form='id')
                if (k == 'slcResponsavel'):
                    selectResponsaveis = self.selenium.select(element)
                    respProcesso = v['Processo'].copy()
                    # sleep(.5)

                    itensNaoInseridos = []
                    if (check):
                        antigosSelecionados = []
                        all_selected_options = selectResponsaveis.all_selected_options
                        if (all_selected_options):
                            for item in all_selected_options:
                                if (item.text):
                                    antigosSelecionados.append(item.text)
                                    if (not(item.text in v['Processo'])):
                                        itensNaoInseridos.append(item.text)

                            if (itensNaoInseridos):
                                respProcesso = itensNaoInseridos
                                valorAntigo = ', '.join(antigosSelecionados)

                    if (not(check) or (check and itensNaoInseridos)):
                        selecionaResponsaveis()
                        camposInseridos = "{}{}: '{}' {} |".format(camposInseridos, k, respProcesso, dadoCorrigido)

                else:
                    # element = self.waitingElement(k, 'click', form='id')
                    # sleep(.5)
                    if (element.tag_name == 'select'):
                        valorElemento = str(v.strip()).title()
                        valorElemento = valorElemento.replace(' Do ', ' do ').replace(' Da ', ' da ').replace(' De ', ' de ')
                        select = self.selenium.select(element)
                        valorAntigo = select.first_selected_option.text
                        if (not(check) or (check and valorAntigo.upper() != (str(v.upper())))):
                            try:
                                select.select_by_visible_text(valorElemento)
                            except:
                                checkValueInCombo(str(v.strip()), k)
                            camposInseridos = "{}{}: '{}' {} |".format(camposInseridos, k, v, dadoCorrigido)
                            # print('{}REG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))

                    else: #QUANDO É INPUTS OU TEXTAREAS
                        is_V_Equal = False
                        if (check):
                            try: #SÓ SERÁ 'VERDADEIRO' SE O ELEMENTO E 'V.' FOREM DIFERENTES
                                is_V_Equal = True if (float(element.get_attribute('value').upper().strip().replace(',','.')) != float(v.strip().replace(',','.'))) else False
                            except:
                                is_V_Equal = True if (element.get_attribute('value').strip() != (str(v.strip()))) else False

                        if (not(check) or (check and is_V_Equal)):
                            if (not(check)):
                                if (tipo == 'atualizacao'): #TODO  -  CRIAR FUNÇÕES DE ATUALIZAÇÃO PARA COMPARAR
                                    if (k in ['txtCampoLivre3', 'txtCampoLivre4']):
                                        if (element.get_attribute('value') != ''):
                                            naoInserido[k] = 'NÃO PREENCHIDO O VALOR "{}"  -> JÁ ESTAVA PREENCHIDO COM O VALOR: "{}".'.format(str(v), element.get_attribute('value'))
                                            continue
                            element.clear()
                            element.send_keys(str(v))
                            if (k == 'txtNroCnj'):
                                segredoJusticaAndamentos()
                            camposInseridos = "{}{}: '{}' {} |".format(camposInseridos, k, v, dadoCorrigido)
                            # print('{}REG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))
            except Exception as err:
                print('{}REG {}: ERRO AO INSERIR PARA {} O VALOR: {} - {}'.format(self.fileName, reg, k, v, err))
                naoInserido[k] = str(v)

        if (naoInserido):
            print('{}REG {}: -> NÃO INSERIDOS: "{}"'.format(self.fileName, reg, naoInserido))

        idNovaPasta = recuperaIdIntegra()
        complementoAdversa = ''
        camposInseridosAdversa = '|'
        # sleep(.5)

        if ('abertura' in tipo): #TODO => CHECAR SE É VOLUMETRIA OU CONTRATO PA  (PODE TER NO FUTURO ATUALIZAÇÃO QUE VAI PARA A PARTE ADVERSA)
            if ("parteAdversa" in registro):
                menuAdversa = None
                countAdversa = 0
                while countAdversa < 5:
                    if (check):
                        menuAdversa = self.waitingElement("divMenuProcesso26", 'click', 'id')
                    else:
                        menuAdversa = self.waitingElement("//*[@id='div_menu17']", 'click')

                    # sleep(.5)
                    self.checkPopUps()
                    if (menuAdversa):
                        try:
                            menuAdversa.click()
                            # sleep(2)
                        except:
                            print('{}REG {}: <<< ERRO AO CLICAR NO MENU ADVERSA >>>'.format(self.fileName, reg))
                            countAdversa = countAdversa + 1
                            continue

                        try: #checa se há mensagens que bloqueiam o salvamento
                            element = self.driver.find_element_by_id('div_txtComarca').is_displayed() #TODO   -> CHECAR SE HÁ CAMPOS OBRIGATÓRIOS VAZIOS (ALÉM DESSE)
                            self.driver.execute_script("verificarComboNovo('-1','txtComarca','slcComarca');")
                            naoInserido['comarcaNova'] = str(registro['comarcaNova'])
                            # sleep(.5)
                            continue
                        except:
                            pass

                        try:
                            if (check):
                                # sleep(.5)
                                tabelaAdversa = self.waitingElement('efect-tableParteAdversa', 'click', form='id')
                                try:
                                    tabelaAdversa = tabelaAdversa.find_element_by_tag_name('tr')
                                except:
                                    tabelaAdversa = self.waitingElement('aAdverso', 'click', form='id')

                                # sleep(.5)
                                tabelaAdversa.click()
                                # sleep(.5)
                        except:
                            print('{}REG {}: <<< ERRO AO CLICAR NO TABELA COM A ADVERSA NA CHECAGEM >>>'.format(self.fileName, reg))
                            countAdversa = countAdversa + 1
                            continue

                        self.checkPopUps()
                        try:
                            complementoAdversa, naoInserido, camposInseridosAdversa = self.inserirParteAdversa(registro, reg, naoInserido, check=check)
                        except:
                            print('{}REG {}: <<< ERRO AO PASSAR PELA PARTE ADVERSA >>>'.format(self.fileName, reg))
                            countAdversa = countAdversa + 1
                            continue
                        # sleep(.5)

                        break
                    else:
                        print('{}REG {}: -> BUSCANDO O ELEMENTO DO MENU ADVERSA...'.format(self.fileName, reg))
                    countAdversa = countAdversa + 1

        if (check and camposInseridos == '|' and camposInseridosAdversa == '|'): #se não houveram correções, sai sem salvar
            print('sem alteração!!!!!!!!!')
            return True

        try: # Botão salvar
            countSalvar = 0
            if (check):
                if (camposInseridosAdversa != '|'): countSalvar = countSalvar + 1 #se teve correção na parte adversa
                if (camposInseridos != '|')       : countSalvar = countSalvar + 1 #se teve correção na parte administrativa/judicial
            else:
                countSalvar = 1

            if (countSalvar):
                for contSalvar in range(countSalvar):
                    botaoSalvar = None
                    botaoSalvar = self.driver.find_elements_by_id("btnSalvar")[contSalvar]
                    botaoSalvar.click()
                    print('{}REG {}: -> SALVANDO'.format(self.fileName, reg))
                    # sleep(.5)

                    try: # POP-UPS APÓS O SALVAMENTO
                        while True:
                            # sleep(.5)
                            container = self.waitingElement('popup_container', 'show', 'id')  #primeiro  #TODO melhorar a forma de buscar esse elemento
                            if (container):
                                try:
                                    janelaOutrosProcessos = self.driver.find_element_by_class_name("confirm")
                                except:
                                    janelaOutrosProcessos = False

                                btnOk = self.waitingElement('popup_ok', 'show', 'id')
                                btnOk.click()
                                # sleep(.5)

                                if (janelaOutrosProcessos):
                                    complementoAdversa = "{} --> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA".format(complementoAdversa)
                                    # print('{}REG {}: -> ADVERSA TEM OUTROS PROCESSOS'.format(self.fileName, reg))

                                    _checkElemento = self.waitingElement('idDoCliente', 'show', form='class') #aguarda carregamento da página depois de salvar.
                                    if (_checkElemento):
                                        break
                                    else:
                                        continue
                                else:
                                    break
                            else:
                                break
                    except:
                        pass
                    # sleep(.5)

            _checkElemento = self.waitingElement('idDoCliente', 'show', form='class')
            if (check):
                if (camposInseridos and camposInseridos !='|'):
                    return camposInseridos #SE HOUVER CAMPOS QUE FORAM CORRIGIDOS
                else:
                    return True

            try:
                complementoNaoInseridos =''
                if (naoInserido):
                    complementoNaoInseridos = ''
                    for k1, v1 in naoInserido.items():
                        complementoNaoInseridos = '{} {}: "{}" | '.format(complementoNaoInseridos, k1, v1)

                message = "{}{};".format(message, "'{}".format(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else ''))
                message = "{}{};".format(message, idNovaPasta)
                if (tipo == 'abertura'):
                    message = "{}{};".format(message, complementoAdversa)
                elif (tipo == 'atualizacao'):
                    message = "{}{};".format(message, camposInseridos)
                message = "{}{};".format(message, complementoNaoInseridos)
            except:
                pass
        except:
            if (check):
                return False

            message = "{}; NÃO FOI POSSÍVEL A ABERTURA/ATUALIZAÇÃO".format(message)
        return message

    def inserirParteAdversa(self, registro, reg, naoInserido, check=False):
        complementoAdversa = ''
        camposInseridos = ''
        dadoCorrigido = ''
        while True:
            try:
                for k, v in registro['parteAdversa'].items():
                    sleep(.5) #por segurança
                    if (check):
                        dadoCorrigido = ' (CORRIGIDO)'
                        # print('{}REG {}: -> CHECANDO VALORES: {} - "{}"'.format(self.fileName, reg, k, v))
                    try:
                        element = self.waitingElement(k, 'click', form='id')
                        if (not(check) or (check and element.get_attribute('value').upper().strip() != (str(v.upper().strip())))):
                            if (element.tag_name == 'input'):
                                element.clear()
                                element.send_keys(str(v))

                            elif (element.tag_name == 'select'):
                                try: #TODO CHECAR OS SELECTS DA PARTE ADVERSA
                                    select = self.selenium.select(element)
                                    select.select_by_visible_text(str(v))
                                except:
                                    # checkValueInCombo(str(v), k) #TODO CHECAR ISSO
                                    pass
                            # sleep(1)
                            camposInseridos = "{}{}: '{}' {} |".format(camposInseridos, k, v, dadoCorrigido)
                            # print('{}REG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))
                    except:
                        print('{}REG {}: ERRO AO INSERIR PARA {} O VALOR: {}'.format(self.fileName, reg, k, v))
                        naoInserido[k] = str(v)
                complementoAdversa = "{}".format(str(registro['parteAdversa']['txtNome']))
                sleep(1) #por segurança
                return (complementoAdversa, naoInserido, camposInseridos)
            except:
                print('{}REG {}: <<< ERRO AO PASSAR PELA PARTE ADVERSA >>>'.format(self.fileName, reg))

    def criaAgendammentos(self, registro, reg, check=False):

        def checkAgendamentos(registro):
            try:
                print('{}REG {}: OBTENDO AGENDAMENTOS JÁ REALIZADOS NA PASTA'.format(self.fileName, reg))
                listaAgendamentos = {}
                contAgend = 0
                while True:
                    sleep(2)
                    dadosAgendamento = {}
                    agendamentoItemHora = None
                    getAgendamentos = None
                    while True:
                        try:
                            getAgendamentos = self.waitingElement('tablesorter', 'show', 'class')
                            getAgendamentos = getAgendamentos.find_element_by_tag_name('tbody')
                            getAgendamentos = getAgendamentos.find_elements_by_tag_name('tr')
                            getAgendamentos[contAgend].click()
                            _cadastroAgendamentoPrincipal = self.waitingElement('cadastroAgendamentoPrincipal', 'show', 'id')
                            agendamentoItemTipo  = self.waitingElement('//*[@id="agendamentoConteudo"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/div[2]', 'show').text.strip()
                            agendamentoItemData  = self.waitingElement('//*[@id="agendamentoConteudo"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/label[1]', 'show').text.strip()
                            agendamentoItemDados = {}
                            agendamentoItemDados[agendamentoItemTipo] = agendamentoItemData
                            break
                        except:
                            pass

                    try:
                        agendamentoItemHora  = self.driver.find_element_by_xpath('//*[@id="agendamentoConteudo"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/label[2]').text.strip()
                        if (agendamentoItemHora):
                            agendamentoItemDados['HoraAudiencia'] = agendamentoItemHora
                    except:
                        pass
                    dadosAgendamento[agendamentoItemTipo] = agendamentoItemDados

                    try:
                        sleep(1)
                        listDestinatarios = self.driver.find_element_by_id('aDestinatario')
                        sleep(.5)
                        listDestinatarios.click()
                        listDestinatarios = self.waitingElement('JTPop_copy', 'show', 'id')
                        listDestinatarios = listDestinatarios.find_elements_by_tag_name('tr')
                        contDest = 1
                        resps = []
                        while True:
                            if (contDest <= len(listDestinatarios)-1):
                                resps.append(listDestinatarios[contDest].text.split('\n')[0])
                            else:
                                break
                            contDest = contDest + 1
                        dadosAgendamento[agendamentoItemTipo].update({'slcResponsavel': resps})
                    except:
                        print('erro')
                        pass

                    listaAgendamentos.update(dadosAgendamento)

                    try:
                        if ((agendamentoItemTipo in agendamentos.keys()) and (agendamentoItemData in agendamentos[agendamentoItemTipo])):
                            for resp in resps:
                                if (resp in agendamentos):
                                    pass

                            if (agendamentoItemTipo != 'HoraAudiencia'):
                                agendNaoAbertos.remove(agendamentoItemTipo)
                        else:
                            pass # Recadastrar item faltante
                    except:
                        pass

                    fecharAgendamento = self.waitingElement('agendamentoFechar', 'click', 'id')
                    fecharAgendamento.click()
                    while self.driver.find_element_by_id('carregando').is_displayed():
                        pass

                    contAgend = contAgend + 1
                    if (contAgend >= len(getAgendamentos)):
                        break
            except Exception as err:
                print('ERRO: {}'.format(err))
                return None
            return listaAgendamentos

        # print("{}REG {}: INICIANDO OS AGENDAMENTOS:".format(self.fileName, reg))
        sleep(1) #por segurança
        self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
        agendNaoAbertos = list(registro['agendamentos'].keys())
        agendamentos    = registro['agendamentos'].copy()

        if ('HoraAudiencia' in agendNaoAbertos):
            agendNaoAbertos.remove('HoraAudiencia')

        message = ''
        messageFinal = ''
        messageNaoAbertos = ''
        refazAgendamento = 1

        # agendamentosJaCriados = None
        # if (check):
        #     try:
        #         agendamentosJaCriados = checkAgendamentos(registro)
        #     except:
        #         print('erro')

        for tipoAgendamento, agendamento in agendamentos.items():
            if (tipoAgendamento == 'HoraAudiencia'):
                continue

            while True:
                self.checkPopUps()
                _formAgendamento = self.waitingElement('divAgendaCadastrar', 'show', 'id')
                # print('{}REG {}: INICIANDO O AGENDAMENTO {}: {}'.format(self.fileName, reg, tipoAgendamento, agendamento))
                # sleep(1)
                try:
                    xPathComboDestinatario = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                    elementComboDestinatario = self.waitingElement(xPathComboDestinatario, 'click')
                    sleep(.5)
                    elementComboDestinatario.click()
                except:
                    print('{}REG {}: <<< ERRO NO COMBO DESTINATÁRIO - INICIANDO NOVAMENTE >>>'.format(self.fileName, reg))
                    continue

                textoAgendamento = ''
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

                totalResp = len(registro['slcResponsavel'][tipoAgendamento])
                countResp = 0
                y = 1
                # print('{}REG {}: SELECIONANDO OS RESPONSÁVEIS'.format(self.fileName, reg))
                listDestinatarios = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li')
                # sleep(.5)
                while True:
                    try:
                        for item in listDestinatarios:  #itera inputs recuperados, checa e clica
                            if (item.text in registro['slcResponsavel'][tipoAgendamento] ):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                element = self.waitingElement(xPathItem, 'click')
                                element.click()
                                sleep(.3)
                                countResp = countResp + 1
                                if (countResp == totalResp):
                                    break
                            y = y + 1
                        break
                    except:
                        print('{}REG {}: <<< ERRO AO CARREGAR OU SELECIONAR DESTINATÁRIOS >>>'.format(self.fileName, reg))
                        continue
                elementComboDestinatario.click()
                sleep(1)

                # combo TIPO - ABRIR
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button'
                comboTipoAgendamento = self.waitingElement(xPathElement, 'click')
                comboTipoAgendamento.click()
                sleep(.5)

                # print('{}REG {}: SELECIONANDO O TIPO TIPO DE AGENDAMENTO'.format(self.fileName, reg))
                listTiposAgendamentos = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li') #recupera os inputs abaixo dessa tag
                y = 1
                while True:
                    try:
                        for item in listTiposAgendamentos:  #itera inputs recuperados, checa e clica
                            if (item.text == tipoAgendamento):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(y)
                                element = self.waitingElement(xPathItem, 'click')
                                element.click()
                                sleep(.3)
                                # sleep(1)
                                break
                            y = y + 1
                        break
                    except:
                        print('{}REG {}: <<< ERRO AO CARREGAR OU SELECIONAR TIPOS DE AGENDAMENTOS >>>'.format(self.fileName, reg))
                        continue

                # CAMPO QUANDO  - SÓ SE A DATA FOR MAIOR QUE HOJE - se menor ou igual: mantém a data do sistema
                if (datetime.strptime(agendamento, '%d/%m/%Y') > datetime.now()):
                    # sleep(1)
                    xPathElement = '//*[@id="txtDataInicialAgendaProcesso1"]'
                    quandoElement = self.waitingElement(xPathElement, 'show')
                    quandoElement.clear()
                    # sleep(.5)
                    quandoElement.send_keys(agendamento)
                    sleep(.5)
                    # print('{}REG {}: SELECIONANDO A DATA DO AGENDAMENTO'.format(self.fileName, reg))

                    try: #se o calendário estiver aberto, será fechado
                        self.driver.execute_script("$('#ui-datepicker-div').css('display', 'none');")
                    except:
                        print("{}REG {}: <<< ERRO CALENDÁRIO >>>".format(self.fileName, reg))

                    # COM HORA
                    sleep(.5)
                    try:
                        if (tipoAgendamento == 'Audiência'):
                            # print('{}REG {}: SELECIONANDO O HORÁRIO DA AUDIÊNCIA'.format(self.fileName, reg))
                            xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso1"]'
                            checkComHora = self.waitingElement(xPathElement, 'click')
                            checkComHora.click()
                            sleep(.5)

                            xPathElement = '//*[@id="txtHoraInicialAgendaProcesso1"]'
                            horaInicial = self.waitingElement(xPathElement, 'click')
                            horaInicial.clear()
                            horaInicial.send_keys(HoraAudiencia)
                            sleep(.5)

                            xPathElement = '//*[@id="txtHoraFinalAgendaProcesso1"]'
                            horaFinal = self.waitingElement(xPathElement, 'show')
                            horaFinal.clear()
                            horaFinal.send_keys(HoraAudiencia)
                    except:
                        print('{}REG {}: A audiência não tem HORARIO definido'.format(self.fileName, reg).upper())
                        pass
                # campo textoAgendamento
                sleep(.5)
                # print('{}REG {}: PREENCHENDO O TEXTO DO AGENDAMENTO'.format(self.fileName, reg))
                xPathElement = '//*[@id="txtDescricaoAgendaProcesso1"]'
                campoAgendamento = self.waitingElement(xPathElement, 'show')
                campoAgendamento.clear()
                campoAgendamento.send_keys(textoAgendamento)
                sleep(.5)

                # BOTÃO SALVAR
                try:
                    # print('{}REG {}: SALVANDO AGENDAMENTO: {}'.format(self.fileName, reg, tipoAgendamento.upper()))
                    botaoSalvar = self.waitingElement('//*[@id="btnAgendarSalvar"]', 'click')
                    botaoSalvar.click()
                except:
                    print("{}REG {}: <<< ERRO AO CLICAR NO BOTÃO SALVAR!!!! >>>".format(self.fileName, reg))
                    pass

                sleep(1)
                # CHECA SE FALTOU INFORMAÇÕES NO INPUT
                validacaoCampos = self.waitingElement('idCampoValidateAgendar', 'show', 'id')
                if (validacaoCampos.text): # Se faltar informações nos inputs, dá um refresh na página e recomeça
                    print('{}REG {}: OS CAMPOS NÃO FORAM PREENCHIDOS CORRETAMENTE'.format(self.fileName, reg))
                    sleep(1)
                    self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #ATUALIZA A PÁGINA
                    print('{}REG {}: TENTATIVA Nº {} DE 3'.format(self.fileName, reg, refazAgendamento))
                    if (refazAgendamento <= 3): # 3 tentativas para o agendamento
                        refazAgendamento = refazAgendamento + 1
                        continue  #volta ao While TRUE e recomeça os preenchimentos
                    else:
                        refazAgendamento = 0
                        print("{}REG {}: NÃO FOI POSSÍVEL REALIZAR O AGENDAMENTO DE {}!".format(self.fileName, reg, tipoAgendamento))
                        break

                try: #Clicar no PopUp - Deseja salvar
                    sleep(1)
                    botaoPopUp = self.waitingElement('//*[@id="popup_ok"]', 'click')
                    botaoPopUp.click()
                    message = "{}|{}: '{}'".format(message, tipoAgendamento, agendamento) # add à message o tipo de agendamento REALIZADO.
                    print("{}REG {}: CRIADO O AGENDAMENTO: |{}".format(self.fileName, reg, tipoAgendamento))
                    sleep(1)
                except:
                    print("{}REG {}: <<< ERRO POPUP SALVAR >>>".format(self.fileName, reg))
                    pass

                try: #remove agendamentos já executados
                    # print('{}REG {}: REMOVENDO O AGENDAMENTO EXECUTADO DA LISTA DE NÃO ABERTOS'.format(self.fileName, reg))
                    agendNaoAbertos.remove(tipoAgendamento)
                except:
                    print('{}REG {}: <<< ERRO AgendNaoAbertos: {} >>>'.format(self.fileName, reg, tipoAgendamento))
                break # SE CHEGAR AQUI SEM ERRO - SAI DO LOOPING

        # APÓS O LOOPING
        sleep(.5)
        if (agendNaoAbertos):
            for x in agendNaoAbertos:
                messageNaoAbertos = "{}|{}".format(messageNaoAbertos, x)

        if (messageFinal):
            # print('{}REG {}: INSERINDO A MENSAGEM FINAL'.format(self.fileName, reg))
            message = "{};{}".format(message, messageFinal)

        if (messageNaoAbertos):
            # print('{}REG {}: INSERINDO OS AGENDAMENTOS NÃO ABERTOS'.format(self.fileName, reg))
            message = "{};{}".format(message, messageNaoAbertos)
        # print('{}REG {}: FINALIZOU TODOS OS AGENDAMENTOS'.format(self.fileName, reg))

        return message

    def removeAgendamentos(self, reg): # EXECUTA QUANDO ESTÁ EM MODO DE TESTE
        xInputs = '//*[@id="divAgendaListar"]/div/table/tbody/tr'
        tentativa = 1
        while True:
            try:
                # sleep(2)
                listaAgendamentos = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag
                if (len(listaAgendamentos)>0):
                    agendItem = listaAgendamentos[-1].find_element_by_tag_name('a')
                    agendItem.click()
                    print('{}REMOVIDO O AGENDAMENTO DE TESTE: "{}" -> REMOVIDO NA {}ª TENTATIVA'.format(self.fileName, listaAgendamentos[-1].find_elements_by_tag_name('td')[3].text.strip(),tentativa))
                    sleep(0.5)
                else:
                    break
            except:
                if (tentativa == 4):
                    print('{}ERRO AO REMOVER AGENDAMENTO'.format(self.fileName))
                    break
                print('{}TENTATIVA {} DE REMOVER AGENDAMENTO'.format(self.fileName, tentativa))
                tentativa = tentativa + 1
                continue

            for _x in range(2):
                botaoPopup = self.waitingElement('popup_ok', 'click', 'id')
                botaoPopup.click()
                sleep(0.5)
            if (tentativa > 1): tentativa = 1

        print('{}REG {}: OS AGENDAMENTOS DE TESTE FORAM EXCLUÍDOS COM SUCESSO!'.format(self.fileName, reg))



#TODO  -> SALVAR TODAS AS MENSAGENS GERADAS EM DICIONÁRIO - DEPOIS, TRANSFORMÁ-LAS EM STRING COM PONTOS E VIRGULAS CORRETAMENTE NA ESTRUTURA

#TODO SE DER ERRO OU FALHA NA VERIFICAÇÃO -> DAR UM CONTINUE E REINICIAR O WEBDRIVER (SE ISSO FOR O CASO)
#TODO  CRIAR UM GATILHO - PARA QUANDO A SESSÃO EXPIRAR OU O CHROME FECHAR - PRA VOLTAR PARA O ROBO MONITOR
#TODO MELHORAR OS LOGS - CAMPO SE EXISTE OUTROS PROCESSOS (P/MARCAR)   ERROS NÃO INSERIDOS PARA O FINAL (NOVO NOME: ITENS QUE NÃO FOI POSSÍVEL REALIZAR O PREENCHIMENTO)
#TODO PENSAR NA VOLTA DO pid PARA CHECAR NAS EXECUÇÕES SE O WEBDRIVER NÃO FOI FINALIZADO E RECOMEÇAR CASO TENHA SIDO.
#TODO ENVIAR OS ITENS PARA PESQUISA - CASO A PASTA EXISTA -> É FEITO O LOOPING SEM ATUALIZAR A PÁGINA