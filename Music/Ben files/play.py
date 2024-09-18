
import pyaudio
from random import choice
from tone import tone, oldtone
from noteValues import noteValues

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio
half=pow(2,1/float(12))
intervals={}
intervals['major']=[4,3,5]
intervals['minor']=[3,4,5]

def get_chord(rootfreq,kind='major',numNotes=3):
    chord=[rootfreq]
    for i in xrange(numNotes-1):
        chord.append(chord[-1]*pow(half,intervals[kind][i]))
    return chord
        
        
    
    
# On my computer, 40000 removes most static
bitrate = 44100

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = bitrate,
                output = True)

### PLAY NOTES HERE:
c_chord = [noteValues['c', 6], noteValues['e', 6], noteValues['g', 6]]
a_chord = [noteValues['a', 5], noteValues['c', 6], noteValues['e', 6]]
f_chord = [noteValues['f', 5], noteValues['a', 5], noteValues['c', 6]]
g_chord = [noteValues['g', 5], noteValues['b', 5], noteValues['d', 6]]
length=0.5

a=oldtone(c_chord, 2, stream, bitrate)
oldtone(get_chord(noteValues['c',6]),2,stream,bitrate)
b=oldtone([noteValues['c', 6]], 2, stream, bitrate)
c=max(a)
tone(f_chord, 2, stream, bitrate)
tone(g_chord, 2, stream, bitrate)



###

stream.stop_stream()
stream.close()
p.terminate()