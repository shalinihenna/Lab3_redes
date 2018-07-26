#Parte 1:
### 1. Utilice la señal “handel.wav” publicada en ​ www.udesantiagovirtual.cl
### 2. Aplique una modulación AM y una modulación FM al 15%, 100% y 125% (porcentaje
###   de modulación). Un gráfico por cada modulación ayudará a exponer los resultados
###   obtenidos.
### 3. Grafique el espectro de frecuencias de la señal original y modulada. Determine el
###   ancho de banda usada por la señal modulada.
### 4. Implemente un demodulador para AM o FM y compare los resultados.
### 5. Responda:
### ● ¿Cuáles son los principales usos para la modulación AM? ¿Por qué?
### ● ¿Cuáles son los principales usos para la modulación FM? ¿Por qué?
### ● ¿Cuáles son los problemas de una sobremodulación? Apóyese gráficamente
###    para argumentar.
### ● ¿Por qué no modular siempre en un 100%?


###################################################
# Laboratorio n°3 Redes de Computadores			  #	
# INTEGRANTES:									  #
#   - Javier Arredondo							  #	
#	- Shalini Ramchandani						  #	
###################################################

###################################################
################## Importaciones ##################
###################################################
import numpy as np
from numpy import linspace,cos
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from math import pi

###################################################
############# Definición de funciones #############
###################################################
def openWav(name):
        rate, info = read(name)  #rate = frecuencia_muestreo
        dimension = info[0].size
        if(dimension == 1):
                data = info
        else:
                data = info[:,dimension-1]
        n = len(data)
        Ts = n / rate  #Ts = Tiempo total
        times = np.linspace(0, Ts, n)
        return (rate, data, times)

def makeGraphic(title, xlabel, xdata, ylabel, ydata):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(xdata, ydata)
    plt.savefig(title + ".png")
    plt.show()
    plt.close('all')

def timeGraphic(data, rate,title):
	duration = len(data)/rate # Tiempo que dura todo el audio
	t = linspace(0, duration, len(data)) # Intervalos de tiempo de 0 a t, generando la misma cantidad de datos que hay en data o vector tiempo
	makeGraphic(title, "Tiempo [s]", t, "Amplitud [dB]", data)


###################################################
################ Bloque Principal #################
###################################################
#rate,data,times = openWav("handel.wav")	 #rate = frecuencia, data = tiempo
#timeGraphic(data,rate,"Señal Original")

tiemposMensaje = linspace(0,1,5000)
datosMensaje = cos(2*pi*2*tiemposMensaje)  #-> frecuencia = 2 vueltas en 1 seg
makeGraphic("Mensaje", "ejex",tiemposMensaje,"ejey",datosMensaje)

tiemposPortador = linspace(0,1,5000) 
datosPortador = 2*cos(2*pi*100*tiemposPortador)
makeGraphic("Señal portador", "ejex",tiemposPortador,"ejey",datosPortador)

modulado = datosMensaje*datosPortador
makeGraphic("Modulado", "ejex",tiemposPortador,"ejey",modulado)


#Aliasing al tener 1000 al ocupar un poco más del doble
#Mientras más lejos esté, más "bonito" se ve el graáfico