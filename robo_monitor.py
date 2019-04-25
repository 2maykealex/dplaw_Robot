import os
import time
import glob
import robot_functions as rf

#============================ ROBO PRINCIPAL==============================

localRobot        = os.getcwd() # obtem o caminho do Robô
local_OpenFolder  = os.getcwd() + "\\inturn.py" # obtem o caminho do script Abertura de pastas
local_Volumetria  = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Volumetria de pastas
# local_Update      = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Atualização de pastas
# local_CloseFolder = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Encerramento de pastas

OpenFolderPath = os.getcwd() + "\\files\\abertura_pastas" # obtem o caminho do script e add a pasta abertura_pastas
VolumetriaPath = os.getcwd() + "\\files\\volumetrias" # obtem o caminho do script e add a pasta abertura_pastas

while True: #Fará looping infinito, buscando novos arquivos nas pastas - se encontrar, abrirá o seu respectivo script
    time.sleep(3)
    hora = time.strftime("%H:%M:%S")
    print('{} - VERIFICANDO SE HÁ NOVOS ARQUIVOS!'.format(hora))
    
    files =  {}
    for file in glob.glob("{}\\*.xlsx".format(OpenFolderPath)):
        fileName = file.split("\\")
        fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo        
        files[OpenFolderPath] = fileName

    for file in glob.glob("{}\\*.xlsx".format(VolumetriaPath)):
        fileName = file.split("\\")
        fileName = fileName[-1] #obtem o ultimo elemento da lista, no caso, o nome do arquivo        
        files[VolumetriaPath] = fileName
    
    if (files):
        for localFile, file in files.items():
            folderName = localFile.split("\\")
            folderName = folderName[-1]
            localPid = localFile + "\\pIDs"

            infoLog = "\\EXECUTANDO {}.txt".format(file.upper())  #criando o nome do arquivo INFOLOG
            logFile = localFile + infoLog

            try:
                for fileEpid in glob.glob("{}\\*.pid".format(localPid)):
                    pId = fileEpid.split("__")
                    pId = int (pId[-1].replace(".pid", ""))
                    if (not(rf.checkPID(pId))): #se pID não está em execução. remover arquivos
                        pidFile = localPid+"\\{}__{}.pid".format(file[:-5].upper(), pId)
                        os.remove(pidFile)
                        os.remove(logFile)
                        print("Removido o PID: {}".format(pId))
            except:
                pass

            if (not(os.path.isfile(logFile))):  #se o log não existir - executa o arquivo no script
                print("{} - Uma nova instancia de {} foi aberta".format(hora, folderName.upper()))
                if (folderName == "abertura_pastas"):
                    os.startfile('inturn.py')   #executa outro script em outro terminal - para trabalhar de forma isolada
                elif (folderName == "volumetrias"):
                    os.startfile('volumetria.py')   #executa outro script em outro terminal - para trabalhar de forma isolada
            else:
                print('{} - Arquivo {} já está em execução!'.format(hora, file))
            
            time.sleep(10) #Colocado um delay para o outro script gerar o arquivo de log e não abrir outro webdriver