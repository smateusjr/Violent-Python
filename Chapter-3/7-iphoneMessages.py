#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sqlite3
import optparse


def isMessageTable(iphoneDB):
    """ Funcao que verifica se arquivo passado eh uma tabela de mensagem do bkp do iphone """

    try:
        # Conecta via sqlite no arquivo de base de dados
        conn = sqlite3.connect(iphoneDB)
        c = conn.cursor()
        # Faz o select no banco
        c.execute('SELECT tbl_name FROM sqlite_master WHERE type=="table";')

        # Se achar a palavra message eh um arquivo valido
        for row in c:
            if 'message' in str(row):
                return True
    except:
        return False


def printMessage(msgDB):
    """ Funcao que imprime as mensagem do bkp do iphone """

    try:
        # Conecta via sqlite no arquivo de base de dados
        conn = sqlite3.connect(msgDB)
        c = conn.cursor()
        # Faz o select no banco
        c.execute('select datetime(date,"unixepoch"), address, text from message WHERE address>0;')

        # Imprime o resultado
        for row in c:
            date = str(row[0])
            addr = str(row[1])
            text = row[2]
            print('\n[+] Date: %s , Addr: %s, Message: %s' % (date, addr, text))
    except:
        pass


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -p <iPhone Backup Directory>')

    # Separa os parametros solicitados
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    pathName = options.pathName

    # Se nao receber os parametros solicitados para o script
    if not pathName:
        print(parser.usage)
        exit(0)
    else:
        # Loopa todos os arquivos do diretorio informado via parametro
        dirList = os.listdir(pathName)
        for fileName in dirList:
            # Concatema o caminho passado via parametro com os arquivos encontrados
            iphoneDB = os.path.join(pathName, fileName)
            # Verifica se o arquivo encontrado eh uma tabela de bkp do message do iphone
            if isMessageTable(iphoneDB):
                try:
                    print('\n[*] --- Found Messages ---')
                    # Chama a funcao que imprime as mensagens encontradas
                    printMessage(iphoneDB)
                except:
                    pass

# Chama a funcao main principal
if __name__ == '__main__':
    main()
