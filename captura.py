# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 08:27:16 2018
@author: bcasas
"""
#REGISTRO DE VERSIONES
VER='2018-12-10 bcasas@socib.es' #Incluye lectura del puerto para scp en info.txt
#VER='2018-10-15 bcasas@socib.es' #Paso las funcions a funciones.py
#VER='2018-10-15 bcasas@socib.es'
#%%

#IMPORTA LAS FUNCIONES NECESARIAS
from funciones import captura, captura_AADI, leeCalAADI, instant, anyadeLog, leeInfo
from threading import Thread
import os
import sys
#import os.path
#%%

#LIMPIA LA PANTALLA
os.system('clear')
#%%

#LOCALIZA EL FICHERO 'info.txt' QUE CONTIENE LA INFORMACION DE LA ESTACION Y DE LOS INSTRUMENETOS INSTALADOS
info = os.path.dirname(os.path.abspath(__file__))+'/info.txt'
#%%

#COMPRUEBA LA EXISTENCIA DEL FICHERO 'info.txt'
if os.path.isfile(info):

#SI EXISTE EJECUTA ACCIONES
# ACCION_1: REALIZA LA LECTURA DEL FICHERO INFO
    Station,DirLocal,Portal,Puerto,User,DirDest,MailFrom,MailPass,MailDest,NInstrum,Instrument,InstrumentId,SerialPort,SerialBaud,SerialBS,SerialPar,Lines,FileInput = leeInfo(info)
# ACCION_2: SE LANZAN LOS PROCESOS DE CAPTURA DE DATOS PARA CADA INSTRUMENTO 
    for n in range (NInstrum):
        if InstrumentId[n].find('AADI') > 0 :
            subproceso = Thread(target=captura_AADI, args=(FileInput[n],SerialPort[n],int(SerialBaud[n]),int(SerialBS[n]),SerialPar[n],DirLocal,Station,InstrumentId[n],MailFrom,MailPass,MailDest,))
            subproceso.start()
        else:
            subproceso = Thread(target=captura, args=(FileInput[n],SerialPort[n],int(SerialBaud[n]),int(SerialBS[n]),SerialPar[n],DirLocal,Station,InstrumentId[n],))
            subproceso.start()
else:
# ACCION_3: NO SE ENCUENTRA EL FICHERO 'info.txt', SE GENERA UN MENSAJE DE ERROR
    import commands
    TEXT = 'ERROR: No se encuentra el fichero de informacion de la estacion:'+info
    print TEXT
    TEXT = instant('%Y-%m-%d %H:%M:%S')+' | ERROR_CAPTURA. '+TEXT
    PWD  = commands.getoutput ('pwd')
    DirLocal = PWD[:PWD.find('pi')+3]
    Station  = PWD[PWD.find('pi')+3:]
    Station  = Station[:Station.find('/')]
    anyadeLog(DirLocal, Station,'ERROR',TEXT,MailFrom,MailPass,MailDest)
    print '    -EL SCRIPT SE HA DETENIDO-'
##################################################################################
