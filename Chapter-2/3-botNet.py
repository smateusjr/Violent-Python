#!/usr/bin/python
# -*- coding: utf-8 -*-

import pxssh


class Client:

    """ Classe de clients com funcoes de conexao """

    def __init__(self, host, user, password):
        """ Inicia as variaveis globais da classe """

        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        """ Funcao para conectar via ssh no alvo """
        try:
            # Cria um objeto da classe pxssh para conexao via ssh
            s = pxssh.pxssh()
            # Tenta realizar o login no alvo
            s.login(self.host, self.user, self.password)
            # Retorna a estancia da conexao
            return s
        except Exception as e:
            # Printa o erro caso nao conecte
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        """ Funcao para enviar um comando para o host alvo """

        # If para verificar se existe conexao
        if self.session:
            # Envia um comando para o host via ssh
            self.session.sendline(cmd)
            # Chama o prompt
            self.session.prompt()
            # Retorna o que eh enviado depois do prompt de comando
            return self.session.before
        return 'No conection'


def botnetCommand(command):
    """ Funcao para adicionar os comando a serem enviado ao host alvo """

    # Loopa a lista de host adicionados
    for client in botNet:
        # Cria a variavel output com o resultado da funcao send_command da classe cliente
        output = client.send_command(command)
        # imprime o resultado
        print('[*] Output from %s' % (client.host))
        # Se o resultado for em bytes faz um decode, se for string imprime direto
        print('[+] %s' % (output.decode() if isinstance(output, bytes) else output))


def addClient(host, user, password):
    """ Funcao para adicionar clientes alvos """

    # cria uma estancia da classe client e passa os parametros de conexao
    client = Client(host, user, password)
    # Adicionar la lista botNet os client alvos
    botNet.append(client)

# Lista usada para adicionar os client alvos
botNet = []
# Chama a funcao addClient com os host alvos e dados de conexao
addClient('127.0.0.1', 'root', 'toor')
addClient('127.0.0.1', 'root', 'toor')
addClient('192.168.56.107', 'sandro', '123123')

# Chama a funcao botnetCommand com os comandos
botnetCommand('uname -v')
botnetCommand('cat /etc/issue')
