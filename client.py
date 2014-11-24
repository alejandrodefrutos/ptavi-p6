#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    metodo = sys.argv[1]
    datos = sys.argv[2]
except IndexError:
    print 'Usage: python cliente.py method receiver@IP:SIPport'
    sys.exit()

receptor = datos.split('@')[0]
SERVER = (datos.split('@')[1]).split(':')[0]
PORT = int((datos.split('@')[1]).split(':')[1])

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

my_socket.send(metodo + ' sip:' + receptor + '@' + SERVER + ' SIP/2.0' + '\r\n')
try:
    data = my_socket.recv(1024)
except socket.error:
    print 'Error: no server listening at ' + SERVER + ' port ' + str(PORT)
    sys.exit()
respuesta = data.split("SIP/2.0 ")
if respuesta[1] == '100 Trying\r\n':
    metodo = 'ACK'
    my_socket.send(metodo + ' sip:' + receptor + '@' + SERVER + ' SIP/2.0' + '\r\n')
elif respuesta[1] == '400 Bad Request\r\n':
    print 'Error: ' + respuesta[1] + respuesta[2]
# Terminamos
print "Terminando socket..."
my_socket.close()
print "Fin."
