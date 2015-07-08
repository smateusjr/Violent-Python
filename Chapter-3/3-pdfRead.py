#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
from PyPDF2 import PdfFileReader


def printMeta(fileName):
    """ Abre e recupera informacoes do pdf """

    # Abre o pdf
    pdfFile = PdfFileReader(open(fileName, 'rb'))
    # Pega as informacoes do pdf
    docInfo = pdfFile.getDocumentInfo()
    print('[*] PDF MetaData For: %s' % str(fileName))
    # Se existir informacoes retorna
    if docInfo:
        # Loopa as informacoes do pdf
        for metaItem in docInfo:
            print('[+] %s:%s' % (metaItem, docInfo[metaItem]))
    else:
        print('[+] No Document Info')


def main():
    """Funcao principal """

    # Separa os parametros solicitados
    parser = optparse.OptionParser('usage %prog -F <PDF file name>')
    parser.add_option('-F', dest='fileName', type='string', help='specify PDF file name')

    # Faz o parse dos parametros
    (options, args) = parser.parse_args()

    # Se nao receber os parametros solicitados para o script
    fileName = options.fileName
    if not fileName:
        print(parser.usage)
        exit(0)
    else:
        # Chama a funcao de leitura do pdf
        printMeta(fileName)

# Chama a funcao main principal
if __name__ == '__main__':
    main()
