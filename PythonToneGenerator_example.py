#! /usr/bin/python
 
import numpy
import pyaudio
import math
import random
 
 
class ToneGenerator(object):
 
    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
 
    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out
 
    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)
 
    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False
 
    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)
    def play_chord(self, frequencies, duration, amplitude):
        self.omegas = []
        for i in frequencies:
            self.omegas.append(float(i) * (math.pi * 2) / self.samplerate)
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)
 
 
###############################################################################
#                                 Usage Example                               #
###############################################################################
 
generator = ToneGenerator()
 
frequency_start = 440        # Frequency to start the sweep from
frequency_end = 880       # Frequency to end the sweep at
num_frequencies = 13       # Number of frequencies in the sweep
amplitude = 0.50            # Amplitude of the waveform
step_duration = 0.43        # Time (seconds) to play at each step

Chromatic = numpy.logspace(math.log(frequency_start, 10),
                                math.log(frequency_end, 10),
                                num_frequencies) 
MajorInd = [0, 2, 4, 5, 7, 9, 11, 12]
MinorInd = [0, 2, 3, 5, 7, 8, 10, 12]
Major = [Chromatic[i] for i in MajorInd]
Minor = [Chromatic[i] for i in MinorInd]
#for frequency in Chromatic:
for i in xrange(100):
    ind = random.randint(0, 7) 
    ind2 = random.randint(0, 7)  
    frequency = Minor[ind]
    frequency2 = Minor[ind2]
    
    print("Playing tone at {0:0.2f} Hz".format(frequency))
    generator.play(frequency, step_duration, amplitude)
    generator.play(frequency2, step_duration, amplitude)
    while generator.is_playing():
        pass                # Do something useful in here (e.g. recording)