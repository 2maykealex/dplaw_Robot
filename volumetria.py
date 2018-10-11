'''
projeto   deeplaw: volumetria
automatizar a inserção da volumetria em pastas existentes no sistema dplaw
'''
import sys
import os
import time
import glob
import robot_functions as rf

def pesquisarPasta(pasta = '01700117977'):
    
    # ACESSANDO DIRETAMENTE A PÁGINA DE PESQUISA NO SISTEMA
    urlPage =  "https://www.integra.adv.br/integra4/modulo/21/default.asp"
    driver.get(urlPage)

    # selecionar opção pesquisa por pasta
    element = rf.waitinstance(driver, '//*[@id="chkPesquisa139"]', 30, 1, 'show')
    element.click()

    # buscando pasta
    element = rf.waitinstance(driver, "txtPesquisa", 30, 1, 'show', 'id')
    element.send_keys(pasta)
    driver.find_element_by_id("btnPesquisar").click()
    
    # SELECIONA O CLIENTE PESQUISADO
    time.sleep(3)
    element = rf.waitinstance(driver, "//*[@id='divCliente']/div[3]/table/tbody/tr/td[5]", 30, 1, 'click')
    element.click()

def inserirVolumetria(volumetriaMes, pasta):

    element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')

    if (element.get_attribute('value') ==  ''):
        print('Preenchendo a volumetria ', volumetriaMes, ' na pasta ', pasta,'\n')
        element = rf.waitinstance(driver, '//*[@id="txtCampoLivre3"]', 30, 1, 'show')
        element.send_keys(volumetriaMes)

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="btnSalvar"]', 30, 1, 'show')
        element.click()

        # SALVAR ALTERAÇÃO
        time.sleep(2)
        element = rf.waitinstance(driver, '//*[@id="popup_ok"]', 30, 1, 'show')
        element.click() 
    else:
        print('------> A pasta ', pasta, ' já está com a volumetria correspondente preenchida!\n')
        time.sleep(2)
       
def enviaParametros(volumetriaMes):
    print('> > > ACESSANDO ARQUIVO ', volumetriaMes, '.xlsx')
    dfExcel = rf.abreArquivo(volumetriaMes)
    count = dfExcel.number_of_rows()-1
    item = 1

    while (item <= count):         #looping dentro de cada arquivo
        pasta =  dfExcel[item, 7]
        pesquisarPasta(pasta)
        print('> > Acessando a pasta ', pasta)
        inserirVolumetria(volumetriaMes, pasta)
        item = item + 1

#============================PROGRAMA PRINCIPAL==============================
#executando python volumetria.py "Volumetria 2018.09.xlsx" no TERMINAL


print('\n========== SELECIONE UMA DAS OPÇÕES ABAIXO ==========\n')

path = os.getcwd() + "/volumetrias" # obtem o caminho do script e add a pasta volumetrias

os.chdir(path) # seleciona o diretório do script



files =  []
print('0  =>  EXECUTAR TODOS OS ARQUIVOS DA PASTA  "VOLUMETRIAS" ')
print('-------------------------------------------')
for file in glob.glob("volu*.xlsx"):
    # print('-------------------------------------------')
    files.append(file)
    print(len(files), ' => ', files[-1])    
print('-------------------------------------------')

selectedFile = int(input('Digite sua opção: '))
print('> > > ACESSANDO http://www.integra.adv.br/...')
time.sleep(1)
driver = rf.iniciaWebdriver(True)
rf.acessToIntegra(driver)


if (selectedFile-1 < 0):
    # opção 0 selecionada
    for file in files:
        volumetriaMes = file
        volumetriaMes = volumetriaMes[:-5]
        enviaParametros(volumetriaMes)
else:
    volumetriaMes = files[selectedFile -1]
    volumetriaMes = volumetriaMes[:-5]
    enviaParametros(volumetriaMes)

rf.logoutIntegra(driver)