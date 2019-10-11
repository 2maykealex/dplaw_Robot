import os
import time
import glob
from datetime import date
import robot_functions as rf
import threading
from abertura import Abertura
from volumetria import Volumetria

def checkIFexecuting():
    deletingFiles = []
    for arquivo, logFile in executingFiles.items():
        if (not(os.path.isfile(logFile))):
            deletingFiles.append(arquivo)
            
    for file in deletingFiles:
        del executingFiles[file]
        print('===O ARQUIVO {} FOI REMOVIDO DA LISTA==='.format(arquivo))

def abrirRobo(tipo, file, path):
    # threading.current_thread().name
    robo = None
    if (tipo == '1'):
        robo = Abertura()
    elif (tipo == '2'):
        robo = Volumetria()
    # elif (tipo == '3'):
    #     robo = Atualizacao()
    # elif (tipo == '4'):
    #     robo = Fechamento()
    try:
        robo.controle(file, path)
    except:
        pass


#============================ ROBO PRINCIPAL==============================

localRobot        = os.getcwd() # obtem o caminho do Robô
local_OpenFolder  = os.getcwd() + "\\abertura.py"    # obtem o caminho do script Abertura de pastas
local_Volumetria  = os.getcwd() + "\\Volumetria.py"  # obtem o caminho do script Volumetria de pastas
local_Update      = os.getcwd() + "\\atualizacao.py" # obtem o caminho do script Atualização de pastas
local_CloseFolder = os.getcwd() + "\\fechamento.py"  # obtem o caminho do script Encerramento de pastas

OpenFolderPath    = os.getcwd() + "\\files\\abertura_pastas" # obtem o caminho do script e add a pasta abertura_pastas
VolumetriaPath    = os.getcwd() + "\\files\\volumetrias"     # obtem o caminho do script e add a pasta abertura_pastas
UpdatePath        = os.getcwd() + "\\files\\atualizacao"     # obtem o caminho do script e add a pasta abertura_pastas
ClosePath         = os.getcwd() + "\\files\\fechamento"      # obtem o caminho do script e add a pasta abertura_pastas

executeRobot = None
executingFiles =  {}
while True:      #Fará looping infinito, buscando novos arquivos nas pastas - se encontrar, abrirá o seu respectivo script
    time.sleep(3)
    print('{} - {} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(date.today(), time.strftime("%H:%M:%S")))
    checkIFexecuting()
    files =  {}
    # filesInFolder = set(glob.glob("{}\\*.xls*".format(OpenFolderPath))) - set(glob.glob("{}\\*.txt".format(OpenFolderPath)))

    #criar uma lista/dicionario contendo os dados dos scripts e executá-los no FOR(1 for)
    for file in glob.glob("{}\\*.xls*".format(OpenFolderPath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            if (fileName not in executingFiles):
                files[OpenFolderPath] = fileName

    for file in glob.glob("{}\\*.xls*".format(VolumetriaPath)):
        if (file[-3:] != 'txt'):
            fileName = file.split("\\")
            fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
            if (fileName not in executingFiles):
                files[VolumetriaPath] = fileName

    # for file in glob.glob("{}\\*.xls*".format(UpdatePath)):
    #     if (file[-3:] != 'txt'):
    #         fileName = file.split("\\")
    #         fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
    #         if (fileName not in executingFiles):
    #             files[UpdatePath] = fileName

    # for file in glob.glob("{}\\*.xls*".format(ClosePath)):
    #     if (file[-3:] != 'txt'):
    #         fileName = file.split("\\")
    #         fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo
    #         if (fileName not in executingFiles):
    #             files[ClosePath] = fileName
    
    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            localPid = localFile + "\\pIDs"

            infoLog = "\\EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
            infoLog = localFile + infoLog
            try:
                for fileEpid in glob.glob("{}\\*.pid".format(localPid)):
                    pId = fileEpid.split("__")
                    pId = int (pId[-1].replace(".pid", ""))
                    if (not(rf.checkPID(pId))): #se pID não está em execução. remover arquivos
                        pidFile = localPid+"\\{}__{}.pid".format(file[:-5].upper(), pId)
                        os.remove(pidFile)
                        print("Removido o PID: {}".format(pId))
                        try:
                            os.remove(infoLog)
                        except:
                            pass
            except:
                pass
            print("\n{} - {} - Uma nova instancia de {} foi aberta".format(date.today(), time.strftime("%H:%M:%S"), folderName.upper()))
            arquivo = open(infoLog, 'w+')
            arquivo.close()
            executingFiles[file] = infoLog
            if (folderName == "abertura_pastas"):
                executeRobot = threading.Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("1", file, localFile))
            elif (folderName == "volumetrias"):
                executeRobot = threading.Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("2", file, localFile))
            # elif (folderName == "atualizacao"):
            #     executeRobot = threading.Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("3", file))
            # elif (folderName == "fechamento"):
            #     executeRobot = threading.Thread(name='Executa_{}_{}'.format(folderName, file.upper()), target=abrirRobo, args=("4", file))

            try:
                executeRobot.start()
                print(executeRobot.name,'\n')
            except Exception as err:
                print('\n ERRO EM {}'.format(executeRobot.name))
                pass