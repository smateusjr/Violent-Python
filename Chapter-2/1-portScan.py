#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
from socket import *
from threading import *

# Cria um novo objeto de thread caso solicitado pelo acquire()
screenLock = Semaphore(value=1)


def connScan(tgtHost, tgtPort):
    """ Funcao para conectar no host alvo """

    try:
        # Cria um INET, STREAMing socket
        connSkt = socket(AF_INET, SOCK_STREAM)
        # Conecta no host e na porta informada
        connSkt.connect((tgtHost, tgtPort))
        # Envia uma mensagem (em bytes devido ao python 3) via TCP
        connSkt.send(bytes('ViolentPython'.encode('utf-8')))
        # Espera um reposta
        results = connSkt.recv(100)
        # Adiquire um block, blocking ou nom-blocling para a thred em semaforo
        screenLock.acquire()

        print('[+] %d/tcp open' % (tgtPort))
        print('[+] %s' % (results.decode()))

    except:
        # Adiquire um block, blocking ou nom-blocling para a thred em semaforo
        screenLock.acquire()
        print('[-] %d/tcp closed' % (tgtPort))

    finally:
        # libera a thread
        screenLock.release()
        # Fecha a conexao do socket
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    """ Funcao para scanear portas """

    try:
        # Busca o Ip (ipv4) do alvo utilizando o hostname, caso informado
        tgtIP = gethostbyname(tgtHost)
    except:
        print('[-] Cannot resolve "%s": Unknown host' % (tgtHost))
        return

    try:
        # Busca o hostname do alvo utilizando o IP, caso informado
        tgtName = gethostbyaddr(tgtIP)

        # Mostra o host do alvo utilizando o IP ou o hostname
        print('\n[+] Scan Results for: %s' % (tgtName[0]))
    except:
        print('\n[+] Scan Results for: %s' % (tgtIP))

    # Seta um time out de 1 segundo
    setdefaulttimeout(1)

    # Loopa as portas informadas por parametro
    for tgtPort in tgtPorts:
        # Cria uma thread chamando a funcao de conectar e passando o Host e a porta como parametro
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        # Inicia a thread
        t.start()


def main():
    """Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>,<target port>,<target port>')

    # Separa os parametros solicitados
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()

    # Se nao receber os parametros solicitados para o script
    if not options.tgtHost or not options.tgtPort:
        print(parser.usage)
        exit(0)

    # Separa as portas em uma lista e remove os espacos
    tgtPorts = options.tgtPort.replace(" ", '').split(',')

    # Chama a funcao de scaneamento de portas, limpa a lista de portas removendo string vazias com o filter
    portScan(options.tgtHost, filter(None, tgtPorts))

# Chama a funcao main principal
if __name__ == '__main__':
    main()
