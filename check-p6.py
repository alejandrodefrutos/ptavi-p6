#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script de comprobación de entrega de práctica

Para ejecutarlo, desde la shell: 
 $ python check-p6.py

"""

import os
import random
import sys
import subprocess
        
files = ['cliente.py',
         'servidor.py',
         'captura.libpcap',
         '.git']

aleatorio = str(int(random.random() * 1000000))

error = 0

print 

os.system('git clone ~/ptavi/p6 /tmp/' + aleatorio + ' > /dev/null 2>&1')
try:
    student_file_list = os.listdir('/tmp/' + aleatorio)
except OSError:
    error = 1
    print "Error: No se ha creado el repositorio git correctamente."
    print 
    sys.exit()

if len(student_file_list) != len(files):
    error = 1
    print "Error: solamente hay que subir al repositorio los ficheros cliente.py, servidor.py y captura.libpcap."
    print 
    sys.exit()

for filename in files:
    if filename not in student_file_list:
        error = 1
        print "Error: " + filename + " no encontrado. Tienes que subirlo al repositorio."
        print 
        sys.exit()
    if filename == "captura.libpcap":
        output = subprocess.Popen(["tshark", "-r", "/tmp/" + aleatorio + "/captura.libpcap"], stdout=subprocess.PIPE)
        output2 = subprocess.Popen(["wc"], stdin=output.stdout, stdout=subprocess.PIPE)
        lines = output2.communicate()[0].split()[0]
        if int(lines) < 1:
            print "Error: La captura realizada está vacía."
            error = 1
        elif int(lines) > 20:
            print "Aviso: La captura realizada contiene más de 20 paquetes, por lo que probablemente no esté filtrada convenientemente."

if not error:
    print "Parece que la entrega se ha realizado bien."
    print
    print "La salida de pep8 es: (si todo va bien, no ha de mostrar nada)"
    print
    os.system('pep8 --repeat --show-source --statistics /tmp/' + aleatorio + '/cliente.py /tmp/' + aleatorio + '/servidor.py')
print
