#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import mechanicalsoup
import re

# Funciona apenas no windows, esse pacote nao existe no linux
from winreg import *


def val2addr(val):
    """ Funcao para validar o Mac encontrado """

    addr = ''
    # Loopa os Macs encontrados
    # Transforma todos os MACs encontrados em uma unica string
    for ch in val:
        addr += '%02x ' % ord(ch)
    # Cria uma lista com os MACs encontrados
    addr = addr.strip(' ').replace(' ', ':')[0:17]
    return addr


def wiglePrint(username, password, netid):
    """ Funcao para logar no wiglet e encontrar a lat e log da rede informada """

    # Cria um objeto do mechanicalsoup para abrir um site
    browser = mechanicalsoup.Browser()

    # Abre a pagina de login do wigle
    login_page = browser.get('https://wigle.net/login')

    # Procura no html da pagina de login a div com a classe 'loginBox'
    # Dentro da div, procura o formulario de login
    login_form = login_page.soup.select('.loginBox')[0].select('form')[0]

    # Seta o login e senha para o formulario encontrado
    login_form.select('#cred0')[0]['value'] = username
    login_form.select('#cred1')[0]['value'] = password

    # Envia o formulario e para logar no wigle
    login = browser.submit(login_form, login_page.url)

    # Verifica o retorno da tentativa de login
    if login.soup.find('div', class_='pageLogoDiv'):
        return

    # Abre a pagina de busca do wigle
    search_page = browser.get('https://wigle.net/search')

    # Procura uma div com o id 'detaillocationDiv'
    # Dentro da div, procura o formulario de busca
    search_form = search_page.soup.select('#detaillocationDiv')[0].select('form')[0]

    # Seta o mac da rede para a busca no input text de id 'netidloc'
    search_form.select('#netidloc')[0]['value'] = netid

    # Envia o formulario de busca
    search = browser.submit(search_form, search_page.url)

    rLat = 'N/A'
    rLon = 'N/A'

    resp = search.soup.select('#test')[0]
    # Busca dentro a tabela a latitude
    rLat = re.findall('Est. Latitude</th><td>(.*?)</td>', resp)
    # Busca dentro a tabela a latitude
    rLon = re.findall('Est. Longitude</th><td>(.*?)</td>', resp)

    print('[-] Lat: %s, Lon: %s' % (rLat[0], rLon[0]))


def printNets(username, password):
    """ Pesquisa as redes no registro do windows """

    # Faz uma pesquisa na suas redes nos registros do windows
    net = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkList\\Signatures\\Unmanaged'
    # Abre o registro encontrado
    key = OpenKey(HKEY_LOCAL_MACHINE, net)
    print('\n[*] Networks You have Joined.')
    for i in range(100):
        try:
            # Cria um indice numerico para os subregistros do registro informado
            guid = EnumKey(key, i)
            # Abre um registro do windows
            netKey = OpenKey(key, str(guid))
            # Cria um indice numerico para o registro informado
            (n, addr, t) = EnumValue(netKey, 5)
            (n, name, t) = EnumValue(netKey, 4)
            # Chama a funcao para validar os mac encontrados
            macAddr = val2addr(addr)
            # Transforma o nome da rede em string
            netName = str(name)
            print('[+] %s   %s' % (netName, macAddr))
            # Chama a funcao para logar no wigle
            wiglePrint(username, password, macAddr)
            # Fecha o registro
            CloseKey(netKey)
        except:
            break


def main():
    """ Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -u <wigle username> -p <wigle password>')

    # Separa os parametros solicitados
    parser.add_option('-u', dest='username', type='string', help='specify wigle password')
    parser.add_option('-p', dest='password', type='string', help='specify wigle username')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    username = options.username
    password = options.password

    # Se nao receber os parametros solicitados para o script
    if not username or not password:
        print(parser.usage)
        exit(0)
    else:
        # Chama a funcao para pesquisar as redes no registro do windows
        printNets(username, password)

# Chama a funcao main principal
if __name__ == '__main__':
    main()
