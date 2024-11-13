import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal import iirnotch, butter, lfilter


#def filtre_passe_bande(signal, freq_ech, freq_basse, freq_haute, Q, gain=1.0):

#Test à mofidier...
def filtreNumTemp1k(data):
    a0 = 0.2183
    a1 = -0.2183
    b1 = 1.7505
    b2 = -0.7661
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
     
    for i in range(2, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + b2* filtered_data[i-2]
    return filtered_data

def filtreNumTemp3k(data):
    a0 = 0.1941
    a1 = -0.1941
    b1 = 1.5568
    b2 = -0.6813
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
     
    for i in range(2, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + b2* filtered_data[i-2]
    return filtered_data

def filtreNumTemp5k(data):
    a0 = 0.1589
    a1 = -0.1589
    b1 = 1.2747
    b2 = -0.5578
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
     
    for i in range(2, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + b2* filtered_data[i-2]
    return filtered_data


def filtreNumTemp7k(data):
    a0 = 0.1249
    a1 = -0.1249
    b1 = 1.0023
    b2 = -0.4386
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
     
    for i in range(2, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + b2* filtered_data[i-2]
    return filtered_data



def filtreNumTemp9k(data):
    a0 = 0.0972
    a1 = -0.0972
    b1 = 0.7800
    b2 = -0.3413
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
     
    for i in range(2, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + b2* filtered_data[i-2]
    return filtered_data



### 3 exemples de donnees d'entress sont proposees
type = 2
creationWavFiltre = False  #True si l'on veut créer un wav à la fin
if type == 0 : 
    ###### Signal sinusoïdal
    freq_ech = 96000  # Fréquence d'échantillonnage en Hz
    f_sin = 7e3  # Fréquence du signal sinusoïdal en Hz
    duree = 1      # Durée du signal en secondes
    # Créer un tableau de temps
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    # Générer le signal sinusoïdal
    data = np.sin(2 * np.pi * f_sin * t)
    
    ###### fin signal sinusoïdal

elif type == 1 : 
    ####### Fichier wav lu resultat dans u ntableau (attention au mon ou au stéréo
    freq_ech, data = wavfile.read('LW_20M_amis.wav')
    # Créer un tableau de temps
    t = np.linspace(0, len(data) / freq_ech, len(data), endpoint=False)
    creationWavFiltre = True
    ####### Fin wav
else : 
    ##### Une impulsion
    freq_ech = 44100
    duree = 4
    data = np.zeros(freq_ech*duree)
    data[0] = 1
    t = np.linspace(0, duree, int(freq_ech * duree), endpoint=False)
    #####Fin impulsion



# Vérifier si le fichier est stéréo ou mono
if len(data.shape) > 1:
    # Si le fichier est stéréo, prendre un seul canal (par exemple, le canal gauche)
    data = data[:, 0]

# Appliquer la FFT
fft_result = np.fft.fft(data)

# Creation du vecteur frequence 1re moitier freq positive, 2e moitié freq négative.  
frequences = np.fft.fftfreq(len(fft_result), d=1/freq_ech)  
print(frequences)
print(len(frequences))

# Optionnel : Afficher la magnitude du spectre



# Application du filtre passe-bas
signal_filtre_1k = filtreNumTemp1k(data)
signal_filtre_3k = filtreNumTemp3k(data)
signal_filtre_5k = filtreNumTemp5k(data)
signal_filtre_7k = filtreNumTemp7k(data)
signal_filtre_9k = filtreNumTemp9k(data)
#signal_filtre = filtre_passe_bas1(data, freq_ech, freq_coupure1, gain_1)
# Calculer la FFT du signal filtré
fft_result_1k = np.fft.fft(signal_filtre_1k)
fft_result_3k = np.fft.fft(signal_filtre_3k)
fft_result_5k = np.fft.fft(signal_filtre_5k)
fft_result_7k = np.fft.fft(signal_filtre_7k)
fft_result_9k = np.fft.fft(signal_filtre_9k)



# Écrire le fichier WAV
if creationWavFiltre == True : 
    # Normalisation du signal filtré avec gain
    signal_filtre_normalise = np.clip(signal_filtre, -32768, 32767)  # Limiter les valeurs
    signal_filtre_normalise  = signal_filtre_normalise .astype(np.int16)  # Convertir en entiers 16 bits


    wavfile.write('wav_filtre.wav', freq_ech, signal_filtre_normalise)


# Créer une figure avec deux sous-graphes
plt.figure(figsize=(12, 10))

# Sous-graphe 1 : Signal temporel
plt.subplot(2, 1, 1)
plt.plot(t, data, label='Signal Origine')
plt.plot(t, signal_filtre_1k, label='Filtre 1k', linestyle='--')
plt.plot(t, signal_filtre_3k, label='Filtre 3k', linestyle='--')
plt.plot(t, signal_filtre_5k, label='Filtre 5k', linestyle='--')
plt.plot(t, signal_filtre_7k, label='Filtre 7k', linestyle='--')
plt.plot(t, signal_filtre_9k, label='Filtre 9k', linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.title('Signal temporel')
plt.legend()



# Sous-graphe 2 : Signal FFT

plt.subplot(2, 1, 2)
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result)[:len(fft_result)//2], label='Original')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_1k)[:len(fft_result_1k)//2], label='Filtre 1k')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_3k)[:len(fft_result_3k)//2], label='Filtre 3k')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_5k)[:len(fft_result_5k)//2], label='Filtre 5k')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_7k)[:len(fft_result_7k)//2], label='Filtre 7k')
plt.plot(frequences[:len(frequences)//2], np.abs(fft_result_9k)[:len(fft_result_9k)//2], label='Filtre 9k')
plt.xscale('log')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Magnitude')
plt.title('Spectre de Fourier')
plt.legend()

# Afficher les sous-graphes
plt.tight_layout()
plt.show()
