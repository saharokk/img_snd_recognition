#-*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.io import wavfile
import pyaudio, wave
import keyboard
import time

matplotlib.use("TkAgg")


chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
filename = "output.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)



frames = np.empty((1, 2), dtype=np.int16)  # Initialize array to store frames
while not keyboard.is_pressed('escape'):
    
    data = stream.read(chunk)
    data = np.fromstring(data, dtype=np.int16)
    data = np.reshape(data, (chunk, 2)) 
    data = data / np.power(2, 15)
    frames = np.concatenate([frames, data])
    time_axis = 1000 * np.arange(0, len(frames), 1) / float(fs)
    len_signal = len(frames)
    len_half = np.ceil((len_signal + 1) / 2.0).astype(np.int)
    freq_signal = np.fft.fft(frames)

    # Нормалізація
    freq_signal = abs(freq_signal[0:len_half]) / len_signal

    # Піднесення до квадрату
    freq_signal **= 2

    # Довжина перетвореного частотного сигналу
    len_fts = len(freq_signal)

     
    if len_signal % 2:
        freq_signal[1:len_fts] *= 2
    else:
        freq_signal[1:len_fts-1] *= 2
    # Потужність сигналу в Дб
    signal_power = 10 * np.log10(freq_signal)

    # Build the X axis
    x_axis = np.arange(0, len_half, 1) * (fs / len_signal) / 1000.0 

    f0 = plt.figure(0)
    plt.plot(time_axis, frames, color='black')
    plt.xlabel('Time (milliseconds)')
    plt.ylabel('Amplitude')
    plt.title('Input audio signal')

    # Побудова графіку зміни потужності сигналу відповідно до частотного спектру
    f1 = plt.figure(1)
    plt.plot(x_axis, signal_power, color='black')
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Signal power (dB)')
    
    f0.canvas.draw()
    f1.canvas.draw()
    
    plt.pause(1e-17)
    #time.sleep(0.1)



# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')


# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()





