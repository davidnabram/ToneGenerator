
import pyaudio
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
    for i in xrange(numNotes-1):
        chord.append(chord[-1]*pow(half,chord_intervals[kind][i]))
    return chord
def get_scale(rootfreq,kind='M',octaves=1):
    key=[(rootfreq,kind)]
    for i in xrange(octaves):
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
    def play_song(self):
        p = PyAudio()
        stream = p.open(format = p.get_format_from_width(1), 
                        channels = 1, 
                        rate = self.bitrate,
                        output = True)
        #WAVEDATA=''  
        self.toneList=[]
        self.wdata=[]
        for i in xrange(self.bars):
            for j in xrange(self.num):
                frequency,kind=choice(self.key)
                frequencies=get_chord(frequency,kind)
                #WAVEDATA=tone([frequency],self.length,stream,self.bitrate)
#                WAVEDATA=tone(frequencies,self.length,stream,self.bitrate)
#                a=tone([frequency],self.length,stream,self.bitrate)
#                toneList.extend(self.a)
#                self.toneList=toneList
                #self.wdata.append(WAVEDATA)
                #self.wdata += tone([frequency],self.length,stream,self.bitrate)
                self.wdata.append(tone(frequencies,self.length,stream,self.bitrate))
                
                #stream.write(WAVEDATA)         
        #WAVEDATA = WAVEDATA+chr(localSum / len(FrequencyList))    
#        print len(self.toneList[0])
#        with open("Output.txt", "w") as text_file:
#            text_file.write(','.join(str(i) for i in self.toneList[0]))
        
        stream.write(''.join(self.wdata))
        stream.stop_stream()
        stream.close()
        p.terminate()

    
root=noteValues['c',5]
mySong=Song(get_scale(root,kind='M',octaves=1),16,tempo=120,num=4,denom=4)
mySong.play_song()





###

