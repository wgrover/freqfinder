import os
from datetime import datetime
import audioread
import wave
import numpy as np
import struct
import sys

files = os.listdir()

for filename in files:
    if filename.endswith(".mp3"):
        window_size = 1000
        f = audioread.audio_open(filename)
        samplerate = f.samplerate
        of = wave.open(filename + '.wav', 'w')
        of.setnchannels(f.channels)
        of.setframerate(f.samplerate)
        of.setsampwidth(2)
        for buf in f:
            of.writeframes(buf)

        f.close()  # trying to fix memory leak
        of.close() # trying to fix memory leak

        wav_file = wave.open(filename + '.wav', 'rb')

        nframes = wav_file.getnframes()
        sounds = wav_file.readframes(nframes)
        wav_file.close()
        sounds = struct.unpack('{n}h'.format(n=nframes*2), sounds)
        sounds = np.array(sounds)
        times = np.linspace(0, len(sounds)/float(f.samplerate), len(sounds))

        def window_rms(a, window_size):
            a2 = np.power(a,2)
            window = np.ones(window_size)/float(window_size)
            return np.sqrt(np.convolve(a2, window, 'valid'))

        powers = window_rms(sounds, window_size)

        max_power = max(powers)

        hanning_window = np.hanning(len(sounds))
        windowed_hanning = hanning_window * sounds

        # original_db = 20*np.log10(np.fft.fft(self.sounds))
        hanning_db = 20*np.log10(np.fft.fft(windowed_hanning))
        pad_size = int(0.50*len(windowed_hanning))
        padding_in_time = pad_size/float(samplerate)
        windowed_hanning = np.pad(windowed_hanning, (pad_size, pad_size), 'constant')
        time_input = np.linspace(times[0] - padding_in_time, times[-1] + padding_in_time, len(windowed_hanning))

        w = np.fft.fft(windowed_hanning)
        # w = np.fft.fft(sounds[enter:exit])
        frequency_spectrum = np.fft.fftfreq(len(w))
        # Find the peak in the coefficients
        idx = np.argmax(np.abs(w))
        ping_frequency = frequency_spectrum[idx]
        ping_frequency = abs(ping_frequency * samplerate)  # convert to Hz

        print(filename, ping_frequency)