# -*- coding: utf-8 -*-

import crypt


def testPass(cryptPass):
    """ Funcao para testar as senhas do dicionario """

    # Faz um split na string da senha criptografada e separa o salt
    salt = cryptPass.split('$')[2]

    # Separa a senha criptografada
    ctype = cryptPass.split('$')[1]

    # cria o insalt para a senha, juntando a senha criptgrafada e o salt, separados por $, um padrao de senhas criptografadas no linux
    insalt = '$' + ctype + '$' + salt + '$'

    # Abre um arquivo com um dicionario de senhas
    dictFile = open('dictionary.txt', 'r')

    # Loopa as linhas do dicionario de senhas
    for word in dictFile.readlines():

        # Separa uma linha no dicionario de senhas separando por \n, um indicador de quebra de linha em arquivo de texto
        word = word.strip('\n')

        # Usa a lib de criptografia do python para criptografar as palavras do dicionario de senha
        # Utiliza o insalt criado a partir do salt e a senha criptgrafada
        cryptWord = crypt.crypt(word, insalt)

        # Se a senhas coincidirem, foi descoberta a senha
        if cryptWord == cryptPass:
            print('[+] Found Password: {} \n'.format(word))
            return

    # Se loopar todo o dicionaro de senha, nao deu match com o dicionario de senhas
    print('[-] Password Not Found.\n')
    return


def main():
    """ Funcao principal """

    # Abre o arquivo com as linhas de um /etc/passwd do linux
    passFile = open('passwords.txt')

    # Loopa as linhas do arquivo com as senhas ah serem quebradas
    for line in passFile.readlines():
        # Se tem : na linha da senha pode ser uma linha do passwd valida
        if ':' in line:
            # faz um split e separa o usuario
            user = line.split(':')[0]
            # Separa a string da senha criptgrafada
            cryptPass = line.split(':')[1].strip(' ')
            print('[*] Cracking Password For: {}'.format(user))
            # Chama a funcao para testar
            testPass(cryptPass)


if __name__ == '__main__':
    main()
