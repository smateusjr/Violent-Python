#!/usr/bin/python
# -*- coding: utf-8 -*-

import pxssh


def send_command(s, cmd):
    """ Funcao para enviar comandos ao host alvo """

    # Envia um comando para o host via ssh
    s.sendline(cmd)
    # Chama o prompt
    s.prompt()
    # Se o resultado for em bytes faz um decode, se for string imprime direto
    print('%s' % (s.before.decode() if isinstance(s.before, bytes) else s.before))


def connect(host, user, password):
    """ Funcao para conectar no host alvo """

    try:
        # Cria um objeto da classe pxssh para conexao via ssh
        s = pxssh.pxssh()
        # Tenta realizar o login no alvo
        s.login(host, user, password)
        # Retorna a estancia da conexao
        return s
    except:
        print('[-] Error Connecting')
        exit(0)

# Chama a funcao de conexao passando os parametros do host alvo
s = connect('127.0.0.1', 'root', 'toor')
# Chama a funcao que envia comandos para o host alvo
send_command(s, 'cat /etc/shadow | grep root')
