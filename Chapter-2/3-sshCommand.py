#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect

PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_command(child, cmd):
    """ Funcao para enviar comandos ao host alvo """

    # Envia um comando para o host via ssh
    child.sendline(cmd)
    # Espera uma resposta do prompt
    child.expect(PROMPT)
    # Se o resultado for em bytes faz um decode, se for string imprime direto
    print(child.before.decode() if isinstance(child.before, bytes) else child.before)


def connect(user, host, password):
    """ Funcao para conectar via ssh no host alvo """

    ssh_newkey = 'Are you sure you want to continue connecting'
    # Comando ssh com os parametros de conexao
    connStr = 'ssh {user}@{host}'.format(user=user, host=host)
    # tenta conectar informando o comando ssh
    child = pexpect.spawn(connStr)
    # Aguarda alguns retorno na lista abaixo
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])

    # Se nao houver retorno retorna um erro
    if ret == 0:
        print('[-] Error Connecting')
        return

    # Se retornar 1 conseguiu conectar
    if ret == 1:
        # Informa 'yes' caso apareca:
        # Are you sure you want to continue connecting (yes/no)?
        child.sendline('yes')
        # Espera um time out ou o prompt para digitar a senha
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
        # Se nao houver retorno retorna um erro
        if ret == 0:
            print('[-] Error Connecting')
            return
    # Informa a senha
    child.sendline(password)
    # Espera o retorno de um prompt
    child.expect(PROMPT)
    # Retorna o promt aberto pronto para receber comandos
    return child


def main():
    """ Funcao principal """

    # Parametros do host alvo
    host = '192.168.56.107'
    user = 'root'
    password = 'root123'

    # Chama a funcao de conexao passando os parametros do host alvo
    child = connect(user, host, password)

    # Se conecctou, chama a funcao que envia comandos para o host alvo
    if child:
        send_command(child, 'cat /etc/shadow | grep root')

# Chama a funcao main principal
if __name__ == '__main__':
    main()
