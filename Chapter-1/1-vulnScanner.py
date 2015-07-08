# -*- coding: utf-8 -*-

import socket
import os
import sys


def retBanner(ip, port):
    """ Funcao que conecta via socket em um servico """

    try:
        # Seta um time out para a conexao
        socket.setdefaulttimeout(2)
        # Abre uma conexao
        s = socket.socket()
        # Faz a conexao com a o ip e a porta
        s.connect((ip, port))
        # Pega o banner de retorno se conectar
        banner = s.recv(1024).decode('utf-8').lower()
        # Retorna o banner
        return banner
    except:
        # Com o try, o erro de conexao cai na exception e informa que nao tem a vulnerabilidade
        print('[-] not connection [port {}].'.format(port))
        return


def checkVulns(banner, filename):
    """ Verifica se o banner retornado esta na lista de vulnerabilidade """

    # Abre o arquivo com a lista de banners de vulnerabilidade
    f = open(filename, 'r')
    # Loopa as linha do arquivo
    for line in f.readlines():
        # Verifica se o banner passado esta na lista de vulnerabilidade
        # usa o in para fazer uma busca na string
        if line.strip('\n').lower() in banner:
            print('[+] Server is vulnerable: {}'.format(banner))


def main():
    """ Funcao principal """

    # Obrigatorio passar 2 argumentos como parametro
    if len(sys.argv) == 2:
        # Pega o nome do arquivo passado por parametro
        filename = sys.argv[1]

        # Valida se o arquivo passado realmente existe
        if not os.path.isfile(filename):
            print('[-] {} does not exist.'.format(filename))
            exit(0)

        # Verifica se o python tem acesso ao arquivo passado por parametro
        if not os.access(filename, os.R_OK):
            print('[-] {} access denied.'.format(filename))
            exit(0)
    else:
        print('[-] Usage: {} <vuln filename>'.format(str(sys.argv[0])))
        exit(0)
    # Lista com as porta a serem scaneadas
    portList = [21, 22, 25, 80, 110, 443]
    # Loopa um range de ips
    for x in range(103, 104):
        # ip base ah ser scaneado
        ip = '192.168.56.%s' % (str(x))

        # Loopa as portas ah serem scaneadas
        for port in portList:
            # Faz a busca do banner do servico
            banner = retBanner(ip, port)
            # Se existe algum servico que restorne o banner faz a busca em nossa lista de vunerabilidade
            if banner:
                print('[+] {} : {}'.format(ip, banner))
                # Verifica se o banner retornado esta em nossa lista de vunerabilidade
                checkVulns(banner, filename)

if __name__ == '__main__':
    main()
