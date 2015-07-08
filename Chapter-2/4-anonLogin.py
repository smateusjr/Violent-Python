#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib


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

# Host alvo para o login anonimo
host = '192.168.56.107'
# Chama a funcao de conecao via FTP anonimo
anonLogin(host)
