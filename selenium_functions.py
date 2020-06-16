from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from os import path as osPath
from platform import system as SO
import time

class SeleniumFunctions(object):
    def select(self, element):
        return Select(element)

    def waitInstance(self, driver, object, poll, type, form = 'xpath'):
        timeOut = 10 #segundos
        count = 1
        while (count < 6):
            try:
                if type == 'click':
                    if form == 'xpath':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.XPATH, object)))
                        # return element
                    elif form == 'id':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.ID, object)))
                    elif form == 'class':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.element_to_be_clickable((By.CLASS_NAME, object)))
                        # return element
                elif type == 'show':
                    if form == 'xpath':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.XPATH, object)))
                        # return element
                    elif form == 'id':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.ID, object)))
                    elif form == 'class':
                        element = WebDriverWait(driver, timeOut, poll_frequency = poll,
                                                ignored_exceptions=[NoSuchElementException,
                                                ElementNotVisibleException, ElementNotSelectableException]).until(EC.presence_of_element_located((By.CLASS_NAME, object)))
                return element
            except:
                count = count + 1
                hora = time.strftime("%H:%M:%S")
                print('{} - {} - Elemento ainda não foi encontrado!'.format(count, hora))

        return False

    def iniciaWebdriver(self, modSilent = False, monitor = 2):

        sistemaOperacional = SO()

        if (sistemaOperacional == 'Windows'):
            # acessando diretório do webdriver do chrome no WINDOWS
            dirpath = osPath.dirname(osPath.realpath(__file__))
            chromepath = dirpath + '/chromedriver.exe'
        elif (sistemaOperacional == 'Linux'):
            # acessando diretório do webdriver do chrome no LINUX
            dirpath = '/usr/bin'
            chromepath = dirpath + '/chromedriver'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
        #chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

        if (modSilent == True):                   # Modo Silencioso: O Navegador fica oculto
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument("--log-level=3")

        slow = False # True - Internet Lenta  / False - Internet normal

        if (slow):
            chrome_options.add_argument("--disable-application-cache")

        driver = webdriver.Chrome(executable_path = chromepath, chrome_options=chrome_options)

        if (monitor == 2):
            driver.set_window_position(2000,0)   # ATIVA A EXECUÇÃO NO SEGUNDO MONITOR

        self.slowInternet(driver, slow)
        return driver

    def slowInternet(self, driver, active = False):   # Para simular internet Lenta
        if (active == True):
            driver.set_network_conditions(
            offline=False,
            latency=3,  # additional latency (ms)
            download_throughput= 50 * 1024,  # maximal throughput
            upload_throughput= 50 * 1024)  # maximal throughput
