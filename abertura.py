# coding=utf-8
import datetime
from datetime import date
from datetime import timedelta
import locale
import time
from time import strftime
import glob
import sys
import os
import shutil
import robot_functions as rf

class Abertura (object):
    def incluirProcesso(self, df, registro):
        # incluindo processo
        print("incluindo processo")
        rf.checkPopUps(self.driver)

        element = rf.waitinstance(self.driver, '//*[@id="frmProcesso"]/table/tbody/tr[2]/td/div[1]', 1, 'show')
        element.click()

        naoInserido = {}

        # Grupo internodd
        if (str(df['gpProcesso'])):
            try:
                element = rf.waitinstance(self.driver, "//*[@id='slcGrupo']", 1, 'show')
                select = rf.Select(element)
                select.select_by_visible_text(str(df['gpProcesso']))
            except:
                naoInserido['gpProcesso'] = str(df['gpProcesso'])
        else:
            naoInserido['gpProcesso'] = 'Vazio'

        time.sleep(0.5)

        #Numero do CNJ
        if (df['cnj'] != ''):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="txtNroCnj"]', 1, 'show', 'xpath')
                element.clear()
                element.send_keys(str(df['cnj']))

                # Segredo de Justiça  #por padrão, será marcado não
                element = self.driver.find_element_by_id("segredoJusticaN")
                self.driver.execute_script("arguments[0].click();", element)

                time.sleep(0.5)
                element = self.driver.find_element_by_id("capturarAndamentosS")
                self.driver.execute_script("arguments[0].click();", element)
            except:
                naoInserido['cnj'] = str(df['cnj'])
        else:
            naoInserido['cnj'] = 'Vazio'

        time.sleep(0.5)

        #Numero do Processo
        if (str(df['numProcesso']) != ''):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="txtNroProcesso"]', 1, 'show', 'xpath')
                element.clear()
                element.send_keys(str(df['numProcesso']))
            except:
                naoInserido['numProcesso'] = str(df['numProcesso'])
        else:
            naoInserido['numProcesso'] = 'vazio'

        time.sleep(0.5)

        # Status
        if (str(df['statusProcessual'])):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="slcStatusProcessual"]', 1, 'show')
                select = rf.Select(element)
                select.select_by_visible_text(str(df['statusProcessual']))
            except:
                naoInserido['statusProcessual'] = str(df['statusProcessual'])
        else:
            naoInserido['statusProcessual'] = 'Vazio'

        time.sleep(0.5)

        ###################################### 2ª COLUNA DA PÁGINA ######################################
        # Pasta
        if (str(df['pasta'])):
            try:
                self.driver.execute_script("document.getElementById('txtPasta').value='{}' ".format(str(df['pasta'])) )
            except:
                naoInserido['pasta'] = str(df['pasta'])
        else:
            naoInserido['pasta'] = 'Vazio'
            
        time.sleep(0.5)

        # Local trâmite - Campo 1
        if (df['localTr'] != ''):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="slcNumeroVara"]', 1, 'show')
                select = rf.Select(element)
                select.select_by_visible_text(str(df['localTr']))
            except:
                naoInserido['localTr'] = str(df['localTr'])
        else:
            naoInserido['localTr'] = 'Vazio'

        time.sleep(0.5)

        # Local trâmite - Campo 2
        if (str(df['localTramite']) != ""):
            localTramite = str(df['localTramite'])
            try:
                element = rf.waitinstance(self.driver, '//*[@id="slcLocalTramite"]', 1, 'show')
                time.sleep(1)
                select = rf.Select(element)

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
                                elemCadastro = rf.waitinstance(self.driver, "//*[@id='slcLocalTramite']/option[2]", 1, 'click') # CADASTRAR NOVO ITEM
                                elemCadastro.click()
                                self.driver.execute_script("document.getElementById('txtLocalTramite').value='{}' ".format(str(localTramite)))
                time.sleep(1)
            except:
                naoInserido['localTramite'] = localTramite
        else:
            naoInserido['localTramite'] = 'Vazio'

        time.sleep(0.5)

        # #PARA ATUALIZAR OS DADOS
        # logAtualizaPromad = os.getcwd() + "\\logs\\_Locais.txt"
        # rf.createLog(logAtualizaPromad)
        # for elemento in element.find_elements_by_tag_name('option'):
        #     texto = "{}\n".format(elemento.text)
        #     rf.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

        # Comarca
        comarcaExiste = False
        comarcaSelecionada = False
        if (str(df['comarca']) != ""):
            comarca = str(df['comarca'])
            comarcaExiste = True
            comarcaSelecionada = True
            try:
                element = rf.waitinstance(self.driver, '//*[@id="slcComarca"]', 1, 'show')
                time.sleep(1)
                select = rf.Select(element)

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
                time.sleep(1)
            except:
                comarcaSelecionada = False
        else:
            naoInserido['comarca'] = 'Vazio'

        # Nova Comarca somente se existir uma no registro e não foi possível fazer a seleção no combo 
        if (comarcaExiste == True and comarcaSelecionada == False):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="slcComarca"]', 1, 'show')
                time.sleep(1)
                select = rf.Select(element)
                select.select_by_visible_text("--Cadastrar Novo Item--")
                time.sleep(1)

                element = rf.waitinstance(self.driver, '//*[@id="txtComarca"]', 1, 'show')
                element.send_keys(str(df['comarca']))
                time.sleep(1)
            except:
                naoInserido['comarca'] = str(df['comarca'])

            # #PARA ATUALIZAR OS DADOS
            # logAtualizaPromad = os.getcwd() + "\\logs\\_Comarcas.txt"
            # rf.createLog(logAtualizaPromad)
            # for elemento in element.find_elements_by_tag_name('option'):
            #     texto = "{}\n".format(elemento.text)
            #     rf.createLog(logAtualizaPromad, texto, tipo="a", onlyText=True)

        # UF
        if (str(df['uf'])):
            try:
                element = rf.waitinstance(self.driver, '//*[@id="txtUf"]', 1, 'show')
                select = rf.Select(element)
                select.select_by_visible_text(str(df['uf']))
            except:
                naoInserido['uf'] = str(df['uf'])
        else:
            naoInserido['uf'] = 'Vazio'

        time.sleep(0.5)

        try:
            element = rf.waitinstance(self.driver, 'slcLocalizador', 1, 'show', 'id')
            select = rf.Select(element)
            select.select_by_visible_text(str(df['localizador']))
        except:
            naoInserido['localizador'] = str(df['localizador'])

        # RESPONSÁVEL
        if (df['responsavel']):   #condição para evitar percorrer a lista se for "Vazio"
            try:
                self.driver.execute_script("$('#slcResponsavel').css('display', 'block');") # torna elemento visível

                comboResponsavel = rf.waitinstance(self.driver, '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/button', 1, 'show')
                comboResponsavel.click()  # clica e abre as opções

                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                xInputs = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li'
                listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                # CARREGA LISTA DE RESPONSÁVEIS
                y = 1
                totalResp = len(df['responsavel'])
                countResp = 0
                print(totalResp)
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text in df['responsavel']):
                        xPathItem = '//*[@id="div_TipoProcesso"]/table/tbody/tr[1]/td[2]/table/tbody/tr[8]/td/div[2]/ul/li[{}]'.format(y)
                        element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                        element.click()
                        time.sleep(0.3)
                        countResp = countResp + 1
                        if (countResp == totalResp):
                            break
                    y = y + 1

                comboResponsavel.click() # clica para fechar as opções do combo
                self.driver.execute_script("$('#slcResponsavel').css('display', 'none');") #torna elemento invisível novamente
            except:
                naoInserido['responsavel'] = str(df['responsavel'])
        else:
            naoInserido['responsavel'] = 'Vazio'

        time.sleep(0.5)

        # Data da Contratação
        if (str(df['dataContratacao'])):
            try:
                self.driver.execute_script("document.getElementById('txtDataContratacao').value='{}' ".format(str(df['dataContratacao'])))
            except:
                naoInserido['dataContratacao'] = str(df['dataContratacao'])
        else:
            naoInserido['dataContratacao'] = 'Vazio'

        time.sleep(0.5)

        # Valor da Causa
        if (str(df['vCausa'])):
            try:
                self.driver.execute_script("document.getElementById('txtValorCausa').value='{}' ".format(str(df['vCausa'])) )
            except:            
                naoInserido['vCausa'] = str(df['vCausa'])
        else:
            naoInserido['vCausa'] = 'Vazio'

        time.sleep(0.5)

        #Obtém o ID do PROMAD da nova pasta a ser aberta 
        try:
            element = rf.waitinstance(self.driver, "idDoProcesso", 1, 'show', 'class')
            idNovaPasta = element.get_attribute("innerHTML")
            idNovaPasta = idNovaPasta[14:].strip()
        except:
            naoInserido['idDoProcesso'] = 'Não recuperado'

        # Abre a aba Parte Adversa
        try:
            element = rf.waitinstance(self.driver, "//*[@id='div_menu17']", 1, 'show')
            element.click()
            time.sleep(1)

            try:
                element = self.driver.find_element_by_id('div_txtComarca').is_displayed()
                self.driver.execute_script("verificarComboNovo('-1','txtComarca','slcComarca');")
                naoInserido['comarcaNova'] = str(df['comarcaNova'])

                # TENTANDO NOVAMENTE ABRIR PARTE ADVERSA
                element = rf.waitinstance(self.driver, "//*[@id='div_menu17']", 1, 'show')
                element.click()
                time.sleep(1)
            except:
                pass

            print('abrindo a parte adversa')
            time.sleep(0.5)
            rf.checkPopUps(self.driver)

            # Parte Adversa
            if (str(df['adversa'])):
                try:
                    element = rf.waitinstance(self.driver, '//*[@id="txtNome"]', 1, 'show')
                    element.send_keys(str(df['adversa']))
                except:
                    naoInserido['adversa'] = str(df['adversa'])
            else:
                naoInserido['adversa'] = 'Vazio'

            time.sleep(0.5)

            # Botão salvar
            element = rf.waitinstance(self.driver, '//*[@id="btnSalvar"]', 1, 'show')
            element.click()

            time.sleep(0.5)
            complemento = ""

            try:
                element = self.driver.find_element_by_id("popup_ok")
                self.driver.execute_script("arguments[0].click();", element)
                print('pop up OK')
                complemento = " | A Parte adversa - '{}' - tem outros processos registrados no sistema! |".format(str(df['adversa']))
                time.sleep(0.5)
            except:
                pass

            if (naoInserido):
                complemento = '{} Não foi gravado esses dados: '.format(complemento)
                for k, v in naoInserido.items():
                    complemento = '{} {}: {} | '.format(complemento, k, v)

            message = "REGISTRO {}: Nova pasta '{}': id Promad: '{}'.{}".format(registro, str(df['pasta']), idNovaPasta, complemento)
        except:
            message = "NÃO FOI POSSÍVEL ABRIR A PASTA {}".format(str(df['pasta']))

        time.sleep(0.5)
        return message

    def criarAgendamentos(self, dataAudiencia, dataAberturaPasta, horaAudienciaFormatada, sigla, responsavel, pasta, registro, dataCiencia, agendFotocopia):
        # Agendamentos
        print("criando agendamentos")
        element = rf.waitinstance(self.driver, "//*[@id='slcGrupo']", 1, 'show')  #checa se redirecionamento ocorreu
        self.driver.execute_script("clickMenuCadastro(109,'processoAgenda.asp');") #clica em agendamentos

        element = rf.waitinstance(self.driver, "btnAgendarSalvar", 1, 'show', id)  #checa se redirecionamento ocorreu para agendamentos
        rf.checkPopUps(self.driver)

        if (sigla =='BRA'):
            respCiencia = 'cbradesco'
        elif (sigla == 'BV'):
            respCiencia = 'CBV'

        complementoAgendamento = ""
        cont = 0
        for x in range(4):
            rf.checkPopUps(self.driver)
            if (dataAudiencia != ""):  #PARA INICIAR NO 1º AGENDAMENTO
                cont = x + 1
            else:
                cont = (x + 1) - 1  #PARA INICIAR NO 2º AGENDAMENTO
                complementoAgendamento = " A audiência não foi marcada."

            if (x == 0):   #tipo audiencia
                if (dataAudiencia != ""):
                    time.sleep(0.5)
                    xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

                    # combo destinatário - abrir
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                    element.click()

                    tipoAgendamento = 'Audiência'
                    appointmentDate = dataAudiencia

                    appointmentDate = datetime.datetime.strptime(dataAudiencia, "%d/%m/%Y")
                    # diaAudiencia = int(appointmentDate.day)

                    data = "{}/{}/{}".format(str(appointmentDate.day), str(appointmentDate.month), str(appointmentDate.year))
                    appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")
                    appointmentDate = format(appointmentDate, "%d/%m/%Y")

                    if (horaAudienciaFormatada != "00:00"):
                        agendamento = "{} - Audiência designada para dia {} às {}".format(sigla, str(appointmentDate), horaAudienciaFormatada)
                    else:
                        agendamento = "{} - Audiência designada para dia {}".format(sigla, str(appointmentDate))

                    #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                    xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                    listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                    totalResp = len(responsavel)
                    countResp = 0
                    y = 1
                    for item in listInputs:  #itera inputs recuperados, checa e clica
                        if (item.text == 'GST' or item.text in responsavel ):
                            xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                            element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                            element.click()
                            time.sleep(0.3)
                            countResp = countResp + 1
                            if (countResp == (totalResp + 1)):
                                break
                        y = y + 1
                    time.sleep(0.3)
                else:
                    continue

            elif (x == 1): #tipo Ciencia de novo processo
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

                # combo destinatário - abrir
                element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                element.click()

                tipoAgendamento = 'Ciencia de novo processo'
                dataAbPasta = datetime.datetime.strptime(dataCiencia, "%d/%m/%Y")
                dataIncrementada = dataAbPasta.date()
                data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")
                appointmentDate = format(appointmentDate, "%d/%m/%Y")
                agendamento = "{} - Certificar abertura, risco e promover agendamentos.{}".format(sigla, complementoAgendamento)

                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD  - OBTÉM SOMENTE DO PRIMEIRO SELECT-DESTINATÁRIO, POIS OS DEMAIS SÃO IGUAIS
                xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                # respons. pelo cliente
                y = 1
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text == respCiencia):
                        xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                        element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                        element.click()
                        time.sleep(0.3)
                        break
                    y = y + 1

            elif (x == 2): #tipo Anexar
                time.sleep(0.5)
                xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

                # combo destinatário - abrir
                element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                element.click()
                
                tipoAgendamento = 'Anexar'
                dataAbPasta = datetime.datetime.strptime(dataCiencia, "%d/%m/%Y")
                dataIncrementada = dataAbPasta.date()
                data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")
                appointmentDate = format(appointmentDate, "%d/%m/%Y")
                agendamento = "ANEXAR"

                #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                totalResp = 2
                countResp = 0
                y = 1
                for item in listInputs:  #itera inputs recuperados, checa e clica
                    if (item.text == 'ESTAGBRA' or item.text == respCiencia):
                        xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                        element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                        element.click()
                        time.sleep(0.3)
                        countResp = countResp + 1
                        if (countResp == totalResp):
                            break
                    y = y + 1

            elif (x == 3): #tipo Fotocópia
                if (agendFotocopia == "1"):
                    time.sleep(0.5)
                    xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)

                    # combo destinatário - abrir
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                    element.click()

                    tipoAgendamento = 'Fotocópia'
                    dataAbPasta = datetime.datetime.strptime(dataCiencia, "%d/%m/%Y")
                    dataIncrementada = dataAbPasta.date()
                    data = "{}/{}/{}".format(dataIncrementada.day, dataIncrementada.month, dataIncrementada.year)
                    appointmentDate = datetime.datetime.strptime("{}".format(data), "%d/%m/%Y")
                    appointmentDate = format(appointmentDate, "%d/%m/%Y")
                    agendamento = "Fotocópia integral"

                    #recupera lista de DESTINATÁRIOS cadastrados no PROMAD
                    xInputs = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li'.format(cont)
                    listInputs = self.driver.find_elements_by_xpath(xInputs) #recupera os inputs abaixo dessa tag

                    # GST e OPERAÇÕES
                    y = 1
                    found = 0
                    for item in listInputs:  #itera inputs recuperados, checa e clica
                        if (item.text == 'GST' or item.text == 'operacoes'):
                            xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/div[2]/ul/li[{}]'.format(cont, y)
                            element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                            element.click()
                            found = found + 1
                            time.sleep(0.3)
                        if (found >= 2):
                            break
                        y = y + 1

            time.sleep(0.3)

            # combo destinatário - fechar
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[3]/td[1]/button'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
            element.click()
            time.sleep(1)

            # combo TIPO - ABRIR
            xPathElement = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/button'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
            element.click()
            time.sleep(1)

            # # TIPO DE AGENDAMENTO  -  recupera lista de TIPOS cadastrados no PROMAD
            xTiposAgendamentos = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li'.format(cont)
            listTiposAgendamentos = self.driver.find_elements_by_xpath(xTiposAgendamentos) #recupera os inputs abaixo dessa tag

            y = 1
            for item in listTiposAgendamentos:  #itera inputs recuperados, checa e clica
                if (item.text == tipoAgendamento):
                    xPathItem = '//*[@id="tableAgendamentoCadastroProcesso{}"]/tbody/tr[4]/td/div[2]/ul/li[{}]'.format(cont, y)
                    element = rf.waitinstance(self.driver, xPathItem, 1, 'click')
                    element.click()
                    time.sleep(0.3)
                    break
                y = y + 1

            # CAMPO QUANDO
            time.sleep(0.3)
            xPathElement = '//*[@id="txtDataInicialAgendaProcesso{}"]'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
            element.clear()
            time.sleep(0.3)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
            element.send_keys(appointmentDate)
            time.sleep(0.3)

            try: #se o calendário estiver aberto, será fechado
                self.driver.execute_script("$('#ui-datepicker-div').css('display', 'none');") #torna elemento invisível novamente
            except:
                pass

            if (dataAudiencia != ""):
                if (x == 0):
                    # com HORA
                    time.sleep(0.3)
                    xPathElement = '//*[@id="chkDiaInteiroAgendaProcesso{}"]'.format(cont)
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                    time.sleep(0.3)
                    element.click()
                    
                    time.sleep(0.3)
                    xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(cont)
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'click')
                    element.clear()

                    time.sleep(0.3)
                    xPathElement = '//*[@id="txtHoraInicialAgendaProcesso{}"]'.format(cont)
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
                    element.send_keys(horaAudienciaFormatada)

                    time.sleep(0.3)
                    xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(cont)
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
                    element.clear()

                    time.sleep(0.3)
                    xPathElement = '//*[@id="txtHoraFinalAgendaProcesso{}"]'.format(cont)
                    element = rf.waitinstance(self.driver, xPathElement, 1, 'show')

                    time.sleep(0.3)
                    element.send_keys(horaAudienciaFormatada)
            else:
                pass

            # campo agendamento
            time.sleep(0.3)
            xPathElement = '//*[@id="txtDescricaoAgendaProcesso{}"]'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
            element.send_keys(agendamento)

            # campo resumo
            time.sleep(0.3)
            xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
            element.clear()
            time.sleep(0.3)
            xPathElement = '//*[@id="txtTituloAgendaProcesso{}"]'.format(cont)
            element = rf.waitinstance(self.driver, xPathElement, 1, 'show')
            element.send_keys(agendamento[:30])

            if (x < 3): #em fotocópia já não clica mais
                if (x < 2 or (x == 2 and agendFotocopia == "1")):  #se é menor que 2  ou  se for igual a 2 e agendFotocopia = '1'
                    element = rf.waitinstance(self.driver, '//*[@id="divAgendaCadastrarIncluir"]/a', 1, 'show')  #abrir novo agendamento
                    element.click()
                else:
                    break

        element = rf.waitinstance(self.driver, '//*[@id="btnAgendarSalvar"]', 1, 'click')
        element.click()

        try:
            element = rf.waitinstance(self.driver, '//*[@id="popup_ok"]', 1, 'click')
            element.click()
        except:
            pass

    def abrePasta(self, arquivoAbrirPasta, item = 1, extensao ="xlsx", path=""):
        dfExcel = rf.abreArquivo(arquivoAbrirPasta, extensao, path=path)
        count = dfExcel.number_of_rows()-1

        cliente = ''
        cliente = dfExcel[1, 12]

        try:
            searchClient = rf.pesquisarCliente(self.driver, cliente)
        except:
            return False

        if (searchClient):
            urlPage = self.driver.current_url
            while (item <= count):
                print ('FALTAM {} REGISTROS A EXECUTAR.'.format(count-item))
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
                    for x in range(qtdZero):
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
                    valorCausa     = locale.format_string("%1.2f", dfExcel[item, 10].strip() , 0)
                    df['vCausa']   = valorCausa.replace('.',',')
                except:
                    df['vCausa'] = "0"

                df['statusProcessual'] = dfExcel[item, 11]

                if (rf.checkIfTest()):  #se for teste
                    df['razaoSocial']  = "Cliente teste"
                    df['gpCliente']    = "Grupo Teste"
                else:
                    df['razaoSocial']  = dfExcel[item, 12]
                    df['gpCliente']    = dfExcel[item, 13]

                responsavel = dfExcel[item, 14].split(';')

                df['responsavel']  = responsavel
                df['sigla']        = dfExcel[item, 15].strip()

                try:
                    df['dataAudiencia'] = dfExcel[item, 16].strip()
                except:
                    df['dataAudiencia'] = ""

                try:
                    if (dfExcel[item, 17]):
                        df['horaAudiencia'] = dfExcel[item, 17].strip()
                        horaAudiencia = df['horaAudiencia'].strftime("%H:%M")
                    else:
                        df['horaAudiencia'] = "00:00"
                        horaAudiencia = df['horaAudiencia']
                except:
                    df['horaAudiencia'] = "00:00"
                    horaAudiencia = df['horaAudiencia']

                df['dataCiencia'] = dfExcel[item, 18]
                df['agendFotocopia'] = dfExcel[item, 19]
                df['localizador'] = dfExcel[item, 20]

                time.sleep(1)

                try:
                    if rf.checkIfTest():
                        searchFolder = False
                    else:
                        searchFolder, element = rf.pesquisarPasta(self.driver, df['pasta'])
                except:
                    print('Não foi possível realizar uma busca')
                    return False

                if (not(searchFolder)):   # se não foi encontrado no sistema, será inserido
                    try:
                        self.driver.get(urlPage)
                        time.sleep(1)
                        messageInclusaoNovoProcesso = self.incluirProcesso(df, item)
                    except:
                        print('Erro ao incluir a pasta: {}!'.format(df['pasta']))
                        return False
                    
                    try: #checa se redirecionamento ocorreu 
                        element = rf.waitinstance(self.driver, "//*[@id='slcGrupo']", 1, 'show')  
                    except:
                        print('Erro ao incluir a pasta: {}!'.format(df['pasta']))
                        return False

                    if (df['responsavel']):
                        try:
                            self.criarAgendamentos(df['dataAudiencia'], df['dataContratacao'], horaAudiencia, df['sigla'], df['responsavel'], df['pasta'], item, df['dataCiencia'], df['agendFotocopia'])
                            if (df['dataAudiencia'] != ""):
                                messageInclusaoNovoProcesso = "{} Agendamentos criados! | Audiência está marcada!".format(messageInclusaoNovoProcesso)
                            else:
                                messageInclusaoNovoProcesso = "{} Agendamentos criados! | Audiência NÃO está marcada!".format(messageInclusaoNovoProcesso)
                        except:
                            messageInclusaoNovoProcesso = "{} ERRO AO CRIAR OS AGENDAMENTOS! FAZÊ-LOS MANUALMENTE! |".format(messageInclusaoNovoProcesso)
                    else:
                        messageInclusaoNovoProcesso = "{} NÃO É POSSÍVEL CRIAR AGENDAMENTOS SEM RESPONSÁVEL! VERIFIQUE! |".format(messageInclusaoNovoProcesso)
                        print('Erro ao incluir Agendamentos')
                    rf.createLog(self.logFile, "{}".format(messageInclusaoNovoProcesso))
                else:
                    rf.createLog(self.logFile, "REGISTRO {}: A pasta '{}' já existe no sistema! Favor verificar!".format(item, df['pasta']))

                self.driver.get(urlPage)   # Volta para a tela de pesquisa
                item = item + 1

            #só encerrará o uso do arquivo se o retorno de abrir pasta for True
            rf.createLog(self.logFile, '_________________________________________________________________')
            rf.createLog(self.logFile, 'FIM')
            return True
        else:
            return False

    def checkLogin(self):
        checarTeste = rf.checkIfTest()
        if (checarTeste):
            print('\n------------EM MODO DE TESTE------------')
            login="robo@dplaw.com.br"
            password="dplaw00612"
        else:
            login="cgst@dplaw.com.br"
            password="gestao0"
        return login, password

    def controle(self, file, path):
        pidNumber = str(os.getpid())
        print("\npID: {}".format(pidNumber))

        infoLog = "EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG

        logsPath = path + "\\logs"
        pathExecutados = path + "\\arquivos_executados"

        if (os.path.exists(pathExecutados) == False):
            os.mkdir(pathExecutados)   # Se o diretório Volumetrias não existir, será criado - 

        if (os.path.exists(logsPath) == False):
            os.mkdir(logsPath)   # Se o diretório Abertura_pastas não existir, será criado - 

        driverIniciado = False
        self.driver = None
        abreNovaPasta = None

        login, password = self.checkLogin()

        print("\n-----------------------------------------")
        print("Login utilizado: {}".format(login))
        print("-----------------------------------------\n")

        file = file.split('.')
        arquivoAbrirPasta = '.'.join(file[:-1])
        extensao = file[-1]

        self.logFile = logsPath + "\\_log_{}.txt".format(arquivoAbrirPasta)

        abreWebDriver = None
        if (os.path.isfile(self.logFile)):    # se existir o log em andamento
            linha, count = rf.checkEndFile(self.logFile)

            if (linha == "FIM"): #ultima linha do arquivo
                print('O arquivo {}.xlsx já foi executado!\n'.format(arquivoAbrirPasta.upper()))
                abreNovaPasta = True # Avança no looping apagando o arquivo existente

            else: # continua o preenchimento do log já existente
                if (driverIniciado == False):
                    driverIniciado = True
                    print("\nINICIANDO WebDriver")
                    rf.createPID(arquivoAbrirPasta.upper(), pidNumber)
                    self.driver = rf.iniciaWebdriver(False)
                    abreWebDriver = rf.acessToIntegra(self.driver, login, password)
                if (abreWebDriver):
                    abreNovaPasta = self.abrePasta(arquivoAbrirPasta, count, extensao=extensao, path=path)
                else:
                    driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                    self.driver.quit()
                    # break
        else:
            print("\nINICIANDO WebDriver")
            if (driverIniciado == False):
                driverIniciado = True
                self.driver = rf.iniciaWebdriver(False)
                rf.createPID(arquivoAbrirPasta.upper(), pidNumber)
                abreWebDriver = rf.acessToIntegra(self.driver, login, password)
            if (abreWebDriver):
                abreNovaPasta = self.abrePasta(arquivoAbrirPasta, extensao=extensao, path=path)
            else:
                driverIniciado = False   #se houve erro ao abrir pasta - força o fechamento do Webdriver
                self.driver.quit()
                # break

        if (abreNovaPasta):
            if (file[0] != ""):
                os.remove("{}\\{}".format(path, infoLog))
                fileExecuted = pathExecutados + "\\{}.{}".format(arquivoAbrirPasta, extensao)
                if (os.path.isfile(fileExecuted)): #se o arquivo existir na pasta arquivos_executados -excluirá este e depois moverá o novo
                    os.remove(fileExecuted)
                shutil.move("{}\\{}.{}".format(path, arquivoAbrirPasta, extensao), pathExecutados) #após executar um arquivo, o mesmo é movido para a pasta 'arquivos_executados'
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