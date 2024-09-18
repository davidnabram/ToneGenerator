#! /usr/bin/python
 
import numpy
import pyaudio
import math

 
class ToneGenerator(object):
    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False
        self.data=[]
 
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
 
    # out_data is a byte array whose length should be frame_count * channels * 
    # bytes-per-channel if output=True or None if output=False
    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            # Creates the out_data by running sinewave(), storing as float
            data = self.sinewave().astype(numpy.float32)
            self.data.append(data)
            # Returns out_data as string; flag = continue
            return (data.tostring(), pyaudio.paContinue)
        else:
            # Returns out_data as None; flag = complete
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
        # omega = 2*pi * frequency / samplerate
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude # Store amplitude
        self.buffer_offset = 0 # Initialize buffer_offset
        self.streamOpen = True #Open stream
        # Set x_max to samplerate * duration rounded down to nearest integer
        self.x_max = math.ceil(self.samplerate * duration) - 1
        # Initialize stream                              
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)
 
 
###############################################################################
#                                 Usage Example                               #
###############################################################################
 

def __main__():
    generator = ToneGenerator() # Initialize ToneGenerator object
 
    frequency_start = 440        # Frequency to start the sweep from
    frequency_end = 880       # Frequency to end the sweep at
    num_frequencies = 13       # Number of frequencies in the sweep
    amplitude = 1        # Amplitude of the waveform
    step_duration = 0.25        # Time (seconds) to play at each step

     # Creates and loops through list of equally spaced frequencies
    for frequency in numpy.logspace(math.log(frequency_start, 10),
                                    math.log(frequency_end, 10),
                                    num_frequencies):

        print("Playing tone at {0:0.2f} Hz".format(frequency))
        generator.play(frequency, step_duration, amplitude)
        while generator.is_playing():
            pass                # Do something useful in here (e.g. recording)

if __name__ == "__main__":
    __main__()