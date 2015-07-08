#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import optparse
from urllib.parse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS


def findImages(url):
    """ Funcao que procura imagens em uma url """

    print('[+] Finding images on %s' % (url))
    # Abre a url informada
    urlContent = urllib.request.urlopen(url).read()
    # Faz um soup e cria um objeto
    soup = BeautifulSoup(urlContent)
    # Faz um procura pela tag img na url
    imgTags = soup.findAll('img')
    return imgTags


def downloadImage(imgTag):
    """ Funcao para baixar as imagens de uma url """

    try:
        print('[+] Dowloading image...')
        # Recupera o atributo src, da tag img, onde tem o endereco para imagem
        imgSrc = imgTag['src']
        # Abre a url da imagem
        imgContent = urllib.request.urlopen(imgSrc).read()
        # Recupera o nome da imagem
        imgFileName = basename(urlsplit(imgSrc)[2])
        # Abre/Cria um arquivo com o nome da imagem
        imgFile = open(imgFileName, 'wb')
        # Escreve todo o conteudo da imagem no arquivo criado acima, assim faz uma copia da imagem
        imgFile.write(imgContent)
        # Fecha o arquivo da imagem
        imgFile.close()
        # retorna a imagem
        return imgFileName
    except:
        return ''


def testForExif(imgFileName):
    """ Funcao que recupera inforamacoes de uma imagem """

    try:
        exifData = {}
        # Abre a imagem informada
        imgFile = Image.open(imgFileName)
        # Recupera as informacoes metadata de uma imagem
        info = imgFile._getexif()
        if info:
            # Loopa todo o conteudo encontrado
            for (tag, value) in info.items():
                # Recupera  valor e o nome da tag da metadata
                decoded = TAGS.get(tag, tag)
                # Cria um array com o nome e a valor do metadata
                exifData[decoded] = value
            # Retorna apenas o GPSInfo da imagem
            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print('[*] %s contains GPS MetaData' % (imgFileName))
    except:
        pass


def main():
    """Funcao principal """

    # Parse explicando como deve ser a chamada do script
    parser = optparse.OptionParser('usage %prog -u <target url>')
    # Separa os parametros solicitados
    parser.add_option('-u', dest='url', type='string', help='specify url address')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()
    url = options.url

    # Se nao receber os parametros solicitados para o script
    if not url:
        print(parser.usage)
        exit(0)
    else:
        # Chama a funcao que localiza as imagens da url informada
        imgTags = findImages(url)
        for imgTag in imgTags:
            # Chama a funcao que procura e faz o download das imagens na url informada
            imgFileName = downloadImage(imgTag)
            # Chama a funcao que recupera as informacoes das imagens
            testForExif(imgFileName)


# Chama a funcao main principal
if __name__ == '__main__':
    main()
