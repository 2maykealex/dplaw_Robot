# coding=utf-8
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import sleep
from os import mkdir
from os import remove
from os import path as pathFolder
from os import getpid
from shutil import move
from locale import format_string
from integra_functions import IntegraFunctions
import basic_functions #uso completo nesse módulo

class Abertura (object):
    def __init__(self):
        self.integra = IntegraFunctions()

    def incluirProcesso(self, df, registro):
        self.integra.checkPopUps()

        element = self.integra.waitInstance(self.integra.driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
        element.click()
        naoInserido = {}

        # Grupo internodd
        if (str(df['gpProcesso'])):
            try:
                element = self.integra.waitInstance(self.integra.driver, "//*[@id='slcGrupo']", 1, 'show')
                select = self.selenium.select(element)
                select.select_by_visible_text(str(df['gpProcesso']))
            except:
                naoInserido['gpProcesso'] = str(df['gpProcesso'])
        else:
            naoInserido['gpProcesso'] = ''

        sleep(0.5)

        #Numero do CNJ
        if (df['cnj'] != ''):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="txtNroCnj"]', 1, 'show', 'xpath')
                element.clear()
                element.send_keys(str(df['cnj']))

                # Segredo de Justiça  #por padrão, será marcado não
                element = self.integra.driver.find_element_by_id("segredoJusticaN")
                self.integra.driver.execute_script("arguments[0].click();", element)

                sleep(0.5)
                element = self.integra.driver.find_element_by_id("capturarAndamentosS")
                self.integra.driver.execute_script("arguments[0].click();", element)
            except:
                naoInserido['cnj'] = str(df['cnj'])
        else:
            naoInserido['cnj'] = ''

        sleep(0.5)

        #Numero do Processo
        if (str(df['numProcesso']) != ''):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="txtNroProcesso"]', 1, 'show', 'xpath')
                element.clear()
                element.send_keys(str(df['numProcesso']))
            except:
                naoInserido['numProcesso'] = str(df['numProcesso'])
        else:
            naoInserido['numProcesso'] = ''

        sleep(0.5)

        # Status
        if (str(df['statusProcessual'])):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="slcStatusProcessual"]', 1, 'show')
                select = self.selenium.select(element)
                select.select_by_visible_text(str(df['statusProcessual']))
            except:
                naoInserido['statusProcessual'] = str(df['statusProcessual'])
        else:
            naoInserido['statusProcessual'] = ''

        sleep(0.5)

        ###################################### 2ª COLUNA DA PÁGINA ######################################
        # Pasta
        if (str(df['pasta'])):
            try:
                self.integra.driver.execute_script("document.getElementById('txtPasta').value='{}' ".format(str(df['pasta'])) )
            except:
                naoInserido['pasta'] = str(df['pasta'])
        else:
            naoInserido['pasta'] = ''

        sleep(0.5)

        # Local trâmite - Campo 1
        if (df['localTr'] != ''):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="slcNumeroVara"]', 1, 'show')
                select = self.selenium.select(element)
                select.select_by_visible_text(str(df['localTr']))
            except:
                naoInserido['localTr'] = str(df['localTr'])
        else:
            naoInserido['localTr'] = ''

        sleep(0.5)

        # Local trâmite - Campo 2
        if (str(df['localTramite']) != ""):
            localTramite = str(df['localTramite'])
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="slcLocalTramite"]', 1, 'show')
                sleep(1)
                select = self.selenium.select(element)

                try:
                    select.select_by_visible_text(localTramite)
                except:
                    try:
                        select.select_by_visible_text(localTramite.title())
                    except:
                        try:
                            select.select_by_visible_text(localTramite.lower())
                        except:
                            try:
                                select.select_by_visible_text(localTramite.lower().capitalize())   #usado sem Tratamento para cair except externo
                            except:
                                elemCadastro = self.integra.waitInstance(self.integra.driver, "//*[@id='slcLocalTramite']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                                elemCadastro.click()
                                self.integra.driver.execute_script("document.getElementById('txtLocalTramite').value='{}' ".format(str(localTramite)))
                sleep(1)
            except:
                naoInserido['localTramite'] = localTramite
        else:
            naoInserido['localTramite'] = ''

        sleep(0.5)

        # #PARA ATUALIZAR OS DADOS
        # logAtualizaPromad = os.getcwd() + "\\logs\\_Locais.txt"
        # basic_functions.createLog(logAtualizaPromad)
        # for elemento in element.find_elements_by_tag_name('option'):
        #     texto = "{}\n".format(elemento.text)
        #     basic_functions.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

        # Comarca
        comarcaExiste = False
        comarcaSelecionada = False
        if (str(df['comarca']) != ""):
            comarca = str(df['comarca'])
            comarcaExiste = True
            comarcaSelecionada = True
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="slcComarca"]', 1, 'show')
                sleep(1)
                select = self.selenium.select(element)

                try:
                    select.select_by_visible_text(comarca)
                except:
                    try:
                        select.select_by_visible_text(comarca.title())
                    except:
                        try:
                            select.select_by_visible_text(comarca.lower())
                        except:
                            select.select_by_visible_text(comarca.lower().capitalize())   #usado sem Tratamento para cair except externo
                sleep(1)
            except:
                comarcaSelecionada = False
        else:
            naoInserido['comarca'] = ''

        # Nova Comarca somente se existir uma no registro e não foi possível fazer a seleção no combo
        if (comarcaExiste == True and comarcaSelecionada == False):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="slcComarca"]', 1, 'show')
                sleep(1)
                select = self.selenium.select(element)
                select.select_by_visible_text("--Cadastrar Novo Item--")
                sleep(1)

                element = self.integra.waitInstance(self.integra.driver, '//*[@id="txtComarca"]', 1, 'show')
                element.send_keys(str(df['comarca']))
                sleep(1)
            except:
                naoInserido['comarca'] = str(df['comarca'])

            # #PARA ATUALIZAR OS DADOS
            # from os import getcwd
            # logAtualizaPromad = getcwd() + "\\logs\\_Comarcas.txt"
            # basic_functions.createLog(logAtualizaPromad)
            # for elemento in element.find_elements_by_tag_name('option'):
            #     texto = "{}\n".format(elemento.text)
            #     basic_functions.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

        # UF
        if (str(df['uf'])):
            try:
                element = self.integra.waitInstance(self.integra.driver, '//*[@id="txtUf"]', 1, 'show')
                select = self.selenium.select(element)
                select.select_by_visible_text(str(df['uf']))
            except:
                naoInserido['uf'] = str(df['uf'])
        else:
            naoInserido['uf'] = ''

        sleep(0.5)

        try:
            element = self.integra.waitInstance(self.integra.driver, 'slcLocalizador', 1, 'show', 'id')
            select = self.selenium.select(element)
            select.select_by_visible_text(str(df['localizador']))
        except:
            naoInserido['localizador'] = str(df['localizador'])

        # RESPONSÁVEL
        if (df['responsavel']):   #condição para evitar percorrer a lista se for ""
            try:
                self.integra.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

                comboResponsavel = self.integra.waitInstance(self.integra.driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 1, 'show')
                comboResponsavel.click()  # clica e abre as opções

                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                xInputs = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li'
                listInputs = self.integra.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                # CARREGA LISTA DE RESPONSÁVEIS
                y = 1
                totalResp = len(df['responsavel'])
                countResp = 0
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text in df['responsavel']):
                        xPathItem = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li[{}]'.format(y)
                        element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                        element.click()
                        sleep(1)
                        countResp = countResp + 1
                        if (countResp == totalResp):
                            break
                    y = y + 1

                comboResponsavel.click() # clica para fechar as opções do combo
                self.integra.driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
            except:
                naoInserido['responsavel'] = str(df['responsavel'])
        else:
            naoInserido['responsavel'] = ''

        sleep(0.5)

        # Data da Contratação
        if (str(df['dataContratacao'])):
            try:
                self.integra.driver.execute_script("document.getElementById('txtDataContratacao').value='{}' ".format(str(df['dataContratacao'])))
            except:
                naoInserido['dataContratacao'] = str(df['dataContratacao'])
        else:
            naoInserido['dataContratacao'] = ''

        sleep(0.5)

        # Valor da Causa
        if (str(df['vCausa'])):
            try:
                self.integra.driver.execute_script("document.getElementById('txtValorCausa').value='{}' ".format(str(df['vCausa'])) )
            except:
                naoInserido['vCausa'] = str(df['vCausa'])
        else:
            naoInserido['vCausa'] = ''

        sleep(0.5)

        #Obtém o ID do PROMAD da nova pasta a ser aberta
        try:
            element = self.integra.waitInstance(self.integra.driver, "idDoProcesso", 1, 'show', 'class')
            idNovaPasta = element.get_attribute("innerHTML")
            idNovaPasta = idNovaPasta[14:].strip()
        except:
            naoInserido['idDoProcesso'] = 'Não recuperado'

        print("REG {}: NOVA PASTA ABERTA: {}".format(registro, idNovaPasta))

        # Abre a aba Parte Adversa
        try:
            element = self.integra.waitInstance(self.integra.driver, "//*[@id='div_menu17']", 1, 'show')
            element.click()
            sleep(2)

            try:
                element = self.integra.driver.find_element_by_id('div_txtComarca').is_displayed()
                self.integra.driver.execute_script("verificarComboNovo('-1','txtComarca','slcComarca');")
                naoInserido['comarcaNova'] = str(df['comarcaNova'])

                # TENTANDO NOVAMENTE ABRIR PARTE ADVERSA
                element = self.integra.waitInstance(self.integra.driver, "//*[@id='div_menu17']", 1, 'show')
                element.click()
                sleep(2)
            except:
                print('erro ao redirecionar para a parte adversa')
                pass

            sleep(0.5)
            self.integra.checkPopUps()

            complemento = ""
            # Parte Adversa
            if (str(df['adversa'])):
                try:
                    element = self.integra.waitInstance(self.integra.driver, '//*[@id="txtNome"]', 1, 'show')
                    element.send_keys(str(df['adversa']))
                    print("REG {}: REGISTRADO A PARTE ADVERSA: {}".format(registro, str(df['adversa'])))
                    complemento = "REG {}: PARTE ADVERSA: {}".format(registro, str(df['adversa']))
                except:
                    naoInserido['adversa'] = str(df['adversa'])
            else:
                naoInserido['adversa'] = ''

            sleep(1)

            # Botão salvar
            element = self.integra.waitInstance(self.integra.driver, '//*[@id="btnSalvar"]', 1, 'show')
            element.click()

            try:  #popup Ok em que a parte Adversa já possui outros processos.
                sleep(1.5)
                element = self.integra.driver.find_element_by_id("popup_ok")
                self.integra.driver.execute_script("arguments[0].click();", element)
                complemento = "{} -> TEM OUTROS PROCESSOS REGISTRADOS NO SISTEMA!\n".format(complemento)
                sleep(0.5)
            except:
                complemento = "{}\n".format(complemento)
                print(complemento)

            if (naoInserido):
                complemento = '{}REG {}: NÃO FORAM INSERIDOS: '.format(complemento, registro)
                for k, v in naoInserido.items():
                    complemento = '{} {}: "{}" | '.format(complemento, k, v)

            hoje = "%s" % (strftime("%d-%m-%Y"))
            hora = strftime("%H:%M:%S")
            horaStr = hora.replace(':', '-')

            message = "REG {}: {}__{}".format(registro, hoje, horaStr)  #Insere a primeira linha do registro no log
            message = "{}\nREG {}: A PASTA '{}' FOI CRIADA!\nREG {}: ID PROMAD: '{}'.\n{}".format(message, registro, str(df['pasta']), registro, idNovaPasta, complemento)
        except:
            message = "NÃO FOI POSSÍVEL ABRIR A PASTA {}".format(str(df['pasta']))

        sleep(0.5)
        return message

    def criarAgendamentos(self, dataAudiencia, dataAberturaPasta, horaAudienciaFormatada, sigla, responsavel, pasta, registro, dataCiencia, agendFotocopia, message):
        # try:
        refazAgendamento = 0
        print("REG {}: INICIANDO OS AGENDAMENTOS:".format(registro))
        while (True):
            try:
                element = self.integra.waitInstance(self.integra.driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu
                self.integra.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
                sleep(1)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                elementComboDestinatario = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                if (elementComboDestinatario == False):
                    print("erro: Elemento da página não foi encontrado!")
                break
            except:
                print("erro de redirecionamento")
        self.integra.checkPopUps()

        if (sigla =='BRA'):
            respCiencia = 'cbradesco'
        elif (sigla == 'BV'):
            respCiencia = 'CBV'

        agendNaoAbertos = []

        qtdAgendamentos = 3
        if (dataAudiencia != ""):
            agendNaoAbertos.append("Audiência")

        agendNaoAbertos.append("Ciencia de novo processo")
        agendNaoAbertos.append("Anexar")

        if (agendFotocopia == "1"):
            qtdAgendamentos = 4
            agendNaoAbertos.append("Fotocópia")

        message = "{}\nREG {}: Agendamentos Criados: ".format(message, registro)

        complementoAgendamento = ""
        for x in range(qtdAgendamentos):
            while (True):
                tipoAgendamento = ""
                agendamento = ""

                # Elemento recebido no início da função
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                elementComboDestinatario = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'click')
                elementComboDestinatario.click()

                try:
                    if (x == 0):   #tipo audiencia
                        if (dataAudiencia != ""):
                            tipoAgendamento = 'Audiência'
                            appointmentDate = dataAudiencia
                            data = "{}/{}/{}".format(str(appointmentDate.day), str(appointmentDate.month), str(appointmentDate.year))
                            appointmentDate = datetime.strptime("{}".format(data), "%d/%m/%Y")
                            appointmentDate = format(appointmentDate, "%d/%m/%Y")

                            if (horaAudienciaFormatada != "00:00"):
                                agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, str(appointmentDate), horaAudienciaFormatada)
                            else:
                                agendamento = "{} - Audiência designada para dia {}".format(sigla, str(appointmentDate))

                            messageFinal = "REG {}: {}".format(registro, agendamento.split('-')[1].strip().upper())

                            #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                            xInputs = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li'
                            listInputs = self.integra.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                            totalResp = len(responsavel)
                            countResp = 0
                            y = 1
                            for item in listInputs:  #itera inputs recuperados, checa e clica
                                if (item.text == 'GST' or item.text in responsavel ):
                                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                    element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                                    element.click()
                                    sleep(1)
                                    countResp = countResp + 1
                                    if (countResp == (totalResp + 1)):
                                        break
                                y = y + 1
                            sleep(1)
                        else:
                            messageFinal = "REG {}: Audiência NÃO está marcada!".format(registro)
                            complementoAgendamento = " A audiência não foi marcada."
                            elementComboDestinatario.click() #se não houver audiência, pula para o próximo item e fecha o combo destinatário
                            break
                except:
                    print("erro X=0")
                    continue

                try:
                    if (x == 1): #tipo Ciencia de novo processo
                        tipoAgendamento = 'Ciencia de novo processo'
                        dataAbPasta = datetime.strptime(dataCiencia, "%d/%m/%Y")
                        dataIncrementada = dataAbPasta.date()
                        data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                        appointmentDate = datetime.strptime("{}".format(data), "%d/%m/%Y")
                        appointmentDate = format(appointmentDate, "%d/%m/%Y")
                        agendamento = "{} - Certificar abertura, risco e promover agendamentos.{}".format(sigla, complementoAgendamento)

                        #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                        xInputs = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li'
                        listInputs = self.integra.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                        # respons. pelo cliente
                        y = 1
                        for item in listInputs:  #itera inputs recuperados, checa e clica
                            if (item.text == respCiencia):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                                element.click()
                                sleep(1)
                                break
                            y = y + 1
                except:
                    print("erro X=1")

                try:
                    if (x == 2): #tipo Anexar
                        tipoAgendamento = 'Anexar'
                        dataAbPasta = datetime.strptime(dataCiencia, "%d/%m/%Y")
                        dataIncrementada = dataAbPasta.date()
                        data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                        appointmentDate = datetime.strptime("{}".format(data), "%d/%m/%Y")
                        appointmentDate = format(appointmentDate, "%d/%m/%Y")
                        agendamento = "ANEXAR"

                        #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                        xInputs = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li'
                        listInputs = self.integra.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                        totalResp = 2
                        countResp = 0
                        y = 1
                        for item in listInputs:  #itera inputs recuperados, checa e clica
                            if (item.text == 'ESTAGBRA' or item.text == respCiencia):
                                xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                                element.click()
                                sleep(1)
                                countResp = countResp + 1
                                if (countResp == totalResp):
                                    break
                            y = y + 1
                except:
                    print("erro X=2")

                try:
                    if (x == 3): #tipo Fotocópia
                        if (agendFotocopia == "1"):
                            tipoAgendamento = 'Fotocópia'
                            dataAbPasta = datetime.strptime(dataCiencia, "%d/%m/%Y")
                            dataIncrementada = dataAbPasta.date()
                            data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                            appointmentDate = datetime.strptime("{}".format(data), "%d/%m/%Y")
                            appointmentDate = format(appointmentDate, "%d/%m/%Y")
                            agendamento = "Fotocópia integral"

                            #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                            xInputs = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li'
                            listInputs = self.integra.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                            # GST e OPERAÇÕES
                            y = 1
                            found = 0
                            for item in listInputs:  #itera inputs recuperados, checa e clica
                                if (item.text == 'GST' or item.text == 'operacoes'):
                                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(y)
                                    element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                                    element.click()
                                    found = found + 1
                                    sleep(1)
                                if (found >= 2):
                                    break
                                y = y + 1
                        else:
                            break
                except:
                    print("erro X=3")

                try:
                    sleep(1)
                    elementComboDestinatario.click() #destinatário
                    sleep(1)

                    # combo TIPO - ABRIR
                    xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/button'
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'click')
                    element.click()
                    sleep(1)

                    # # TIPO DE AGENDAMENTO  -  recupera lista de TIPOS cadastrados no PROMAD
                    xTiposAgendamentos = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li'
                    listTiposAgendamentos = self.integra.driver.find_elements_by_xpath(xTiposAgendamentos) #recupera os inputs abaixo dessa tag

                    y = 1
                    for item in listTiposAgendamentos:  #itera inputs recuperados, checa e clica
                        if (item.text == tipoAgendamento):
                            xPathItem = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(y)
                            element = self.integra.waitInstance(self.integra.driver, xPathItem, 1, 'click')
                            element.click()
                            sleep(1)
                            break
                        y = y + 1

                    # CAMPO QUANDO
                    sleep(1)
                    xPathElement = '//*[@id="txtDataInicialAgendaProcesso1"]'
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                    element.clear()
                    sleep(1)
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                    element.send_keys(appointmentDate)
                    sleep(1)

                    try: #se o calendário estiver aberto, será fechado
                        self.integra.driver.execute_script("$('#ui-datepicker-div').css('display', 'none');") #torna elemento invisível novamente
                    except:
                        print("ERRO CALENDÁRIO")
                        pass

                    if (dataAudiencia != ""):
                        if (x == 0):
                            # com HORA
                            sleep(1)
                            xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso1"]'
                            element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'click')
                            sleep(1)
                            element.click()

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraInicialAgendaProcesso1"]'
                            element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'click')
                            element.clear()

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraInicialAgendaProcesso1"]'
                            element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                            element.send_keys(horaAudienciaFormatada)

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraFinalAgendaProcesso1"]'
                            element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                            element.clear()

                            sleep(1)
                            xPathElement = '//*[@id="txtHoraFinalAgendaProcesso1"]'
                            element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')

                            sleep(1)
                            element.send_keys(horaAudienciaFormatada)
                    else:
                        pass

                    # campo agendamento
                    sleep(1)
                    xPathElement = '//*[@id="txtDescricaoAgendaProcesso1"]'
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                    element.clear()
                    element.send_keys(agendamento)

                    # campo resumo
                    sleep(1)
                    xPathElement = '//*[@id="txtTituloAgendaProcesso1"]'
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                    element.clear()
                    sleep(1)
                    xPathElement = '//*[@id="txtTituloAgendaProcesso1"]'
                    element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                    element.send_keys(agendamento[:30])
                except:
                    print("erro de preenchimento nos campos")

                try:
                    element = self.integra.waitInstance(self.integra.driver, '//*[@id="btnAgendarSalvar"]', 1, 'click')
                    element.click()
                    sleep(2)
                except:
                    print("erro ao clicar no SALVAR!!!!")
                    pass

                try: # CHECA SE FALTOU INFORMAÇÕES NO INPUT
                    element = self.integra.waitInstance(self.integra.driver, 'idCampoValidateAgendar', 1, 'show', 'id')
                    if (element.text): # Se faltar informações nos inputs, dá um refresh na página e recomeça
                        element = self.integra.waitInstance(self.integra.driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu
                        self.integra.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos
                        xPathElement = '//*[@id="tableAgendamentoCadastroProcesso1"]/tbody/tr[3]/td[1]/button'
                        element = self.integra.waitInstance(self.integra.driver, xPathElement, 1, 'show')
                        if (element == False):
                            print("erro: Elemento da página não foi encontrado!")
                        self.integra.checkPopUps()
                        sleep(2)
                        refazAgendamento = refazAgendamento + 1
                        if (refazAgendamento <= 3): # limita a 3 tentativas para o agendamento
                            continue #volta ao While TRUE e recomeça os preenchimentos
                        else:
                            refazAgendamento = 0
                            break
                except:
                    print("erro INFORMAÇÕES NO INPUT")
                    pass

                try: #Clicar no PopUp - Deseja salvar
                    sleep(2)
                    element = self.integra.waitInstance(self.integra.driver, '//*[@id="popup_ok"]', 1, 'click')
                    element.click()
                    message = "{} |{}".format(message, tipoAgendamento) # add à message o tipo de agendamento REALIZADO.
                    print ("REG {}: CRIADO O AGENDAMENTO: |{}".format(registro, tipoAgendamento))
                    sleep(2)
                except:
                    print("erro POPUP SALVAR")
                    pass

                try: #remove agendamentos já executados
                    agendNaoAbertremove(tipoAgendamento)
                except:
                    print('erro AgendNaoAbertos: {}'.format(tipoAgendamento))
                break #sai do While TRUE

        # APÓS O LOOPING
        if (agendNaoAbertos):
            message = "{}\nREG {}: AGENDAMENTOS NÃO ABERTOS!: ".format(message, registro)
            for x in agendNaoAbertos:
                message = "{} |{}".format(message, x)

        if (messageFinal):
            message = "{}\n{}".format(message, messageFinal)
        basic_functions.createLog(self.logFile, "{}".format(message.upper()))

    def removeAgendamentos(self): # EXECUTA QUANDO ESTÁ EM MODO DE TESTE
        trash = '/html/body/div[13]/table/tbody/tr[2]/td/form/div/fieldset/div[2]/table[2]/tbody/tr/td/fieldset/div[2]/div/table/tbody/tr/td[1]/div'
        while True:
            try:
                trash = self.integra.waitInstance(self.integra.driver, trash, 2, 'click')
                trash.click()
                sleep(1)
                botaoPopup = self.integra.waitInstance(self.integra.driver, 'popup_ok', 2, 'click', 'id')
                botaoPopup.click()
            except:
                break
        print('OS AGENDAMENTOS FORAM EXCLUÍDOS COM SUCESSO!')

    def abrePasta(self, arquivoAbrirPasta, item = 1, extensao ="xlsx", path=""):
        dfExcel = basic_functions.abreArquivo(arquivoAbrirPasta, extensao, path=path)
        count = dfExcel.number_of_rows()-1

        cliente = ''
        cliente = dfExcel[1, 12]

        try:
            searchClient, elemPesquisado = self.integra.pesquisarCliente(cliente, 'cliente')
        except:
            return False

        if (searchClient):
            total = (count if (item==1) else ((count - item)+1)) # se não rodou, Total=Count||Sse rodou (item>1 -> Subtrai item de count e add 1)
            print ('REG {}: TOTAL DE REGISTROS A EXECUTAR: {}'.format(item, total))

            elemPesquisado.click()
            urlPage = self.integra.driver.current_url

            while (item <= count):
                df = {}

                df['pasta']            = dfExcel[item, 0]
                df['adversa']          = dfExcel[item, 1].strip()
                dataContratacao        = dfExcel[item, 2]
                try:
                    dataContratacao        = str(dataContratacao.strftime("%d/%m/%Y"))
                except:
                    pass
                df['dataContratacao']  = dataContratacao
                numProcesso = dfExcel[item, 4]

                try:
                    numProcesso = numProcesso.replace('.', '')
                    numProcesso = numProcesso.replace('-', '')
                except:
                    pass

                num = len(numProcesso)

                if (num > 20):   #se maior que 20, obter até o caracter n.º 20
                    numProcesso = numProcesso[:20]
                elif (num < 20): # se menor que 20, incrementar ZEROS no início até que complete 20 caracteres
                    qtdZero = 20 - len(numProcesso)
                    for _x in range(qtdZero):
                        numProcesso = "0{}".format(numProcesso)

                numProcesso = '{}-{}.{}.{}.{}.{}'.format(numProcesso[:7], numProcesso[7:9], numProcesso[9:13], numProcesso[13:14], numProcesso[14:16], numProcesso[16:20])
                if (numProcesso == '-....'):
                    numProcesso = ''
                df['numProcesso']  = numProcesso
                df['cnj']          = numProcesso
                df['gpProcesso']   = dfExcel[item, 5].strip()
                df['localTr']      = dfExcel[item, 6]
                df['localTramite'] = dfExcel[item, 7].strip()
                df['comarca']      = dfExcel[item, 8].strip()
                df['uf']           = dfExcel[item, 9].strip()
                try:
                    valorCausa     = format_string("%1.2f", dfExcel[item, 10].strip() , 0)
                    df['vCausa']   = valorCausa.replace('.',',')
                except:
                    df['vCausa'] = "0"

                df['statusProcessual'] = dfExcel[item, 11]

                if (basic_functions.checkIfTest):  #se for teste
                    df['razaoSocial']  = "Cliente teste"
                    df['gpCliente']    = "Grupo Teste"
                else:
                    df['razaoSocial']  = dfExcel[item, 12]
                    df['gpCliente']    = dfExcel[item, 13]

                responsavel = dfExcel[item, 14].split(';')

                df['responsavel']  = responsavel
                df['sigla']        = dfExcel[item, 15].strip()

                try:
                    df['dataAudiencia'] = dfExcel[item, 16]
                except:
                    df['dataAudiencia'] = ""

                try:
                    if (dfExcel[item, 17]):
                        df['horaAudiencia'] = dfExcel[item, 17]
                        horaAudiencia = df['horaAudiencia']
                    else:
                        df['horaAudiencia'] = "00:00"
                        horaAudiencia = df['horaAudiencia']
                except:
                    df['horaAudiencia'] = "00:00"
                    horaAudiencia = df['horaAudiencia']

                df['dataCiencia'] = dfExcel[item, 18]
                df['agendFotocopia'] = dfExcel[item, 19]
                df['localizador'] = dfExcel[item, 20]

                sleep(1)

                try:
                    isTest = basic_functions.checkIfTest()
                    if (isTest):
                        searchFolder = False
                    else:
                        searchFolder, _element = self.integra.pesquisarCliente(df['pasta'], 'pasta')
                except:
                    print('Não foi possível realizar uma busca')
                    return False

                if (not(searchFolder)):   # se não foi encontrado no sistema, será inserido
                    try:
                        self.integra.driver.get(urlPage)
                        sleep(1)
                        message = self.incluirProcesso(df, item)
                        basic_functions.createLog(self.logFile, "\nREG {}: =================================================================\n".format(item))
                        basic_functions.createLog(self.logFile, "{}".format(message.upper()))
                        message = ""
                    except:
                        print('Erro ao incluir a pasta: {}!'.format(df['pasta']))
                        return False

                    try: #checa se redirecionamento ocorreu
                        self.integra.waitInstance(self.integra.driver, "//*[@id='slcGrupo']", 1, 'show')
                    except:
                        print('Erro ao incluir a pasta: {}!'.format(df['pasta']))
                        return False

                    if (df['responsavel']):
                        self.criarAgendamentos(df['dataAudiencia'], df['dataContratacao'], horaAudiencia, df['sigla'], df['responsavel'], df['pasta'], item, df['dataCiencia'], df['agendFotocopia'], message)
                        if (isTest):
                            self.removeAgendamentos()
                    else:
                        message = "\nREG {}: NÃO FO POSSÍVEL CRIAR OS AGENDAMENTOS - NÃO EXISTEM RESPONSAVEIS! |".format(item)
                        basic_functions.createLog(self.logFile, "{}".format(message.upper()))
                else:
                    basic_functions.createLog(self.logFile, "\nREG {}: A pasta '{}' já existe no sistema! Favor verificar!".format(item, df['pasta']))

                if (item < count):
                    print ('REG {}: FALTAM {} REGISTROS A EXECUTAR DO ARQUIVO "{}.{}"\n'.format(item, count-item, arquivoAbrirPasta, extensao))

                item = item + 1

            if (not(isTest)):
                basic_functions.createLog(self.logFile, '\nFIM')
            return True
        else:
            return False

    def controle(self, file, path):
        pidNumber = str(getpid())
        print("\npID: {}".format(pidNumber))

        infoLog = "EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG

        logsPath = path + "\\logs"
        pathExecutados = path + "\\arquivos_executados"

        if (pathFolder.exists(pathExecutados) == False):
            mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado -

        if (pathFolder.exists(logsPath) == False):
            mkdir(logsPath)   # Se o diretório Abertura_pastas não existir, será criado -

        driverIniciado = False
        abreNovaPasta = None
        login, password = basic_functions.checkLogin()

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        arquivoAbrirPasta = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(arquivoAbrirPasta)

        abreWebDriver = None
        if (pathFolder.isfile(self.logFile)):    # se existir o log em andamento
            registro = basic_functions.checkEndFile(self.logFile)

            if (registro == "FIM"): # checa se no registro do arquivo encerra a operação
                print('O arquivo {}.xlsx já foi executado!\n'.format(arquivoAbrirPasta.upper()))
                abreNovaPasta = True # Avança no looping apagando o arquivo existente

            else: # continua o preenchimento do log já existente a partir do último registro lançado
                registro = int(registro.split(":")[0][4:]) + 1     #obtém o valor do último registro lançado (+1) para dar continuidade
                if (driverIniciado == False):
                    driverIniciado = True
                    print("\nINICIANDO WebDriver")
                    basic_functions.createPID(arquivoAbrirPasta.upper(), pidNumber)
                    abreWebDriver = self.integra.acessToIntegra(login, password)
                if (abreWebDriver):
                    abreNovaPasta = self.abrePasta(arquivoAbrirPasta, registro, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    self.integra.driver.quit()
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True
                basic_functions.createPID(arquivoAbrirPasta.upper(), pidNumber)
                abreWebDriver = self.integra.acessToIntegra(login, password)
            if (abreWebDriver):
                abreNovaPasta = self.abrePasta(arquivoAbrirPasta, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.integra.driver.quit()
                remove("{}\\{}".format(path, infoLog))
                # break

        if (abreNovaPasta):
            if (file[0] != ""):
                #APAGA O ARQUIVO .TXT
                remove("{}\\{}".format(path, infoLog))
                fileExecuted = pathExecutados + "\\{}.{}".format(arquivoAbrirPasta, extensao)

                #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                if (pathFolder.isfile(fileExecuted)):
                    remove(fileExecuted)

                move("{}\\{}.{}".format(path, arquivoAbrirPasta, extensao), pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
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