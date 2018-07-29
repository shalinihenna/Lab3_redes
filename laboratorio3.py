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
from scipy.fftpack import fft, ifft
from scipy.signal import firwin, lfilter
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
    plt.savefig("images/"+title + ".png")
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

    #Se interpola para tener la misma cantidad de datos
    newData = interp(timesCarrier,timesAudio,dataAudio)

    #Señal modulada
    AM = dataCarrier*newData

    #Gráficos
    fig = plt.figure(1)
    plt.subplot(311)
    plt.title("Señal Audio")
    graph1 = plt.plot(timesCarrier[0:1000],newData[0:1000])
    plt.subplot(312)
    plt.title("Señal Portadora")
    graph2 = plt.plot(timesCarrier[0:1000],dataCarrier[0:1000])
    plt.subplot(313)
    plt.title("Señal Modulada AM al " +str(percentage)+"%")
    graph3 = plt.plot(timesCarrier[0:1000],AM[0:1000])

   # anim = animation.FuncAnimation(fig, animate,frames=100, interval=5, blit=True)
    plt.savefig("images/modulacion"+str(percentage)+".png")
    plt.show()
    return AM,timesCarrier


def demoduladorAM(percentage,timesModulated,dataModulated):
    timesCarrier = linspace(0,totalTime,250000*totalTime)
    dataCarrier = (percentage/100)*cos(2*pi*62500*timesCarrier)
    demoduleAM = dataModulated*dataCarrier
    return demoduleAM


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
  


def saveWav(title, rate, data):
        write(title + ".wav", rate, data.astype('int16'))

def tFourier(data,  rate):
        n = len(data)
        Ts = n / rate
        fftData = fft(data) / n
        fftFreqs = np.fft.fftfreq(n, 1/rate)
        #print(fftFreqs)
        #fftFreqs = np.fft.fftshift(fftFreqs)
        #print(fftFreqs)
        return (fftData, fftFreqs)

def lowFilter(data,rate):
    nyq = rate / 2
    cutoff = 4000
    numtaps = cutoff + 1
    coeff = firwin(numtaps,(cutoff/nyq)) #,window= 'blackmanharris'
    filtered = lfilter(coeff,1.0,data)
    return filtered

"""
def init():
    line.set_data([],[])
    return line

def animate(times,data):
    return times,data
"""
###################################################
################ Bloque Principal #################
###################################################
rate, data, times = openWav("handel.wav") #rate = frecuencia_muestreo, data = datos(eje y), times = tiempos(eje x)
totalTime = len(data)/rate
fftData, fftFreqs = tFourier(data,rate)
makeGraphic("Grafico frecuencia senal original", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))

#Modulación AM.
print("Graficos Modulacion al 15%")
AM15, timesCarrier15 = modulacionAM(15,data,times,rate,totalTime)
fftData, fftFreqs = tFourier(AM15,rate)
makeGraphic("Grafico frecuencia AM 15", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))

print("Graficos Modulacion al 100%")
AM100, timesCarrier100 = modulacionAM(100,data,times,rate,totalTime)
fftData, fftFreqs = tFourier(AM100,rate)
makeGraphic("Grafico frecuencia AM 100", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))

print("Graficos Modulacion al 125%")
AM125, timesCarrier125 = modulacionAM(125,data,times,rate,totalTime)
fftData, fftFreqs = tFourier(AM125,rate)
makeGraphic("Grafico frecuencia AM 125", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))

#Demodulación AM.
print("Demodulacion 15%")
dem15 = demoduladorAM(15,timesCarrier15,AM15)
filtered = lowFilter(dem15,rate)
fftData, fftFreqs = tFourier(filtered,rate)
makeGraphic("Grafico frecuencia demodulador 15", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))


print("Demodulacion 100%")
dem100 = demoduladorAM(100,timesCarrier15,AM100)
filtered = lowFilter(dem100,rate)
fftData, fftFreqs = tFourier(filtered,rate)
makeGraphic("Grafico frecuencia demodulador 100", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))


print("Demodulacion 125%")
dem125 = demoduladorAM(125,timesCarrier15,AM125)
filtered = lowFilter(dem125,rate)
fftData, fftFreqs = tFourier(filtered,rate)
makeGraphic("Grafico frecuencia demodulador 125", "Frecuencia [Hz]", fftFreqs, "Amplitud [dB]", abs(fftData))

#saveWav("prueba",rate,dem15)
#Modulación FM.

print("Ejecución Finalizada")
#APUNTES:
#Aliasing al tener 1000 al ocupar un poco más del doble
#Mientras más lejos esté, más "bonito" se ve el graáfico
#Analizar con la transformada de fourier
#Animación gráficos
