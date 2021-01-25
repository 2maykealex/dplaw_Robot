# coding=utf-8
from os import path
from os import walk
from os import rename
from shutil import move
from time import sleep, strftime
from datetime import date
from datetime import datetime
from threading import Thread
from basic_functions import createFolder
from basic_functions import createLog
from basic_functions import abreArquivo
from basic_functions import checkEndFile
from integra_functions import IntegraFunctions
import json

def acessaIntegra(registros, reg, pathFile, folderName, logFileCSV):
    try:
        integra = IntegraFunctions()
        integra = integra.controle(registros, reg, logFileCSV)

        if (integra):
            executedFileFolder = "{}\\{}".format(ARQUIVOS_EXECUTADOS, folderName)
            executedFile = "{}\\{}".format(executedFileFolder, pathFile.split('\\')[-1])
            createFolder(executedFileFolder)

            if (path.isfile(executedFile)):
                rename(executedFile, '{}'.format(executedFile.replace('.txt', '.OLD.txt')))  # Antigo / Novo

            move("{}".format(pathFile), executedFileFolder) #move o arquivo para a pasta 'arquivos_executados'
    except Exception as err:
        print('\nHouve um erro: {}\n'.format(err))
        pass
    executingFiles.remove(file) # COM ERRO OU SEM ERRO, REMOVE DA EXECUÇÃO
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))


#============================ ROBO PRINCIPAL====================================================
ARQUIVOS_A_EXECUTAR = "{}\\arquivos_a_executar".format(path.dirname(path.realpath(__file__)))
ARQUIVOS_EXECUTADOS = "{}\\arquivos_executados".format(path.dirname(path.realpath(__file__)))
LOGS = "{}\\LOGS".format(path.dirname(path.realpath(__file__)))
createFolder(ARQUIVOS_A_EXECUTAR)
createFolder(ARQUIVOS_EXECUTADOS)
createFolder(LOGS)

executeRobot = []
executingFiles =  []
print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

while True:   # Percorre a pasta e subpastas de arquivos a executar em looping, checando a existência de novos arquivos
    files =  {}
    for folder, subdirs, filesFolder in walk(ARQUIVOS_A_EXECUTAR):
        for name in filesFolder:
            if (name not in executingFiles):
                files[folder] = name
    sleep(3)

    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            pathFile = "{}\\{}".format(localFile, file)

            registros = abreArquivo(pathFile)
            registros = json.loads(registros)

            # CRIANDO ARQUIVO DE LOG .CSV
            logFileName = file.split('\\')[-1].split('.txt')[0]
            logPath     = '{}\\{}'.format(LOGS, registros['tipo'])
            logFileCSV = "{}\\{}.csv".format(logPath, logFileName)
            createFolder(logPath) # CRIA DIRETÓRIO SE NÃO EXISTIR.

            if not(path.isfile(logFileCSV)): #se o log não existir, cria-se
                open(logFileCSV, 'a')
                cabeçalhoLog = ''
                if (registros['tipo'] == 'abertura'):
                    cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA / NUM PROCESSO;ID PROMAD;PARTE ADVERSA; ERRO: NÃO INSERIDOS; AGENDAMENTOS CRIADOS; AUDIÊNCIA; ERRO: AGENDAMENTOS NÃO CRIADOS;'
                elif (registros['tipo'] == 'atualizacao'):
                    cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA / NUM PROCESSO;ID PROMAD;CAMPOS ATUALIZADOS; ERRO: NÃO ATUALIZADOS'
                createLog(logFileCSV, "{}\n".format(cabeçalhoLog), printOut=False)

            reg = checkEndFile(logFileCSV)
            if (reg != 'FIM'):
                executingFiles.append(file)
                executeRobot.append(Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args= (registros, reg, pathFile, folderName, logFileCSV)))
            else:
                if (file in executingFiles):
                    executingFiles.remove(file)
                createFolder('{}\\{}'.format(ARQUIVOS_EXECUTADOS, folderName))
                move("{}".format(pathFile), '{}\\{}'.format(ARQUIVOS_EXECUTADOS, folderName)) #move o arquivo para a pasta 'arquivos_executados'
                print("NÃO HÁ MAIS REGISTROS NO ARQUIVO '{}' PARA IMPORTAR.".format(file).upper())
                print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

        if (executeRobot):
            for executa in executeRobot:
                print('\n', executa.name,'\n')
                try:
                    executa.start() # ABRIRÁ TODOS OS ARQUIVOS SIMULTÂNEAMENTE
                except Exception as err:
                    print(err)
                    print('\n ERRO EM {}'.format(executa.name))