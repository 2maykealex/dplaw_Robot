# coding=utf-8
from os import path
from os import getcwd as osGetCWD
from os import mkdir as osMKdir
from os import walk
from os import rename
from os import remove
from shutil import move
from time import strftime
from time import sleep
from glob import glob
from datetime import date
from datetime import datetime
from threading import Thread
from basic_functions import checkPID
from basic_functions import createFolder
from basic_functions import createLog
from basic_functions import checkIfTest
from basic_functions import abreArquivo
from basic_functions import checkEndFile
from integra_functions import IntegraFunctions
import json
# from abertura import Abertura
# from volumetria import Volumetria
# from contrato import Contrato
# from atualizacao import Atualizacao

# def checkIFexecuting():
#     deletingFiles = []
#     for arquivo, logFile in executingFiles.items():
#         if (not(osPath.isfile(logFile))):
#             deletingFiles.append(arquivo)

#     for file in deletingFiles:
#         del executingFiles[file]
#         print('===O ARQUIVO {} FOI REMOVIDO DA LISTA==='.format(arquivo))

def acessaIntegra(registros, reg, pathFile, folderName, logFileCSV):
    # current_thread().name
    try:
        integra = IntegraFunctions()
        integra = integra.controle(registros, reg, logFileCSV)

        if (integra):
            executedPath = "{}\\arquivos_executados\\{}".format(path.dirname(__file__), folderName)
            executedFile = "{}\\{}".format(executedPath, pathFile.split('\\')[-1])
            createFolder(executedPath)

            if (path.isfile(executedFile)):#todo Testar
                rename(executedFile, '{}'.format(executedFile.replace('.txt', '.OLD.txt')))  # Antigo / Novo

            move("{}".format(pathFile), executedPath) #move o arquivo para a pasta 'arquivos_executados'
    except Exception as err:
        print('\nHouve um erro: {}\n'.format(err))
        pass
    executingFiles.remove(file) # COM ERRO OU SEM ERRO, REMOVE DA EXECUÇÃO
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))


#============================ ROBO PRINCIPAL====================================================
executePath = "{}\\arquivos_a_executar".format(path.dirname(__file__))
# executeRobot = []
executingFiles =  []
print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

while True:   # Percorre a pasta e subpastas de arquivos a executar em looping, checando a existência de novos arquivos
    files =  {}
    for folder, subdirs, filesFolder in walk(executePath):
        for name in filesFolder:
            if (name not in executingFiles):
                files[folder] = name

    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            pathFile = "{}\\{}".format(localFile, file)

            registros = abreArquivo(pathFile)
            registros = json.loads(registros)

            # CRIANDO ARQUIVO DE LOG .CSV
            logFileName = file.split('\\')[-1].split('.txt')[0]
            logPath     = '{}\\logs\\{}'.format(path.dirname(__file__), registros['tipo'])
            logFileCSV = "{}\\{}.csv".format(logPath, logFileName)
            createFolder(logPath) # CRIA DIRETÓRIO SE NÃO EXISTIR.

            if not(path.isfile(logFileCSV)): #se o log não existir, cria-se
                open(logFileCSV, 'a')
                if (registros['tipo'] == 'abertura'):
                    cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA;ID PROMAD;PARTE ADVERSA; ERRO: NÃO INSERIDOS; AGENDAMENTOS CRIADOS; AUDIÊNCIA; ERRO: AGENDAMENTOS NÃO CRIADOS;'
                elif (registros['tipo'] == 'atualizacao'):
                    cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA;ID PROMAD;CAMPOS ATUALIZADOS; ERRO: NÃO ATUALIZADOS'
                createLog(logFileCSV, "{}\n".format(cabeçalhoLog), printOut=False)

            # else:
            reg = checkEndFile(logFileCSV)

            executingFiles.append(file)
            executeRobot = (Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args= (registros, reg, pathFile, folderName, logFileCSV)))



            # executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra(file,pathFile, folderName))


        # for executa in executeRobot:
            print(executeRobot.name,'\n')
            try:
                executeRobot.start()
            except Exception as err:
                print(err)
                print('\n ERRO EM {}'.format(executeRobot.name))



        # try:
        #     print('\n', executeRobot.name,'\n')
        #     executeRobot.start()
        # except Exception as err:
        #     print('\n ERRO EM {}'.format(executeRobot.name))
        #     pass