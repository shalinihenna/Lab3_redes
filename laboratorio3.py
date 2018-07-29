#HECHO:
### 1. Utilice la señal “handel.wav” publicada en ​ www.udesantiagovirtual.cl

#POR HACER:
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
from numpy import linspace,cos,interp
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from matplotlib import animation
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

def modulacionAM(percentage,dataAudio,timesAudio,rate,totalTime):
    #Señal Portadora
   
    timesCarrier = linspace(0,totalTime,250000*totalTime)
    dataCarrier = (percentage/100)*cos(2*pi*62500*timesCarrier)

    newData = interp(timesCarrier,timesAudio,dataAudio)

    AM = dataCarrier*newData

    plt.subplot(311)
    graph1 = plt.plot(timesCarrier[0:1000],newData[0:1000])

    plt.subplot(312)
    graph2 = plt.plot(timesCarrier[0:1000],dataCarrier[0:1000])

    plt.subplot(313)
    graph3 = plt.plot(timesCarrier[0:1000],AM[0:1000])

    #anim = animation.FuncAnimation(fig, animate, init_func=init,frames=100, interval=20, blit=True)
    plt.show()
    return

def modFM(percentage, dataAudio, timesAudio, rate, totalTime):
        freqP = 5/2 * rate # Se necesita de una frecuencia portadora que sea la mitad de la freq obtenida y minimo 4 veces mayor a la freq de muestreo.
        # ^ Eso da 20480
        
        # Señal portadora
        A = 1 # Amplitud definida para la señal portadora
        timesCarrier = linspace(0, totalTime, 250000*totalTime)
        dataCarrier = A * cos(pi * timesCarrier * 6500) # Podriamos cambiar el 6500 por freqP
        # Reestructuración de datos originales
        dataAudio =  interp(timesCarrier, timesAudio, dataAudio)
        timesAudio = timesCarrier
        # Señal modulada en su frecuencia
        signalIntegrate =  integrate.cumtrapz(dataAudio, timesAudio, initial=0) # Integral acumulada
        dataModulated = A * cos(pi * timesCarrier * 6500 + (percentage/100) * signalIntegrate)


        plt.subplot(311)
        plt.title("Señal del Audio")
        plt.plot(timesAudio[:5000], dataAudio[:5000])
        
        plt.subplot(312)
        plt.title("Señal Portadora")
        plt.plot(timesCarrier[:5000], dataCarrier[:5000], linewidth=0.3, color = "red")
        
        plt.subplot(313)
        plt.title("Modulación FM "+str(percentage)+" %")
        plt.plot(timesAudio[:5000], dataModulated[:5000], linewidth=0.3, color = "green", marker = "o", markersize= 0.5)
        plt.show()
        return 



###################################################
################ Bloque Principal #################
###################################################
rate, data, times = openWav("handel.wav") #rate = frecuencia_muestreo, data = datos(eje y), times = tiempos(eje x)
#timeGraphic(data,rate,"Señal Original")
totalTime = len(data)/rate
print(totalTime)
modulacionAM(15,data,times,rate,totalTime)
modulacionAM(100,data,times,rate,totalTime)
modulacionAM(125,data,times,rate,totalTime)


"""
tiemposMensaje = linspace(0,1,2500)
datosMensaje = cos(2*pi*2*tiemposMensaje)  #-> frecuencia = 2 vueltas en 1 seg
makeGraphic("Mensaje", "ejex",tiemposMensaje,"ejey",datosMensaje)

tiemposPortador = linspace(0,1,2500) 
datosPortador = 2*cos(2*pi*1000*tiemposPortador)
makeGraphic("Señal portador", "ejex",tiemposPortador,"ejey",datosPortador)

modulado = datosMensaje*datosPortador
makeGraphic("Modulado", "ejex",tiemposPortador,"ejey",modulado)
"""


#APUNTES:
#Aliasing al tener 1000 al ocupar un poco más del doble
#Mientras más lejos esté, más "bonito" se ve el graáfico
#Analizar con la transformada de fourier
#Animación gráficos
