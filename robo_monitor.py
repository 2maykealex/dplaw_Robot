# coding=utf-8
from os import path as osPath
from os import getcwd as osGetCWD
from os import mkdir as osMKdir
from os import rename as osRename
from os import remove as osRemove
from time import strftime
from time import sleep
from glob import glob
from datetime import date
from datetime import datetime
from threading import Thread
from basic_functions import checkPID
from basic_functions import checkIfTest
from abertura import Abertura
from volumetria import Volumetria
from contrato import Contrato
from atualizacao import Atualizacao

def checkIFexecuting():
    deletingFiles = []
    for arquivo, logFile in executingFiles.items():
        if (not(osPath.isfile(logFile))):
            deletingFiles.append(arquivo)

    for file in deletingFiles:
        del executingFiles[file]
        print('===O ARQUIVO {} FOI REMOVIDO DA LISTA==='.format(arquivo))

def abrirRobo(tipo, file, path):
    # current_thread().name
    robo = None
    if (tipo == '1'):
        robo = Abertura()
    elif (tipo == '2'):
        robo = Volumetria()
    elif (tipo == '3'):
        robo = Contrato()
    elif (tipo == '4'):
        robo = Atualizacao()
    # elif (tipo == '5'):
    #     robo = Fechamento()
    try:
        robo.controle(file, path)
    except:
        pass
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))


#============================ ROBO PRINCIPAL====================================================
localRobot        = osGetCWD() # obtem o caminho do Robô
local_OpenFolder  = osGetCWD() + "\\abertura.py"    # obtem o caminho do script Abertura de pastas
local_Contract    = osGetCWD() + "\\contrato.py"  # obtem o caminho do script Volumetria de pastas
local_Volumetria  = osGetCWD() + "\\volumetria.py"  # obtem o caminho do script Volumetria de pastas
local_Update      = osGetCWD() + "\\atualizacao.py" # obtem o caminho do script Atualização de pastas
local_CloseFolder = osGetCWD() + "\\fechamento.py"  # obtem o caminho do script Encerramento de pastas

OpenFolderPath    = osGetCWD() + "\\files\\abertura_pastas" # obtem o caminho do script e add a pasta abertura_pastas
ContractPath      = osGetCWD() + "\\files\\contrato"     # obtem o caminho do script e add a pasta abertura_pastas
VolumetriaPath    = osGetCWD() + "\\files\\volumetrias"     # obtem o caminho do script e add a pasta abertura_pastas
UpdatePath        = osGetCWD() + "\\files\\atualizacao"     # obtem o caminho do script e add a pasta abertura_pastas
ClosePath         = osGetCWD() + "\\files\\fechamento"      # obtem o caminho do script e add a pasta abertura_pastas

executeRobot = None
executingFiles =  {}
print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), strftime("%H:%M:%S")))
while True:      #Fará looping infinito, buscando novos arquivos nas pastas - se encontrar, abrirá o seu respectivo script
    sleep(3)
    checkIFexecuting()
    files =  {}
    # filesInFolder = set(glob("{}\\*.xls*".format(OpenFolderPath))) - set(glob("{}\\*.txt".format(OpenFolderPath)))

    #criar uma lista/dicionario contendo os dados dos scripts e executá-los no FOR(1 for)
    for file in glob("{}\\*.xls*".format(OpenFolderPath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            if (fileName not in executingFiles):
                files[OpenFolderPath] = fileName

    for file in glob("{}\\*.xls*".format(VolumetriaPath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            if (fileName not in executingFiles):
                files[VolumetriaPath] = fileName

    for file in glob("{}\\*.xls*".format(ContractPath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            extension = fileName.split('.')[-1]
            checkValor = fileName.split(' ')
            if (checkValor[0] != 'Contrato'): #Renomeia o Arquivo
                oldFileName = fileName
                fileName = fileName.replace('{}'.format(checkValor[0]), 'Contrato PA_{}.{}'.format(datetime.now().strftime("%Y_%m"), extension))
                osRename(osPath.join(ContractPath, oldFileName), osPath.join(ContractPath, fileName))  # Old - New
            else:
                if (fileName not in executingFiles):
                    files[ContractPath] = fileName

    for file in glob("{}\\*.xls*".format(UpdatePath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            if (fileName not in executingFiles):
                files[UpdatePath] = fileName

    # for file in glob("{}\\*.xls*".format(ClosePath)):
    #     if (file[-3:] != 'txt'):
    #         fileName = file.split("\\")
    #         fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
    #         if (fileName not in executingFiles):
    #             files[ClosePath] = fileName

    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            localPid = "{}\\pIDs".format(osGetCWD())

            infoLog = "\\EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
            infoLog = localFile + infoLog
            try:
                fileEpid = 0
                for fileEpid in glob("{}\\*.pid".format(localPid)):
                    pId = fileEpid.split("\\")[-1]
                    pId = pId.split("__")
                    if (pId[0] == file.split('.')[0]): #só vai remover o pID referente ao arquivo em execução
                        pId = int (pId[-1].replace(".pid", ""))
                        if (not(checkPID(pId))): #se pID não está em execução. remover arquivos
                            try:
                                osRemove(fileEpid)
                                print("Removido o PID: {}".format(pId))
                                osRemove(infoLog)
                            except:
                                pass
                if (not (fileEpid)):  #se FileEpid não existir, Remova o infoLog.
                    if (osPath.isfile(infoLog)):
                        osRemove(infoLog)
            except:
                pass
            print("\n{} - {} - Uma nova instancia de {} foi aberta".format(date.today(), strftime("%H:%M:%S"), folderName.upper()))
            arquivo = open(infoLog, 'w+')
            arquivo.close()
            executingFiles[file] = infoLog
            if (folderName == "abertura_pastas"):
                executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("1", file, localFile))
            elif (folderName == "volumetrias"):
                executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("2", file, localFile))
            elif (folderName == "contrato"):
                executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("3", file, localFile))
            elif (folderName == "atualizacao"):
                executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("4", file, localFile))
            # elif (folderName == "fechamento"):
            #     executeRobot = Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("5", file, localFile))

            try:
                executeRobot.start()
                print('\n', executeRobot.name,'\n')
            except Exception as err:
                print('\n ERRO EM {}'.format(executeRobot.name))
                pass