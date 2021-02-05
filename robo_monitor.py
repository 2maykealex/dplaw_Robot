# coding=utf-8
from os import path
from os import walk
from os import rename
from sys import exc_info
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

            move("{}".format(pathFile), executedFileFolder)
    except Exception as err:
        print('\nHouve um erro: {}\n'.format(err))
        pass

    executingFiles.remove(file) # COM ERRO OU SEM ERRO, REMOVE DA EXECUÇÃO
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

#============================================= ROBO PRINCIPAL====================================================
ARQUIVOS_A_EXECUTAR = "{}\\arquivos_a_executar".format(path.dirname(path.realpath(__file__)))
ARQUIVOS_EXECUTADOS = "{}\\arquivos_executados".format(path.dirname(path.realpath(__file__)))
LOGS = "{}\\LOGS".format(path.dirname(path.realpath(__file__)))
createFolder(ARQUIVOS_A_EXECUTAR)
createFolder(ARQUIVOS_EXECUTADOS)
createFolder(LOGS)

executeRobot = []
executingFiles =  []
print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

while True:
    try:
        files =  {}
        countFiles = 0
        for folder, subdirs, filesFolder in walk(ARQUIVOS_A_EXECUTAR):
            for name in filesFolder:
                if (name not in executingFiles):
                    files[countFiles] = {folder : name}
                    countFiles = countFiles + 1
        sleep(3)

        if (files):
            for _numFile, fileItem in files.items():
                for localFile, file in fileItem.items():
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
                            cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA / NUM PROCESSO;ID PROMAD;PARTE ADVERSA; ITENS NÃO INSERIDOS; AGENDAMENTOS CRIADOS; AUDIÊNCIA; AGENDAMENTOS NÃO CRIADOS;'
                        elif (registros['tipo'] == 'atualizacao'):
                            cabeçalhoLog = 'REG NUMº;DATA-HORA;NUM PASTA / NUM PROCESSO;ID PROMAD;CAMPOS ATUALIZADOS; ITENS NÃO ATUALIZADOS'
                        createLog(logFileCSV, "{}\n".format(cabeçalhoLog), printOut=False)

                    reg = checkEndFile(logFileCSV)
                    if (reg != 'FIM'):
                        executingFiles.append(file)
                        myThread = None
                        myThread = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=acessaIntegra, args= (registros, reg, pathFile, folderName, logFileCSV))
                        executeRobot.append(myThread)
                    else:
                        if (file in executingFiles):
                            executingFiles.remove(file)

                        createFolder('{}\\{}'.format(ARQUIVOS_EXECUTADOS, folderName))
                        move("{}".format(pathFile), '{}\\{}'.format(ARQUIVOS_EXECUTADOS, folderName)) #move o arquivo para a pasta 'arquivos_executados'
                        print("NÃO HÁ MAIS REGISTROS NO ARQUIVO '{}' PARA IMPORTAR.".format(file).upper())
                        print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))
                        continue

            if (executeRobot):
                for num, executa in enumerate(executeRobot):
                    print('\n', executa.name,'\n')
                    try:
                        executa.start()
                    except Exception as err:
                        print('\n ERRO EM {} -> {}'.format(executa.name, err))

                executeRobot = None

    except Exception as err:
        exception_type, exception_object, exception_traceback = exc_info()
        line_number = exception_traceback.tb_lineno
        print('\n <<< HOUVE UM ERRO INESPERADO EM -> {} na linha {}>>>'.format(err, line_number))
        pass
