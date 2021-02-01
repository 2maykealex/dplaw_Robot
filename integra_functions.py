from selenium_functions import SeleniumFunctions
from datetime import datetime
from time import strftime
from time import sleep
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

            print("\n{}PESQUISA -  {}: {}".format(self.fileName, tipoPesquisa, search).upper())
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
                    break
                except:
                    contPesquisa = contPesquisa + 1
                    print('\n{}AGUARDANDO CARREGAMENTO DA PESQUISA...{}'.format(self.fileName, contPesquisa+1))
                    sleep(1)
                    if (contPesquisa > 15):
                        retorno = False
                        break

            if (tabelaRegistro):
                try:
                    sleep(1)
                    tabelaRegistro = tabelaRegistro.find_element_by_class_name('tablesorter')
                    tabelaRegistro = tabelaRegistro.find_element_by_tag_name('tbody')
                    tabelaRegistro = tabelaRegistro.find_elements_by_tag_name('tr')[0]
                    tabelaRegistro = tabelaRegistro.find_elements_by_tag_name('td')[4]
                    print('{}PESQUISA -  {}: {} - FOI ENCONTRADO'.format(self.fileName, tipoPesquisa, search).upper())
                    retorno = True
                except:
                    tabelaRegistro = tabelaRegistro.find_element_by_id('loopVazio')
                    print('{}PESQUISA -  {}: {} - NÃO FOI ENCONTRADO'.format(self.fileName, tipoPesquisa, search).upper())
                    retorno = False
        else:
            retorno = False

        sleep(1.5)
        return retorno, tabelaRegistro

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
        try:
            robo = None
            self.logFileCSV = logFileCSV
            self.fileName = "{} ==> ".format(logFileCSV.split('\\')[-1].upper())
            self.isTest = basic_functions.checkIfTest()
            self.login, self.password = basic_functions.checkLogin(str(registros['tipo']))     #se for atualização - usa-se o login do robô
            while True:
                if (isinstance(reg, int)):
                    if (reg != -1 and (reg <= (len(registros['registros'])))):
                        robo = self.abrePasta(registros, reg)
                    else:
                        print('{} <<<NÃO HÁ MAIS REGISTROS NESSE ARQUIVO PARA IMPORTAR! >>>'.format(self.fileName).upper())
                        basic_functions.createLog(self.logFileCSV, "\nCONFERENCIA", printOut=False)
                        reg = 'CONFERENCIA'

                if (robo or reg == 'CONFERENCIA'):
                    # print('\n=============== CONFERÊNCIA DE DADOS ===============')
                    # _abreWebDriver = self.acessToIntegra(self.login, self.password)
                    # reg = 1
                    # while True:
                    #     if (reg > len(registros['registros'])):
                    #         break
                    #     registro = registros['registros']['{}'.format(reg)]
                    #     try:
                    #         countChar = len(str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                    #         if (countChar >= 14):
                    #             _searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else registro['txtPasta'], 'processo')  # INVERTIDO
                    #         else:
                    #             _searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtPasta'], 'pasta')
                    #     except:
                    #         return False

                    #     if (elementoPesquisado):
                    #         elementoPesquisado.click() # Na conferência, sempre vai clicar
                    #         messageConferencia = self.incluiAlteraProcesso(registro, reg, registros['tipo'], check=True)
                    #         # confereAgendamentos = self.criaAgendammentos(registro, reg, True)
                    #     reg = reg + 1

                    basic_functions.createLog(self.logFileCSV, "\nFIM", printOut=False)
                    self.logoutIntegra()
                    return True
                else:
                    try:
                        self.logoutIntegra()
                        print('{} <<<NÃO HÁ MAIS REGISTROS NESSE ARQUIVO PARA IMPORTAR! >>>'.format(self.fileName).upper())
                        break
                    except:
                        pass

        except Exception as err:
            print('{}\n ERRO EM {}'.format(self.fileName, err))
            self.driver.quit()
            return False

    def abrePasta(self, registros, reg):
        clienteLocalizado = True
        ultimoCliente = ''
        elementoPesquisado = None
        _abreWebDriver = self.acessToIntegra(self.login, self.password)
        try:
            while True:
                if (reg > len(registros['registros'])):
                    break
                registro = registros['registros']['{}'.format(reg)]
                message = ''
                print('=========================================================')
                print('{}FALTAM {} DE {} REGISTROS PARA FINALIZAR!'.format(self.fileName, (len(registros['registros']) -int(reg) + 1), len(registros['registros'])).upper())

                if ('abertura' in registros['tipo']):
                    if (not(ultimoCliente) or (registro['razaoSocial'].upper() != ultimoCliente.upper())):
                        if not(self.isTest):
                            ultimoCliente = registro['razaoSocial']
                        else: #cliente teste
                            ultimoCliente = 'Cliente teste'
                            registro['razaoSocial'] = ultimoCliente
                            self.driver.get('https://integra.adv.br/integra4/modulo/21/parteVisualizar.asp?codigo=104330872&codigo2=104330872') #redireciona p/ URL

                tentativa = 1
                message = ''
                print('=========================================================')
                print('{}REG {}: INICIANDO: {}'.format(self.fileName, str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))

                searchFolder = None
                try:
                    print('{}REG {}: REALIZANDO PESQUISA: {}'.format(self.fileName, str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                    if (self.isTest and 'abertura' in registros['tipo']):
                        searchFolder = False
                    else:
                        try:
                            countChar = len(str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                            if (countChar >= 14):
                                searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtNroProcesso'] if ('txtNroProcesso' in registro) else registro['txtPasta'], 'processo')  # INVERTIDO
                            else:
                                searchFolder, elementoPesquisado = self.realizarPesquisa(registro['txtPasta'], 'pasta')
                        except:
                            return False
                except:
                    print('{}REG {}: NÃO FOI POSSÍVEL REALIZAR UMA BUSCA POR {}'.format(self.fileName, str(reg), registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                    return False

                if (not(searchFolder) and ('abertura' in registros['tipo'])): # SE NÃO EXISTE E FOR ABERTURA
                    try:
                        sleep(3)
                        self.driver.get(registro['urlCliente']) #redireciona p/ URL
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
                                continue

                        incluiAlteraProcesso = self.waitingElement('//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 'click')
                        incluiAlteraProcesso.click()
                        message = self.incluiAlteraProcesso(registro, reg, registros['tipo'])

                    except:
                        print('{}REG {}: TENTATIVA {}: ERRO AO INCLUIR'.format(self.fileName, str(reg), tentativa))
                        if (tentativa > 5):
                            message = "REG {}; FOI REALIZADO {} TENTATIVAS E NÃO FOI POSSÍVEL REALIZAR A ABERTURA: {}".format(str(reg), tentativa, str(registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
                            reg = reg + 1
                        tentativa = tentativa + 1
                        continue

                    messageAgendamentos = ''
                    if (('abertura' in registros['tipo']) and ('slcResponsavel' in registro) and message):
                        messageAgendamentos = self.criaAgendammentos(registro, reg)
                        if (self.isTest):
                            self.removeAgendamentos(reg)
                    else:
                        message = "{};;NÃO HÁ RESPONSÁVEIS PELA PASTA - NÃO FOI CRIADO NENHUM AGENDAMENTO! FAVOR VERIFICAR!".format(message)

                    if (messageAgendamentos): message = '{}{}'.format(message, messageAgendamentos)

                elif (searchFolder) and ('atualizacao' in registros['tipo']):
                    sleep(1.3)
                    elementoPesquisado.click()
                    message = self.incluiAlteraProcesso(registro, reg, registros['tipo'], itensExcluidosLoop = ['txtPasta'])
                elif not(searchFolder) and ('atualizacao' in registros['tipo']):
                    message = "REG {};;A PASTA/PROCESSO {} NÃO EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'])
                else:
                    message = "REG {};;A PASTA/PROCESSO {} JÁ EXISTE NO SISTEMA! FAVOR VERIFICAR!".format(reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso'])
                    print(message)

                basic_functions.createLog(self.logFileCSV, "{}\n".format(message), printOut=False)
                reg = reg + 1
            print('{}<<<<< NÃO HÁ MAIS REGISTROS PARA IMPORTAR. FINALIZANDO! >>>>>'.format(self.fileName))
        except Exception as err:
            print('{}REG {}: <<< HOUVE UM ERRO: {} >>>'.format(self.fileName, reg, err))
            pass

        basic_functions.createLog(self.logFileCSV, "\nCONFERENCIA", printOut=False)
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
                        print('\n{}REG {}: -> ITEM PREENCHIDO : {} -> RESPONSÁVEL "{}"'.format(self.fileName, reg, k, item.text))
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
                print("\n{}REG {}: -> ID PROMAD: {}".format(self.fileName, reg, numIdPromad))
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
        sleep(2)
        print('\n{}REG {}: -> INICIANDO: {}'.format(self.fileName, reg, registro['txtPasta'] if ('txtPasta' in registro) else registro['txtNroProcesso']))
        naoInserido = {}
        camposInseridos = '|'

        hoje = "%s" % (strftime("%d-%m-%Y"))
        hoje = hoje.replace('-', '/')
        hora = strftime("%H:%M:%S")
        message = ''
        message = "REG {};{} às {};".format(reg, hoje, hora)  #Insere a primeira linha do item no log

        itensExcluidosLoop.extend(['razaoSocial', 'parteAdversa', 'sigla', 'agendamentos', 'urlCliente'])
        for k, v in registro.items():
            valorAntigo = ''
            #TODO salvar o valor antigo, no caso de atualização ou inserção em registro que já contém dados
            try:
                if (k in itensExcluidosLoop or v == None):
                    continue

                if (check):
                    if (k in ['txtNroCnj']):
                        v = basic_functions.ajustarNumProcessoCNJ(v)
                    print ('\n{}REG {}: -> CHECANDO VALORES: {} - "{}"'.format(self.fileName, reg, k, v))

                #TODO   verificar se dá pra MOVER  "if (k == 'slcResponsavel'):"    PARA DENTRO DO   "if (element.tag_name == 'select')"  (LOGO ABAIXO)
                if (k == 'slcResponsavel'):
                    self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível
                    selectResponsaveis = self.waitingElement(k, 'click', form='id')
                    selectResponsaveis = self.selenium.select(selectResponsaveis)
                    respProcesso = v['Processo'].copy()

                    if (check):
                        antigosSelecionados = []
                        all_selected_options = selectResponsaveis.all_selected_options
                        if (all_selected_options):
                            for item in all_selected_options:
                                antigosSelecionados.append(item.text)
                            respProcesso = list(set(respProcesso) - set(antigosSelecionados))
                            valorAntigo = ''.join(antigosSelecionados)

                    selecionaResponsaveis()
                    camposInseridos = "{}{}: '{}' |".format(camposInseridos, k, respProcesso)

                else:
                    element = self.waitingElement(k, 'click', form='id')
                    if (element.tag_name == 'select'):
                        valorElemento = str(v.strip()).title()
                        valorElemento = valorElemento.replace(' Do ', ' do ').replace(' Da ', ' da ').replace(' De ', ' de ')
                        select = self.selenium.select(element)
                        valorAntigo = select.first_selected_option.text
                        if (not(check) or (check and valorAntigo != (str(v)))):
                            try:
                                select.select_by_visible_text(valorElemento)
                            except:
                                checkValueInCombo(str(v.strip()), k)
                            camposInseridos = "{}{}: '{}' |".format(camposInseridos, k, v)
                            print('\n{}REG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))

                    else: #QUANDO É INPUTS OU TEXTAREAS
                        if (not(check) or (check and element.get_attribute('value') != (str(v)))):
                            element.clear()
                            element.send_keys(str(v))
                            if (k == 'txtNroCnj'):
                                segredoJusticaAndamentos()
                            camposInseridos = "{}{}: '{}' |".format(camposInseridos, k, v)
                            print('\n{}REG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))
                    sleep(1)
            except Exception as err:
                print('{}{}'.format(self.fileName, err))
                naoInserido[k] = str(v)

        if (naoInserido):
            print('\n{}REG {}: -> NÃO INSERIDOS: {} - "{}"'.format(self.fileName, reg, naoInserido))
            print(naoInserido)

        idNovaPasta = recuperaIdIntegra()
        complementoAdversa = ""

        if (check):
            menuAdversa = self.waitingElement("divMenuProcesso26", 'click', 'id')
        else:
            menuAdversa = self.waitingElement("//*[@id='div_menu17']", 'click')

        if (tipo == 'abertura'):
            if ("parteAdversa" in registro):
                while True: # ABRE A PARTE ADVERSA
                    try:
                        menuAdversa.click()
                        sleep(1.5)
                        try: #checa se há mensagens que bloqueiam o salvamento #TODO   -> CHECAR SE HÁ CAMPOS OBRIGATÓRIOS VAZIOS (ALÉM DESSE)
                            element = self.driver.find_element_by_id('div_txtComarca').is_displayed()
                            self.driver.execute_script("verificarComboNovo('-1','txtComarca','slcComarca');")
                            naoInserido['comarcaNova'] = str(registro['comarcaNova'])
                            sleep(1.5)
                            continue
                        except:
                            break
                    except:
                        pass
                self.checkPopUps()
                complementoAdversa, naoInserido = self.inserirParteAdversa(registro, reg, naoInserido, check=check)
            sleep(1)

        try: # Botão salvar
            countSalvar = 2 if (check) else 1
            for contSalvar in range(countSalvar):
                botaoSalvar = None
                botaoSalvar = self.driver.find_elements_by_id("btnSalvar")[contSalvar]
                botaoSalvar.click()
                print('{}REG {}: -> SALVANDO'.format(self.fileName, reg))
                sleep(1)

                try: # POP-UPS APÓS O SALVAMENTO
                    while True:
                        sleep(1)
                        container = self.waitingElement('popup_container', 'show', 'id')  #primeiro
                        if (container):
                            try:
                                janelaOutrosProcessos = self.driver.find_element_by_class_name("confirm")
                            except:
                                janelaOutrosProcessos = False

                            btnOk = self.waitingElement('popup_ok', 'show', 'id')
                            btnOk.click()
                            sleep(1.5)

                            if (janelaOutrosProcessos):
                                complementoAdversa = "{} --> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA".format(complementoAdversa)
                                print('{}REG {}: -> ADVERSA TEM OUTROS PROCESSOS'.format(self.fileName, reg))
                                continue
                            else:
                                break
                        else:
                            break
                except:
                    pass
                sleep(1.5)

            _checkElemento = self.waitingElement('idDoCliente', 'show', form='class') #aguarda carregamento da página depois de salvar.
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
            message = "{}; NÃO FOI POSSÍVEL A ABERTURA/ATUALIZAÇÃO".format(message)
        return message

    def inserirParteAdversa(self, registro, reg, naoInserido, check=False):
        complementoAdversa = ""
        if (check):
            tabelaAdversa = self.waitingElement('efect-tableParteAdversa', 'click', form='id')
            try:
                tabelaAdversa = tabelaAdversa.find_element_by_tag_name('tr')
            except:
                tabelaAdversa = self.waitingElement('aAdverso', 'click', form='id')
                pass
            sleep(1)
            tabelaAdversa.click()
            sleep(1)

        for k, v in registro['parteAdversa'].items():
            if (check):
                print('\n{}REG {}: -> CHECANDO VALORES: {} - "{}"'.format(self.fileName, reg, k, v))
            try:
                element = self.waitingElement(k, 'click', form='id')
                if (not(check) or (check and element.get_attribute('value').upper() != (str(v.upper())))):
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
                    sleep(1)
                    print('{}\nREG {}: -> ITEM PREENCHIDO : {} - "{}"'.format(self.fileName, reg, k, v))
            except:
                print('{}REG {}: ERRO AO INSERIR PARA {} O VALOR: {}'.format(self.fileName, reg, k, v))
                naoInserido[k] = str(v)
        complementoAdversa = "{}".format(str(registro['parteAdversa']['txtNome']))
        return (complementoAdversa, naoInserido)

    def criaAgendammentos(self, registro, reg, check=False):

        def checkAgendamentos(registro):
            try:
                print('\n{}REG {}: OBTENDO AGENDAMENTOS JÁ REALIZADOS NA PASTA'.format(self.fileName, reg))
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

        print("\n{}REG {}: INICIANDO OS AGENDAMENTOS:".format(self.fileName, reg))
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
                print('{}REG {}: INICIANDO O AGENDAMENTO {}: {}'.format(self.fileName, reg, tipoAgendamento, agendamento))
                sleep(1)
                try:
                    xPathComboDestinatario = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                    elementComboDestinatario = self.waitingElement(xPathComboDestinatario, 'click')
                    elementComboDestinatario.click()
                except:
                    print('{}REG {}: <<< ERRO NO COMBO DESTINATÁRIO - INICIANDO NOVAMENTE >>>'.format(self.fileName, reg))
                    break

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
                print('{}REG {}: SELECIONANDO OS RESPONSÁVEIS'.format(self.fileName, reg))
                listDestinatarios = self.driver.find_elements_by_xpath('//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li')
                while True:
                    try:
                        for item in listDestinatarios:  #itera inputs recuperados, checa e clica
                            if (item.text in registro['slcResponsavel'][tipoAgendamento] ):
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
                        print('{}REG {}: <<< ERRO AO CARREGAR OU SELECIONAR DESTINATÁRIOS >>>'.format(self.fileName, reg))
                        continue
                elementComboDestinatario.click()
                sleep(1)

                # combo TIPO - ABRIR
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button'
                comboTipoAgendamento = self.waitingElement(xPathElement, 'click')
                comboTipoAgendamento.click()
                sleep(1)

                print('{}REG {}: SELECIONANDO O TIPO TIPO DE AGENDAMENTO'.format(self.fileName, reg))
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
                        print('{}REG {}: <<< ERRO AO CARREGAR OU SELECIONAR TIPOS DE AGENDAMENTOS >>>'.format(self.fileName, reg))
                        continue

                # CAMPO QUANDO  - SÓ SE A DATA FOR MAIOR QUE HOJE - se menor ou igual: mantém a data do sistema
                if (datetime.strptime(agendamento, '%d/%m/%Y') > datetime.now()):
                    sleep(1)
                    xPathElement = '//*[@id="txtDataInicialAgendaProcesso1"]'
                    quandoElement = self.waitingElement(xPathElement, 'show')
                    quandoElement.clear()
                    sleep(1)
                    quandoElement.send_keys(agendamento)
                    print('{}REG {}: SELECIONANDO A DATA DO AGENDAMENTO'.format(self.fileName, reg))

                    try: #se o calendário estiver aberto, será fechado
                        sleep(1)
                        self.driver.execute_script("$('#ui-datepicker-div').css('display', 'none');")
                    except:
                        print("{}REG {}: <<< ERRO CALENDÁRIO >>>".format(self.fileName, reg))

                    # COM HORA
                    try:
                        sleep(1)
                        if (tipoAgendamento == 'Audiência'):
                            print('{}REG {}: SELECIONANDO O HORÁRIO DA AUDIÊNCIA'.format(self.fileName, reg))
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
                        print('{}REG {}: A audiência não tem HORARIO definido'.format(self.fileName, reg).upper())
                        pass
                # campo textoAgendamento
                sleep(1)
                print('{}REG {}: PREENCHENDO O TEXTO DO AGENDAMENTO'.format(self.fileName, reg))
                xPathElement = '//*[@id="txtDescricaoAgendaProcesso1"]'
                campoAgendamento = self.waitingElement(xPathElement, 'show')
                campoAgendamento.clear()
                campoAgendamento.send_keys(textoAgendamento)

                # BOTÃO SALVAR
                try:
                    sleep(1)
                    print('{}REG {}: SALVANDO'.format(self.fileName, reg))
                    botaoSalvar = self.waitingElement('//*[@id="btnAgendarSalvar"]', 'click')
                    botaoSalvar.click()
                except:
                    print("{}REG {}: <<< ERRO AO CLICAR NO BOTÃO SALVAR!!!! >>>".format(self.fileName, reg))
                    pass

                sleep(1.5)
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
                    sleep(1.5)
                except:
                    print("{}REG {}: <<< ERRO POPUP SALVAR >>>".format(self.fileName, reg))
                    pass

                try: #remove agendamentos já executados
                    print('{}REG {}: REMOVENDO O AGENDAMENTO EXECUTADO DA LISTA DE NÃO ABERTOS'.format(self.fileName, reg))
                    agendNaoAbertos.remove(tipoAgendamento)
                except:
                    print('{}REG {}: <<< ERRO AgendNaoAbertos: {} >>>'.format(self.fileName, reg, tipoAgendamento))
                break # SE CHEGAR AQUI SEM ERRO - SAI DO LOOPING

        # APÓS O LOOPING
        sleep(1)
        if (agendNaoAbertos):
            for x in agendNaoAbertos:
                messageNaoAbertos = "{}|{}".format(messageNaoAbertos, x)

        if (messageFinal):
            print('{}REG {}: INSERINDO A MENSAGEM FINAL'.format(self.fileName, reg))
            message = "{};{}".format(message, messageFinal)

        if (messageNaoAbertos):
            print('{}REG {}: INSERINDO OS AGENDAMENTOS NÃO ABERTOS'.format(self.fileName, reg))
            message = "{};{}".format(message, messageNaoAbertos)
        print('{}REG {}: FINALIZOU TODOS OS AGENDAMENTOS'.format(self.fileName, reg))

        return message

    def removeAgendamentos(self, reg): # EXECUTA QUANDO ESTÁ EM MODO DE TESTE
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



#TODO SE DER ERRO OU FALHA NA VERIFICAÇÃO -> DAR UM CONTINUE E REINICIAR O WEBDRIVER (SE ISSO FOR O CASO)

#TODO  CRIAR UM GATILHO - PARA QUANDO A SESSÃO EXPIRAR OU O CHROME FECHAR - PRA VOLTAR PARA O ROBO MONITOR
#TODO MELHORAR OS LOGS - CAMPO SE EXISTE OUTROS PROCESSOS (P/MARCAR)   ERROS NÃO INSERIDOS PARA O FINAL (NOVO NOME: ITENS QUE NÃO FOI POSSÍVEL REALIZAR O PREENCHIMENTO)
#TODO PENSAR NA VOLTA DO pid PARA CHECAR NAS EXECUÇÕES SE O WEBDRIVER NÃO FOI FINALIZADO E RECOMEÇAR CASO TENHA SIDO.
#TODO ENVIAR OS ITENS PARA PESQUISA - CASO A PASTA EXISTA -> É FEITO O LOOPING SEM ATUALIZAR A PÁGINA