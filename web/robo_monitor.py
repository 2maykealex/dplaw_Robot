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
from basic_functions import checkIfTest
from integra_functions import IntegraFunctions
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

def acessaIntegra(file, pathFile, folderName):
    # current_thread().name
    try:
        integra = IntegraFunctions()
        integra = integra.controle(pathFile)

        if (integra):
            executedPath = "{}\\arquivos_executados\\{}".format(path.dirname(__file__), folderName)
            executedFile = "{}\\{}".format(executedPath, pathFile.split('\\')[-1])

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
executeRobot = None
executingFiles =  []
print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

while True:   # Percorre a pasta e subpastas de arquivos a executar em looping, checando a existência de novos arquivos
    files =  {}
    for folder, subdirs, filesFolder in walk(executePath):
        for name in filesFolder:
            if (name not in executingFiles):
                files[folder] = name
    # sleep(3)
    # checkIFexecuting()

    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            pathFile = "{}\\{}".format(localFile, file)
            # localPid = "{}\\pIDs".format(osGetCWD())

            # infoLog = "\\EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
            # infoLog = localFile + infoLog
            # try:
            #     fileEpid = 0
            #     for fileEpid in glob("{}\\*.pid".format(localPid)):
            #         pId = fileEpid.split("\\")[-1]
            #         pId = pId.split("__")
            #         if (pId[0] == file.split('.')[0]): #só vai remover o pID referente ao arquivo em execução
            #             pId = int (pId[-1].replace(".pid", ""))
            #             if (not(checkPID(pId))): #se pID não está em execução. remover arquivos
            #                 try:
            #                     osRemove(fileEpid)
            #                     print("Removido o PID: {}".format(pId))
            #                     osRemove(infoLog)
            #                 except:
            #                     pass
            #     if (not (fileEpid)):  #se FileEpid não existir, Remova o infoLog.
            #         if (osPath.isfile(infoLog)):
            #             osRemove(infoLog)
            # except:
            #     pass

            # print("\n{} - {} - Uma nova instancia de {} foi aberta".format(date.today(), strftime("%H:%M:%S"), folderName.upper()))
            # arquivo = open(infoLog, 'w+')
            # arquivo.close()
            executingFiles.append(file)

            if (folderName == "abertura"):
                executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra(file,pathFile, folderName))
            # elif (folderName == "volumetrias"):
            #     executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args=("2", file, localFile))
            # elif (folderName == "contrato"):
            #     executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args=("3", file, localFile))
            # elif (folderName == "atualizacao"):
            #     executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args=("4", file, localFile))
            # elif (folderName == "fechamento"):
            #     executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args=("5", file, localFile))

        try:
            print('\n', executeRobot.name,'\n')
            executeRobot.start()
        except Exception as err:
            print('\n ERRO EM {}'.format(executeRobot.name))
            pass