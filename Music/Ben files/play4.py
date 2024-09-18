
import pyaudio
import numpy as np
from random import choice
from tone import tone
from noteValues import noteValues

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio
half=pow(2,1/float(12))
chord_intervals={'M':[4,3,5],
           'm':[3,4,5],
           'M7':[4,3,4],
           '7':[4,3,3],
           'm7':[3,4,3],
           'dim':[3,3,6]
           }
key_intervals={'M':[(2,'m'),(2,'m'),(1,'M'),(2,'M'),(2,'m'),(2,'dim'),(1,'M')],
               'm':[(2,'dim'),(2,'M'),(1,'m'),(2,'m'),(2,'M'),(2,'M'),(1,'m')]
               }

def get_chord(rootfreq,kind='M',numNotes=4):
    chord=[rootfreq]
    for i in range(numNotes-1):
        chord.append(chord[-1]*pow(half,chord_intervals[kind][i]))
    return chord
def get_scale(rootfreq,kind='M',octaves=1):
    key=[(rootfreq,kind)]
    for i in range(octaves):
        for (j,k) in key_intervals[kind]:
            key.append((key[-1][0]*pow(half,j),k))            
    return key
        
class Song(object):
    def __init__(self,key,bars,tempo=120,num=4,denom=4,bitrate=44100,rhythm=None):
        self.key=key
        self.tempo=tempo
        self.bars=bars
        self.num=num
        self.denom=denom
        self.bitrate=bitrate
        self.rhythm=rhythm
        self.length=240 / (float(tempo)*denom)
        self.chord_length = num * self.length
        self.trackValues=[]
        self.songValues=np.array([])
        self.WAVEDATA = ''
    def play_song(self):
        p = PyAudio()
        stream = p.open(format = p.get_format_from_width(1), 
                        channels = 1, 
                        rate = self.bitrate,
                        output = True)
        self.combine_tracks()
        self.convert_to_wavedata()
        
        
        # stream.write(self.WAVEDATA)
        stream.write(bytes(self.WAVEDATA))
        stream.stop_stream()
        stream.close()
        p.terminate()
    def combine_tracks(self):
#        track_lengths=[len(a) for a in self.trackValues]
#        track_length_min=min(track_lengths)
#        if track_lengths[0] > track_lengths[1]:
        #self.songValues=int((trackValues[0]+trackValues[1])/2)
        #self.songValues=np.array([])
        self.songValues = 1.1*self.trackValues[0] + .9*self.trackValues[1]
        self.songValues = self.songValues / len(self.trackValues)
            
        
    def convert_to_wavedata(self):
        songValues = [int(i) for i in self.songValues]
        # self.WAVEDATA = ''.join(chr(i) for i in songValues)
        self.WAVEDATA = bytearray(songValues)
            
        
    def get_track(self,chords=False):
        valueList=np.array([])
        
        if chords:
            for i in range(self.bars):                
                frequency,kind=choice(self.key)                
                frequencies=get_chord(frequency,kind=kind,numNotes=3)
                print (('frequencies = %s') % frequencies)
                valueList = np.append(valueList,tone(frequencies,self.chord_length,self.bitrate))                
        else:
            for i in range(self.bars):
                for j in range(self.num):
                    frequency,kind=choice(self.key)                                    
                    print (('frequency = %s') % frequency)
                    valueList = np.append(valueList,tone([frequency],self.length,self.bitrate))                                  
        self.trackValues.append(valueList)

    
root=noteValues['c',5]
mySong=Song(get_scale(root,kind='M',octaves=1),8,tempo=120,num=4,denom=4)
mySong.get_track()
mySong.get_track(chords=True)
# import ipdb; ipdb.set_trace()
mySong.play_song()





###

