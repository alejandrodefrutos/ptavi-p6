#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import os


class EchoHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        Error = False
        while Error is False:
            line = str(self.rfile.read())
            metodo = line.split(' ')[0]
            nick = ((line.split(' ')[1]).split('@')[0]).split(':')[1]
            IP = ((line.split(':')[1]).split('@')[1]).split(' ')[0]

            if metodo == 'INVITE':
                self.wfile.write("SIP/2.0 100 Trying\r\n")
                self.wfile.write("SIP/2.0 180 Ring\r\n")
                self.wfile.write("SIP/2.0 200 OK\r\n")
            elif metodo == 'ACK':
                aEjecutar = ('./mp32rtp -i ' + IP + ' -p 23032 < ' + fichero_audio)
                print "Vamos a ejecutar", aEjecutar
                os.system(aEjecutar)
            elif metodo == 'BYE':
                self.wfile.write("SIP/2.0 200 OK\r\n")
            else:
                self.wfile.write("SIP/2.0 400 Bad Request\r\n")
                self.wfile.write("SIP/2.0 405 Method Not Allowed\r\n")
            Error = True
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        server = sys.argv[1]
        puerto = int(sys.argv[2])
        fichero_audio = sys.argv[3]
    except IndexError:
        print 'Usage: python servidor.py IP port audio_file'
        sys.exit()
    serv = SocketServer.UDPServer(("", puerto), EchoHandler)
    print "Listening..."
    serv.serve_forever()
