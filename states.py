import serialfuncs
from gridsnotes import note

from tkinter import *
from tkinter import ttk

import serial.tools.list_ports
import time
import mido

import numpy
import sounddevice as sd
testarr = numpy.array([255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0])
testarr = testarr.astype(numpy.uint8)

playMode = 0
songTempo = 120
gridSpeed = 4
gridSize = 16
serialActive = 0
portsOld = serial.tools.list_ports.comports()
pianoOctave = 2
    
outport = mido.open_output('MINT 0.5', virtual=True)

def saveFile():
    f = open("hello", "x")

def pianoPush(key, offset, tracks, instrument):
    midimsg = mido.Message('note_on', note=convertNoteMidi(note(key, pianoOctave + offset, instrument.get())))
    outport.send(midimsg)
    serialfuncs.playNote(convertNoteHz(note(key, pianoOctave + offset, instrument.get())), 10)
    for selected in tracks:
        selected.assignNote(note(key, pianoOctave + offset, instrument.get()))
        
def keyRelease(event):
    time.sleep(.1)
    outport.panic()

def keyPush(event, tracks, instrument):
    if (event.char == 'a'):
        pianoPush("A", 0, tracks, instrument)
    if (event.char == 'w'):
        pianoPush("A#", 0, tracks, instrument)
    if (event.char == 's'):
        pianoPush("B", 0, tracks, instrument)
    if (event.char == 'd'):
        pianoPush("C", 0, tracks, instrument)
    if (event.char == 'r'):
        pianoPush("C#", 0, tracks, instrument)
    if (event.char == 'f'):
        pianoPush("D", 0, tracks, instrument)
    if (event.char == 't'):
        pianoPush("D#", 0, tracks, instrument)
    if (event.char == 'g'):
        pianoPush("E", 0, tracks, instrument)
    if (event.char == 'h'):
        pianoPush("F", 0, tracks, instrument)
    if (event.char == 'u'):
        pianoPush("F#", 0, tracks, instrument)
    if (event.char == 'j'):
        pianoPush("G", 0, tracks, instrument)
    if (event.char == 'i'):
        pianoPush("G#", 0, tracks, instrument)
    if (event.char == 'k'):
        pianoPush("A", 1, tracks, instrument)
    if (event.char == 'o'):
        pianoPush("A#", 1, tracks, instrument)
    if (event.char == 'l'):
        pianoPush("B", 1, tracks, instrument)
    if (event.char == ';'):
        pianoPush("C", 1, tracks, instrument)
    if (event.char == '['):
        pianoPush("C#", 1, tracks, instrument)
    if (event.char == """'"""):
        pianoPush("D", 1, tracks, instrument)
    if (event.char == ']'):
        pianoPush("D#", 1, tracks, instrument)

def delPush(event, tracks):
    for selected in tracks:
        selected.assignNote(note("--", "-", "--"))
        
def breakPush(event, tracks):
    for selected in tracks:
        selected.assignNote(note("==", "=", "=="))

def songSettingsApply(tracks, tempo, grids, speed):
    global songTempo
    global gridSize
    global gridSpeed
    songTempo = int(tempo.get())
    if (songTempo > 999):
        songTempo = 999
        tempo.delete(0, END)
        tempo.insert(0, "999")
    if (songTempo < 20):
        songTempo = 20
        tempo.delete(0, END)
        tempo.insert(0, "20")
    gridSize = int(grids.get())
    if (gridSize > 64):
        gridSize = 64
        grids.delete(0, END)
        grids.insert(0, "64")
    gridSpeed = int(speed.get())
    if (gridSpeed > 64):
        gridSpeed = 64
        speed.delete(0, END)
        speed.insert(0, "64")
    for track in tracks:
        track.changeRows(gridSize)

def increaseOctave(frame):
    global pianoOctave
    pianoOctave+=1
    if (pianoOctave > 8):
        pianoOctave = 8
    ttk.Label(frame, text = pianoOctave).grid(row = 1, column = 1)

def decreaseOctave(frame):
    global pianoOctave
    pianoOctave-=1
    if (pianoOctave < 0):
        pianoOctave = 0
    ttk.Label(frame, text = pianoOctave).grid(row = 1, column = 1)
    
def convertNoteHz(note):
    if (note.key[0] == "A"):
        dist = 0
    if (note.key[0] == "B"):
        dist = 2
    if (note.key[0] == "C"):
        dist = 3
    if (note.key[0] == "D"):
        dist = 5
    if (note.key[0] == "E"):
        dist = 7
    if (note.key[0] == "F"):
        dist = 8
    if (note.key[0] == "G"):
        dist = 10
    if (len(note.key) > 1):
        dist += 1
    pitch = 27.5 * pow(pow(2, 1/12), dist + note.octave*12)
    return round(pitch)

def convertNoteMidi(note):
    if (note.key[0] == "A"):
        dist = 0
    if (note.key[0] == "B"):
        dist = 2
    if (note.key[0] == "C"):
        dist = 3
    if (note.key[0] == "D"):
        dist = 5
    if (note.key[0] == "E"):
        dist = 7
    if (note.key[0] == "F"):
        dist = 8
    if (note.key[0] == "G"):
        dist = 10
    if (len(note.key) > 1):
        dist += 1
    midi = dist + note.octave*12 + 21
    return midi
    
def stopPlaying():
    global playMode
    playMode = 0
    #outport.panic()
    outport.reset()

def playFrame(track, root):
    global playMode
    playMode = 1
    lastNote = note("C",4,"00")
    for i in range(track.gridRows):
        if '-' not in track.playRow(i).key and '=' not in track.playRow(i).key:
            msg = mido.Message('note_off', note=convertNoteMidi(lastNote))
            outport.send(msg)
            serialfuncs.playNote(convertNoteHz(track.playRow(i)), 100)
            msg = mido.Message('note_on', note=convertNoteMidi(track.playRow(i)))
            outport.send(msg)
            lastNote = track.playRow(i)
        if "=" in track.playRow(i).key:
            msg = mido.Message('note_off', note=convertNoteMidi(lastNote))
            outport.send(msg)
        root.update()
        time.sleep((60/songTempo)/gridSpeed)
        if (playMode == 0):
            break
    stopPlaying()
        
def playSong(track, root):
    global playMode
    playMode = 1
    lastNote = note("C",4,"00")
    for i in range(len(track.trackGrids)):
        track.selectGrid(i)
        for j in range(track.gridRows):
            if '-' not in track.playRow(j).key and '=' not in track.playRow(j).key:
                serialfuncs.playNote(convertNoteHz(track.playRow(j)), 100)
                msg = mido.Message('note_off', note=convertNoteMidi(lastNote))
                outport.send(msg)
                msg = mido.Message('note_on', note=convertNoteMidi(track.playRow(j)))
                outport.send(msg)
                lastNote = track.playRow(j)
            if "=" in track.playRow(j).key:
                msg = mido.Message('note_off', note=convertNoteMidi(lastNote))
                outport.send(msg)
            root.update()
            time.sleep((60/songTempo)/gridSpeed)
            if (playMode == 0):
                break
    stopPlaying()
        
