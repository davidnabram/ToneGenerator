import math
import pyaudio
import numpy as np
# from graph import letterFreqPlot

def tone(FrequencyList, length, BITRATE):
    NumberOfFrames = int(BITRATE * length)
    length=length / len(FrequencyList)

    
    WAVEDATA = ''
    valueList = np.zeros(NumberOfFrames)

    # sine wave dampening
    ExtraFrames = []
    for Frequency in FrequencyList:
        ExtraFrames.append(NumberOfFrames % (2 * (BITRATE/Frequency)))
#    print(ExtraFrames)
    

    # note sound
    for i,frame in enumerate(range(NumberOfFrames)):
        localSum = 0
        for Frequency in FrequencyList:
            if frame < NumberOfFrames - int(ExtraFrames[FrequencyList.index(Frequency)]):
                localSum += int(128 + math.sin((math.pi * frame) / (BITRATE / Frequency)) * 127)
            else:
                localSum += int(128)
        valueList[i] = int(localSum / len(FrequencyList))
        
        
    #letterFreqPlot(valueList[-700:])

    #stream.write(WAVEDATA)
    #return valueList
    
    return valueList

def oldtone(FrequencyList, length, stream, BITRATE):

    NumberOfFrames = int(BITRATE * length) # Total number of frames = bitrate * length
    WAVEDATA = ''
    valueList = []

    # sine wave dampening
    ExtraFrames = []
    for Frequency in FrequencyList:
        # append remainder of NumberOfFrames / (2 * Bitrate / frequency)
        ExtraFrames.append(NumberOfFrames % (2 * (BITRATE/Frequency)))
#    print(ExtraFrames)

    # note sound
    #Loop through frames up to total NumberOfFrames-minimum extra frames value from frequency list
    for frame in range(NumberOfFrames - int(min(ExtraFrames))):
        localSum = 0
        # Loop through frequencies in FrequencyList
        # Will create sin waves at each frequency and add the values together
        # Can get constructive or deconstructive interference
        for Frequency in FrequencyList:
            # If frame < NumberOfFrames - ExtraFrames of the specified frequency
            if frame < NumberOfFrames - int(ExtraFrames[FrequencyList.index(Frequency)]):
                #localSum = int(128 + 127*sin(frame*pi*frequency/bitrate). )
                #integers between 1 and 255 will be created
                localSum += int(128 + math.sin((math.pi * frame) / (BITRATE / Frequency)) * 127)
            else:
                localSum += int(128)
        valueList.append(localSum)
        WAVEDATA = WAVEDATA+chr(localSum / len(FrequencyList))    
        
    #letterFreqPlot(valueList[-700:])

    stream.write(WAVEDATA)
    return valueList
