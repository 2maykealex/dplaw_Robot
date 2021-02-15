from os import path
from os import getcwd
from os import mkdir
from time import strftime
from psutil import pid_exists
from pyexcel import get_sheet
from sys import exc_info

def checkLogin(tipo=''):
    checarTeste = checkIfTest()
    if (checarTeste or tipo=='atualizacao'):
        print('\n------------EM MODO DE TESTE------------')
        login="robo@dplaw.com.br"
        password="dplaw00612"
    else:
        login="cgst@dplaw.com.br"
        password="gestao0"

    print("\n-----------------------------------------")
    print("Login utilizado: {}".format(login))
    print("-----------------------------------------\n")
    return login, password

def checkIfTest():
    pathRootScript = path.dirname(path.realpath(__file__))
    pathFileTeste = pathRootScript + "\\teste.txt"
    if (path.isfile(pathFileTeste)):
        return True
    else:
        return False

def abreArquivo(fileName):
    try:
        arquivo =  open(fileName, 'r')
        message = arquivo.readlines()
        arquivo.close()
        return message[-1]
    except:
        pass

def checkEndFile(log):
    arquivo =  open(log, 'r')
    message = arquivo.readlines()
    countLines = len(message)
    arquivo.close()

    lastLine = None
    if (countLines == 1):
        lastLine = 'REG 1'
    else:
        ultimaLinha = message[ len(message) - 1].split(';')[0].strip()
        if ('FIM' in ultimaLinha):
                lastLine = 'FIM'
        elif ('CONFERENCIA' in ultimaLinha):
            lastLine = 'CONF REG 1'
        elif ('CONF REG' in ultimaLinha):
            lastLine = "CONF REG {}".format( int( ultimaLinha.split(' ')[-1] ) + 1 )
        else:
            lastLine = "REG {}".format( int( ultimaLinha.split(' ')[-1] ) + 1 )
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
    numTamanho = len(numProcessCNJ)
    if (numTamanho > 20):   #se maior que 20, obter até o caracter n.º 20
        numProcessCNJ = numProcessCNJ[:20]
    elif (numTamanho < 20): # se menor que 20, incrementar ZEROS no início até que complete 20 caracteres
        qtdZero = 20 - numTamanho
        for _x in range(qtdZero):
            numProcessCNJ = "0{}".format(numProcessCNJ)
    numProcessCNJ = '{}-{}.{}.{}.{}.{}'.format(numProcessCNJ[:7], numProcessCNJ[7:9], numProcessCNJ[9:13], numProcessCNJ[13:14], numProcessCNJ[14:16], numProcessCNJ[16:20])
    if (numProcessCNJ == '-....'):
        numProcessCNJ = ''
    return numProcessCNJ.strip()

def getTodayTime():
    hoje = "%s" % (strftime("%Y-%m-%d"))
    hoje = hoje.replace('-', '_')
    hora = strftime("%H:%M:%S")
    hora = hora.replace(':', '_')
    return (hoje, hora)