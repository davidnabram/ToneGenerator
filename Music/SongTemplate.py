# -*- coding: utf-8 -*-
"""
Created on Thu May 04 19:38:47 2017

@author: David
"""

class Scale():
    """Scale object"""

class Song():
    """Song object: Collection of track(s)
    
    Should have key and time signature, though this could be at tracks or bars level""" 
    
class Track():
    """Track object: Collection of bars
    
    Should have bars as inputs. 
    Could have key and time signature"""

class Bar():
    """Bar object: A collection of Notes and/or Chords.
    
    Should have chords and/or notes as inputs
    Could have key and time signature
    """

class Beat():
    """Beat object"""

class Chord():
    """Chord object.
    
    Should have inputs of [frequencies], volume, length, bitrate**
    Should have a chr rep of the note that can be added to form bars and tracks
    Could have information on timbre, tone, instrument, vibrato, etc?
    """
    
class Note():
    """Note object. 
    
    Should have inputs of frequency, volume, length, bitrate**
    Should have a chr rep of the note that can be added to form bars and tracks
    Could have information on timbre, tone, instrument, vibrato, etc?
    """
    
def play_audio(string_of_amplitude_chr):
    """Plays a chr representaion of audio using pyaudio stream"""

def frequency_generator(args):
    """Decides what frequency or frequencies to use for a chord or tone.
    
    Can determine probability of frequency based on chord of measure, or previous chord.
    Also could be based on what bar in the song or sequence of bars (mod) it is in
    """                                                                    