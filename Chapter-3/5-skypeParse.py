#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import optparse
import os


def printProfile(skypeDB):
    """ Funcao que imprime os profiles da base de dados do skype """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('SELECT fullname, skypename, city, country, datetime(profile_timestamp,"unixepoch") FROM Accounts;')

    # Imprime o resultado
    for row in c:
        print('[*] -- Found Account --')
        print('[+] User           : %s' % (str(row[0])))
        print('[+] Skype Username : %s' % (str(row[1])))
        print('[+] Location       : %s, %s' % (str(row[2]), str(row[3])))
        print('[+] Profile Date   : %s' % (str(row[4])))


def printContacts(skypeDB):
    """ Funcao que imprime os contatos da base de dados do skype """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;')

    # Imprime o resultado
    for row in c:
        print('\n[*] -- Found Contact --')
        print('[+] User           : %s' % (str(row[0])))
        print('[+] Skype Username : %s' % (str(row[1])))

        if str(row[2]):
            print('[+] Location       : %s, %s' % (str(row[2]), str(row[3])))
        if str(row[4]):
            print('[+] Mobile Number  : %s' % (str(row[4])))
        if str(row[5]):
            print('[+] Birthday       : %s' % (str(row[5])))


def printCallLog(skypeDB):
    """ Funcao que imprime os contatos da base de dados do skype """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('SELECT datetime(begin_timestamp,"unixepoch"), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;')
    print('\n[*] -- Found Calls --')

    # Imprime o resultado
    for row in c:
        print('[+] Time: %s | Partner: %s' % (str(row[0]), str(row[1])))


def printMessages(skypeDB):
    """ Funcao que imprime os contatos da base de dados do skype """

    # Conecta via sqlite no arquivo de base de dados
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    # Faz o select no banco
    c.execute('SELECT datetime(timestamp,"unixepoch"), dialog_partner, author, body_xml FROM Messages;')
    print('\n[*] -- Found Messages --')

    # Imprime o resultado
    for row in c:
        try:
            if 'partlist' not in str(row[3]):
                if str(row[1]) != str(row[2]):
                    msgDirection = 'To ' + str(row[1]) + ': '
                else:
                    msgDirection = 'From ' + str(row[2]) + ' : '
                print('Time: %s %s%s' % (str(row[0]), msgDirection, str(row[3])))
        except:
            pass


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -p <skype profile path>')

    # Separa os parametros solicitados
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    pathName = options.pathName

    # Se nao receber os parametros solicitados para o script
    if not pathName:
        print(parser.usage)
        exit(0)
    # Verifica se foi passado o caminho do arquivo da base de dados do skype
    elif not os.path.isdir(pathName):
        print('[!] Path Does Not Exist: %s' % (pathName))
        exit(0)
    else:
        # Concatena o caminho com o nome do arquivo de base de dados
        skypeDB = os.path.join(pathName, 'main.db')
        # Valida se existe o caminho completo do arquivo de banco de dados do skype
        if os.path.isfile(skypeDB):
            # Chama a funcao que imprime os profiles do banco
            printProfile(skypeDB)
            # Chama a funcao que imprime os contato do banco
            printContacts(skypeDB)
            # Chama a funcao que imprime as chamadas do banco
            printCallLog(skypeDB)
            # Chama a funcao que imprime sa mensagens do banco
            printMessages(skypeDB)
        else:
            print('[!] Skype Database does not exist: %s' % (skypeDB))

# Chama a funcao main principal
if __name__ == '__main__':
    main()
