#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import optparse
import os


def printProfile(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute('SELECT fullname, skypename, city, country, datetime(profile_timestamp,"unixepoch") FROM Accounts;')

    for row in c:
        print('[*] -- Found Account --')
        print('[+] User           : %s' % (str(row[0])))
        print('[+] Skype Username : %s' % (str(row[1])))
        print('[+] Location       : %s, %s' % (str(row[2]), str(row[3])))
        print('[+] Profile Date   : %s' % (str(row[4])))


def printContacts(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute('SELECT displayname, skypename, city, country, phone_mobile, birthday FROM Contacts;')

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
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute('SELECT datetime(begin_timestamp,"unixepoch"), identity FROM calls, conversations WHERE calls.conv_dbid = conversations.id;')
    print('\n[*] -- Found Calls --')

    for row in c:
        print('[+] Time: %s | Partner: %s' % (str(row[0]), str(row[1])))


def printMessages(skypeDB):
    conn = sqlite3.connect(skypeDB)
    c = conn.cursor()
    c.execute('SELECT datetime(timestamp,"unixepoch"), dialog_partner, author, body_xml FROM Messages;')
    print('\n[*] -- Found Messages --')

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
    parser = optparse.OptionParser('usage %prog -p <skype profile path>')
    parser.add_option('-p', dest='pathName', type='string', help='specify skype profile path')

    (options, args) = parser.parse_args()
    pathName = options.pathName
    if not pathName:
        print(parser.usage)
        exit(0)
    elif not os.path.isdir(pathName):
        print('[!] Path Does Not Exist: %s' % (pathName))
        exit(0)
    else:
        skypeDB = os.path.join(pathName, 'main.db')
        if os.path.isfile(skypeDB):
            printProfile(skypeDB)
            printContacts(skypeDB)
            printCallLog(skypeDB)
            printMessages(skypeDB)
        else:
            print('[!] Skype Database does not exist: %s' % (skypeDB))


if __name__ == '__main__':
    main()
