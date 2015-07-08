# -*- coding: utf-8 -*-

import zipfile
import optparse
from threading import Thread


def extractFile(zFile, password):
    """ Funcao que tenta descompactar o zip informando uma senha """

    try:
        # Faz a descompactacao e passa a senha como parametro
        zFile.extractall(pwd=password)
        # Se acertou a senha, imprimi a senha usada e transforma ela em string
        print('[+] Found password {}'.format(bytes.decode(password)))
    # Com a exception, ao tentar descompactar e nao conseguir, ja cai na exception e sai da funcao
    except:
        pass


def main():
    """ Funcao principal """

    # Informa ao usuario como deve ser chamado o script
    parser = optparse.OptionParser('usage %prog ' + '-f <zipfile> -d <dictionary>')

    # faz com que o -f seja o parametro para especificar o nome do arquivo zip
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')

    # faz com que o -d seja o parametro para especificar o arquivo com o dicionario de senhas
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')

    # Separa os paramentros nas variaveis option e args
    (options, args) = parser.parse_args()

    # Se nao foi digitado o nome de um arquivo zip e o nome de um arquivo de dicionario de senhas para o script, solicita novamente e para o script
    if (not options.zname) | (not options.dname):

        # Solicita novamente ao usuario como deve ser chamado o script e os parametros necessarios
        print(parser.usage)
        exit(0)
    else:
        # Separa o nome do zip e o nome do arquivo de dicionario de senhas
        zname = options.zname
        dname = options.dname

    # Estancia a lib de zip passando o arquivo zip como parametro
    zFile = zipfile.ZipFile(zname)

    # Abre o arquivo com o dicionario de senhas
    passFile = open(dname)

    # Loopa as linhas do dicionario de senhas
    for line in passFile.readlines():
        # Separa a senha pela quebra de linha "\n" e faz um encode para ser a variavel ficar em bytes
        password = str.encode(line.strip('\n'))
        # Faz a chamada da funcao de quebra de senha em thread para ela rodar independente do loop senhas
        # ou seja, vai ser chamado varias funcoes para quebrar senha ao mesmo tempo melhorando a performance do brute force
        t = Thread(target=extractFile, args=(zFile, password))
        # Inicia a thread
        t.start()

if __name__ == '__main__':
    main()
