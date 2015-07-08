#!/usr/bin/python
# -*- coding: utf-8 -*-

import nmap
import optparse


def nmapScan(tgtHost, tgtPort):
    """ Funcao para fazer o scaneamento utilizando o Nmap """

    # Cria um objeto Nmap
    nmScan = nmap.PortScanner()
    # Faz o scaneamento no host e na porta informada
    nmScan.scan(tgtHost, tgtPort)
    # Verifica o estado do servico pela porta
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    # Imprimi o resultado
    print('[*] %s tcp %s %s' % (tgtHost, tgtPort, state))


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
    for tgtPort in filter(None, tgtPorts):
        nmapScan(options.tgtHost, tgtPort)

# Chama a funcao main principal
if __name__ == '__main__':
    main()
