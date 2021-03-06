# coding=utf-8
from os import path
from os import walk
from os import rename
from os import remove
from sys import exc_info
from shutil import move
from time import sleep, strftime
from datetime import date
from threading import Thread
from basic_functions import createFolder
from basic_functions import createLog
from basic_functions import deleteLastLineLog
from basic_functions import abreArquivo
from basic_functions import checkEndFile
from integra_functions import IntegraFunctions
import json

def acessaIntegra(registros, reg, pathFile, folderName, logFileCSV):
    try:
        integra = IntegraFunctions()
        integra = integra.controle(registros, reg, logFileCSV)

        if (integra):
            executedFileFolder = "{}\\{}".format(ARQUIVOS_EXECUTADOS, registros['tipo'])
            executedFile = "{}\\{}".format(executedFileFolder, pathFile.split('\\')[-1])
            createFolder(executedFileFolder)

            if (path.isfile(executedFile)):
                rename(executedFile, '{}'.format(executedFile.replace('.txt', '.OLD.txt')))  # Antigo / Novo

            move("{}".format(pathFile), executedFileFolder)

    except Exception as err:
        print('\nHouve um erro: {}\n'.format(err))
        pass

    executingFiles.remove(pathFile.split('\\')[-1]) # COM ERRO OU SEM ERRO, REMOVE DA EXECUÇÃO
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

def checkNewFiles():
    while True:
        for folder, subdirs, filesFolder in walk(ARQUIVOS_A_EXECUTAR):
            for name in filesFolder:
                try:
                    if (name not in executingFiles):
                        pathFile = "{}\\{}".format(folder, name)
                        registros = abreArquivo(pathFile)
                        registros = json.loads(registros)
                        logPath     = '{}\\{}'.format(LOGS, registros['tipo'])
                        logFileCSV = "{}\\{}.csv".format(logPath, name.replace('.txt', '').strip())
                        logsFiles.append(logFileCSV)
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
                        createLog(logFileCSV, "EM FILA", printOut=False)

                        if (reg != 'FIM'):
                            executingFiles.append(name)
                            try:
                                myThreads.append(Thread(name='Executa_{}_{}'.format(registros['tipo'].upper(), name.upper()), target=acessaIntegra, args= (registros, reg, pathFile, folder, logFileCSV)))
                            except Exception as err:
                                print(err)
                                print('\n ERRO EM {}'.format(myThreads.name))
                                if (name in executingFiles):
                                    executingFiles.remove(name)
                                    logsFiles.remove(logFileCSV)
                        else:
                            if (name in executingFiles):
                                executingFiles.remove(name)
                                logsFiles.remove(logFileCSV)

                            executedFolder = '{}\\{}'.format(ARQUIVOS_EXECUTADOS, registros['tipo'])
                            executedFile   = '{}\\{}'.format(executedFolder, name)

                            createFolder(executedFolder)
                            if (path.isfile(executedFile)):
                                rename(executedFile, '{}'.format(executedFile.replace('.txt', '.OLD.txt')))  # Antigo / Novo
                            move("{}".format(pathFile), executedFolder) #move o arquivo para a pasta 'arquivos_executados'

                            print("NÃO HÁ MAIS REGISTROS NO ARQUIVO '{}' PARA IMPORTAR.".format(name).upper())
                            print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))

                    elif (name in executingFiles): #se por ventura, o Log da execução tenha sido deletado
                        for x in range(len(logsFiles)):
                            if (not(path.isfile(logsFiles[x]))):
                                executingFiles.remove(name)
                                logsFiles.remove(logsFiles[x])
                except:
                    pass

        sleep(1.5)

#============================================= ROBO PRINCIPAL====================================================
ARQUIVOS_A_EXECUTAR = "{}\\arquivos_a_executar".format(path.dirname(path.realpath(__file__)))
ARQUIVOS_EXECUTADOS = "{}\\arquivos_executados".format(path.dirname(path.realpath(__file__)))
LOGS = "{}\\LOGS".format(path.dirname(path.realpath(__file__)))
createFolder(ARQUIVOS_A_EXECUTAR)
createFolder(ARQUIVOS_EXECUTADOS)
createFolder(LOGS)

try:
    file = None
    executeRobot = []
    executingFiles =  []
    myThreads = []
    logsFiles = []

    #THREAD CHECA NOVOS ARQUIVOS E ADD NA FILA DE THREADS
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))
    checkNewFilesThread = Thread(name='CHECK_NEW_FILES', target=checkNewFiles, args= ()).start()

    while True:
        if (myThreads): #CASO HAJA NOVOS ARQUIVOS
            myThread = myThreads[0]
            if (path.isfile(myThread._args[2].strip())): #SE O ARQUIVO ADD AINDA ESTÁ NA PASTA
                print('\n{}\n'.format(myThread.name))
                deleteLastLineLog(myThread._args[-1].strip()) #DELETE ULTIMA LINHA QUE DIZ "EM FILA"
                myThread.start()
                while (myThread.is_alive()):
                    pass
            else:
                remove(myThread._args[-1]) # SE O ARQUIVO ADD NÃO ESTÁ MAIS DISPONÍVEL, O SEU LOG TAMBÉM É APAGADO
            try:
                if (myThread._args[2] in executingFiles):
                    executingFiles.remove(myThread._args[2]) #REMOVE DA FILA DE EXECUÇÃO
                    logsFiles.remove(myThread._args[-1])
            except:
                pass
            myThreads.remove(myThread) #REMOVE A THREAD EXECUTADA


except Exception as err:
    exception_type, exception_object, exception_traceback = exc_info()
    line_number = exception_traceback.tb_lineno
    if (file in executingFiles):
        executingFiles.remove(file)
    print('\n <<< HOUVE UM ERRO INESPERADO EM -> {} na linha {}>>>'.format(err, line_number))
    pass
