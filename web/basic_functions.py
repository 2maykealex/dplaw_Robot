from os import path
from os import getcwd
from os import mkdir
from psutil import pid_exists
from pyexcel import get_sheet

def checkLogin():
    checarTeste = checkIfTest()
    if (checarTeste):
        print('\n------------EM MODO DE TESTE------------')
        login="robo@dplaw.com.br"
        password="dplaw00612"
    else:
        login="cgst@dplaw.com.br"
        password="gestao0"
    return login, password

def checkIfTest():
    pathRootScript = path.abspath(path.dirname(__file__))
    pathFileTeste = pathRootScript + "\\teste.txt"
    if (path.isfile(pathFileTeste)):
        return True
    else:
        return False

def abreArquivo(arquivo, extensao, path=""):
    fileName = "{}\\{}.{}".format(path, arquivo, extensao)
    # fileName = (arquivo + '.' + extensao)
    dfExcel = get_sheet(file_name=fileName)
    return dfExcel

def checkEndFile(log):
    try:
        arquivo =  open(log, 'r')
        message = arquivo.readlines()
        arquivo.close()
        lastLine = message[len(message)-1]
    except:
        lastLine = 1
    return (lastLine)

def createLog(logFile, message = "", tipo = 'w+', printOut = True, onlyText=False):
    if (path.isfile(logFile)): #se o log não existir, cria-se
        arquivo =  open(logFile, 'a')
    else:
        arquivo = open(logFile, tipo)
    writeLog = "{}".format(message)
    if (arquivo != ""):
        arquivo.writelines(writeLog)
    if (printOut):
        print(writeLog)
    arquivo.close()

def createFolder(folder):
    if (not(path.exists(folder))):
        mkdir(folder)

def createPID(pidName, pidNumber):
    logsPath = "{}\\pIDs".format(getcwd())
    logFile = logsPath +"\\{}__{}.pid".format(pidName, pidNumber)

    if (path.exists(logsPath) == False):
        mkdir(logsPath)   # Se o diretório pIDs não existir, será criado

    if (not(path.isfile(logFile))): #se o log não existir, cria-se
        arquivo =  open(logFile, 'w')
        arquivo.close()
        return True

def checkPID(pidNumber):
    if pid_exists(pidNumber):
        print ("pid {} existe".format(pidNumber))
        return True

def ajustarNumProcessoCNJ(numProcessCNJ):
    try:
        numProcessCNJ = numProcessCNJ.replace('.', '')
        numProcessCNJ = numProcessCNJ.replace('-', '')
    except:
        pass
    num = len(numProcessCNJ)
    if (num > 20):   #se maior que 20, obter até o caracter n.º 20
        numProcessCNJ = numProcessCNJ[:20]
    elif (num < 20): # se menor que 20, incrementar ZEROS no início até que complete 20 caracteres
        qtdZero = 20 - len(numProcessCNJ)
        for _x in range(qtdZero):
            numProcessCNJ = "0{}".format(numProcessCNJ)
    numProcessCNJ = '{}-{}.{}.{}.{}.{}'.format(numProcessCNJ[:7], numProcessCNJ[7:9], numProcessCNJ[9:13], numProcessCNJ[13:14], numProcessCNJ[14:16], numProcessCNJ[16:20])
    if (numProcessCNJ == '-....'):
        numProcessCNJ = ''
    return numProcessCNJ
