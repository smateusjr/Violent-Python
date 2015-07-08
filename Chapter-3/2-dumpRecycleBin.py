#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from winreg import *


def sid2user(sid):
    """ Recupera o usuario, procurando no registro do windows """

    try:
        # Abre a registros do windows pelo sid informado
        key = OpenKey(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\\%s' % (sid))
        # Recupea o tipo e o valor do registro
        (value, type) = QueryValueEx(key, 'ProfileImagePath')
        # Divide a valor do registro e pega o usuario
        user = value.split('\\')[-1]
        return user
    except:
        return sid


def returnDir():
    """ Funcao para verificar qual o caminho absoluto da lixeira """

    # Lista com os possiveis caminhos
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']

    # Loopa os possivel caminhos da lixeira
    for recycleDir in dirs:
        # Se o caminho informado existir, encontro
        if os.path.isdir(recycleDir):
            # Retorna o caminho, caso exista
            return recycleDir
    return None


def findRecycled(recycleDir):
    """ Funcao para listar os arquivos da lixeira """

    # Pega todo os diretorios da lixeira
    dirList = os.listdir(recycleDir)
    # Loopa todo os diretorios da lixeira
    for sid in dirList:
        # Lista todos os diretorios da lixeira
        files = os.listdir(recycleDir + sid)
        # Chama a funcao que pega o usuario
        user = sid2user(sid)
        print('\n[*] Listing Files For User: %s' % str(user))
        for file in files:
            print('[+] Found File: %s' % str(file))


def main():
    """Funcao principal """

    # Chama a funcao que encontra o diretorio da lixeira
    recycledDir = returnDir()
    # Chama a funcao que lista os arquivos da lixeira
    findRecycled(recycledDir)


# Chama a funcao main principal
if __name__ == '__main__':
    main()
