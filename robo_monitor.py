import os
import time
import glob

#============================ ROBO PRINCIPAL==============================

localRobot        = os.getcwd() # obtem o caminho do Robô
local_OpenFolder  = os.getcwd() + "\\inturn.py" # obtem o caminho do script Abertura de pastas
local_Volumetria  = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Volumetria de pastas
# local_Update      = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Atualização de pastas
# local_CloseFolder = os.getcwd() + "\\Volumetria.py" # obtem o caminho do script Encerramento de pastas

OpenFolderpath = os.getcwd() + "\\files\\abertura_pastas" # obtem o caminho do script e add a pasta abertura_pastas

while True: #Fará looping infinito, buscando novos arquivos nas pastas - se encontrar, abrirá o seu respectivo script
    files =  []
    for file in glob.glob("{}\\*.xlsx".format(OpenFolderpath)):
        files.append(file)
    
    if (files):
        for file in files:
            fileName = file.split("\\")
            fileName = fileName[-1]

            infoLog = "\\EXECUTANDO {}.txt".format(fileName.upper())  #criando o nome do arquivo INFOLOG
            logFile = OpenFolderpath + infoLog

            hora = time.strftime("%H:%M:%S")
            if (not(os.path.isfile(logFile))):  #se o log não existir - executa o arquivo no script
                print("{} - Uma nova instancia de Abertura de pastas foi aberta")
                os.startfile('inturn.py')   #executa outro script em outro terminal - para trabalhar de forma isolada
            else:
                print('{} - Arquivo em execução!'.format(hora))
            
            time.sleep(10) #Colocado um delay para o outro script gerar o arquivo de log e não abrir outro webdriver