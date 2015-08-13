#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import optparse
import os
import sqlite3


def printDownloads(downloadDB):
    """ Funcao que imprime os downloads realizados no firefox """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(downloadDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('SELECT name, source, datetime(endTime/1000000,"unixepoch") FROM moz_downloads;')
    print('\n[*] --- Files Downloaded --- ')

    # Imprime o resultado
    for row in c:
        print('[+] File: %s from source: %s at: %s' % (str(row[0]), str(row[1]), str(row[2])))


def printCookies(cookiesDB):
    """ Funcao que imprime os cookies do firefox """

    try:
        # Conecta via sqlite no arquivo de base de dados
        conn = sqlite3.connect(cookiesDB)
        c = conn.cursor()
        # Faz o select no banco
        c.execute('SELECT host, name, value FROM moz_cookies')

        print('\n[*] -- Found Cookies --')

        # Imprime o resultado
        for row in c:
            host = str(row[0])
            name = str(row[1])
            value = str(row[2])
            print('[+] Host: %s, Cookie: %s, Value: %s' % (host, name, value))

    # Exception com o erro
    except Exception as e:
        if 'encrypted' in str(e):
            print('\n[*] Error reading your cookies database.')
            print('[*] Upgrade your Python-Sqlite3 Library')


def printHistory(placesDB):
    """ Funcao que imprime o historico do firefox """

    try:
        # Conecta via sqlite no arquivo de base de dados
        conn = sqlite3.connect(placesDB)
        c = conn.cursor()
        # Faz o select no banco
        c.execute('select url, datetime(visit_date/1000000, "unixepoch") from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;')

        print('\n[*] -- Found History --')

        # Imprime o resultado
        for row in c:
            url = str(row[0])
            date = str(row[1])
            print('[+] %s - Visited: %s' % (date, url))

    # Exception com o erro
    except Exception as e:
        if 'encrypted' in str(e):
            print('\n[*] Error reading your places database.')
            print('[*] Upgrade your Python-Sqlite3 Library')
            exit(0)


def printGoogle(placesDB):
    """ Funcao que imprime o historico do firefox """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(placesDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('select url, datetime(visit_date/1000000, "unixepoch") from moz_places, moz_historyvisits where visit_count > 0 and moz_places.id==moz_historyvisits.place_id;')

    print('\n[*] -- Found Google --')

    # Imprime o resultado
    for row in c:
        url = str(row[0])
        date = str(row[1])
        # Se encontrar alguma pesquisa por google faz um parser e separa o que foi pesquisado
        if 'google' in url.lower():
            # Faz um parser e separa o que foi pesquisado
            r = re.findall(r'q=.*\&', url)
            # Se econtrar alguma coisa imprime
            if r:
                search = r[0].split('&')[0]
                search = search.replace('q=', '').replace('+', ' ')
                print('[+] %s  - Searched For: %s' % (date, search))


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -p <firefox profile path>')

    # Separa os parametros solicitados
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    pathName = options.pathName

    # Se nao receber os parametros solicitados para o script
    if not pathName:
        print(parser.usage)
        exit(0)
    # Se nao for passado um caminho para os arquivos de banco
    elif not os.path.isdir(pathName):
        print('[!] Path Does Not Exist: %s' % (pathName))
        exit(0)
    else:
        # Concatena o caminho com o arquivo de banco com os downloads do firefox
        downloadDB = os.path.join(pathName, 'downloads.sqlite')
        # Se existir o arquivo, faz a chamada da funcao
        if os.path.isfile(downloadDB):
            # Chama a funcao que imprimir os download realizados no firefox
            printDownloads(downloadDB)
        else:
            print('[!] Downloads Db does not exist: %s' % (downloadDB))

        # Concatena o caminho com o arquivo de banco dos cookies do firefox
        cookiesDB = os.path.join(pathName, 'cookies.sqlite')
        # Se existir o arquivo, faz a chamada da funcao
        if os.path.isfile(cookiesDB):
            # Chama a funcao que imprimir os cookies do firefox
            printCookies(cookiesDB)
        else:
            print('[!] Cookies Db does not exist:' % (cookiesDB))

        # Concatena o caminho com o arquivo de banco dos cookies do firefox
        placesDB = os.path.join(pathName, 'places.sqlite')
        # Se existir o arquivo, faz a chamada da funcao
        if os.path.isfile(placesDB):
            # Chama a funcao que imprimir o historico do firefox
            printHistory(placesDB)
            # Chama a funcao que imprimir oas pequisar realizadas no google pelo firefox
            printGoogle(placesDB)
        else:
            print('[!] PlacesDb does not exist: ' % (placesDB))

# Chama a funcao main principal
if __name__ == '__main__':
    main()
