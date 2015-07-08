#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib


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


# Parametros para conexao no host alvo
host = '192.168.56.107'
userName = 'sergio'
passWord = '123123'

# Cria um objeto de ftp para conexao
ftp = ftplib.FTP(host)
# Loga via ftp usando os parametros informados
ftp.login(userName, passWord)
# Chama a funcao de procura de paginas default
returnDefault(ftp)
