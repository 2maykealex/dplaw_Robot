from selenium_functions import SeleniumFunctions
from datetime import datetime
from datetime import timedelta
from time import strftime
from time import sleep

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
            sleep(0.2)
            self.driver.find_element_by_tag_name('button').click()
            sleep(0.2)
            self.checkPopUps()
            return True
        except:
            return False

    def acessaMenuPesquisa(self):
        #menu CLIENTES
        sleep(1)
        try:
            element = self.waitingElement('//*[@id="header"]/ul/li[1]')
            # sleep(.5)
            element.click()
        except:
            print("ERRO AO CLICAR NO MENU CLIENTES")
            return False

        #submenu PESQUISAR CLIENTE
        try:
            element = self.waitingElement('//*[@id="header"]/ul/li[1]/ul/lii[1]/p')
            element.click()
        except:
            print("ERRO AO CLICAR NO SUBMENU PESQUISAR CLIENTES")
            return False
        return True

    def pesquisarCliente(self, search, tipoPesquisa):
        menuPesquisa = self.acessaMenuPesquisa()
        if (menuPesquisa):
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

            element = self.waitInstance(self.driver, '{}'.format(xPathOption), 1, 'click')
            element.click()
            sleep(0.5)

            # valor do parâmetro
            self.driver.execute_script("document.getElementById('txtPesquisa').value='{}' ".format(search))
            sleep(2)
            print("pesquisar pasta {}".format(search))
            #botão pesquisar
            self.driver.find_element_by_id("btnPesquisar").click()
            sleep(2)

            try:
                #Checa se não existe registros para essa pasta
                element = self.driver.find_element_by_id('loopVazio').is_displayed()
                hora = strftime("%H:%M:%S")
                print('{} - Não encontrou a pasta'.format(hora))
                retorno = False

            except:
                # SELECIONA O CLIENTE PESQUISADO        -  clica no primeiro item encontrado(não poderia ter duas pastas com o mesmo número)
                try:
                    element = self.waitInstance(self.driver, "{}/div".format(xPathClick), 1, 'click')
                except:
                    try:
                        element = self.waitInstance(self.driver, "{}/div".format(xPathClick), 1, 'click')
                    except:
                        pass
                        # element = self.waitInstance(self.driver, '//*[@id="divCliente"]/div[3]/table/tbody/tr', 1, 'click')  #clica no registro -> abre a pasta
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
        element = self.waitInstance(self.driver, '//*[@id="btnSalvar"]', 1, 'show')
        element.click()
        # POP UP (OK)
        sleep(1)
        element = self.waitInstance(self.driver, '//*[@id="popup_ok"]', 1, 'show')
        element.click()

    def logoutIntegra(self):
        self.driver.execute_script("chamarLink('../../include/desLogarSistema.asp');")
        sleep(2)
        self.driver.quit()

    def checkPopUps(self):
        popupOk = False
        try:
            self.driver.execute_script("$('.popup_block').css('display', 'none');")
            popupOk = True
        except:
            pass

        try:
            self.driver.execute_script("$('#menuvaimudar').css('display', 'none');")
            popupOk = True
        except:
            pass

        try:
            self.driver.execute_script("$('#divFecharAvisoPopUp').css('display', 'none');")
            popupOk = True
        except:
            pass

        try:
            self.driver.execute_script("$('#backgroundPopup').css('display', 'none');")
            popupOk = True
        except:
            pass

        try:
            self.driver.execute_script("$('#carregando').css('display', 'none');")
            popupOk = True
        except:
            pass

        try:
            self.driver.execute_script("$('#card').css('display', 'none');")
            popupOk = True
        except:
            pass

        if (popupOk == True):
            sleep(2)

    def waitingElement(self, elementName):
        tempo = datetime.now().second + 15
        while True:
            try:
                element = self.waitInstance(self.driver, elementName, 2, 'click')
                return element
            except:
                if (datetime.now().second <= tempo):
                    print('Tempo Esgotado!!! Saindo!')
                    return False
                else:
                    print('teste  - não encontrado ainda!!!!')
                pass