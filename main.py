import states
import serialfuncs
from tracks import track

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

def no():
    messagebox.showinfo("Failure", "Not Yet Implemented")

root = ThemedTk(theme="black", gif_override = True)
root.title("MINT v0.5")
icon = PhotoImage(file = "icon.png")
root.iconphoto(False, icon)

currentInstrument = StringVar()

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

visualFrame = ttk.LabelFrame(root)
visualFrame.grid(row = 0, column = 0, rowspan = 2, sticky = 'nsew')
gridFrame = ttk.LabelFrame(root, text = "Grid Tracker")
gridFrame.grid(row = 0, column = 1, sticky = 'nsew')
noteFrame = ttk.LabelFrame(root, text = "Note Tracker")
noteFrame.grid(row = 0, column = 2, sticky = 'nsew', rowspan = 4)
songFrame = ttk.LabelFrame(root, text = "Song Settings")
songFrame.grid(row = 1, column = 1, sticky = 'nsew')
pianoFrame = ttk.LabelFrame(root, text = "Piano Settings")
pianoFrame.grid(row = 2, column = 1, sticky = 'nsew')
connectionFrame = ttk.LabelFrame(root, text = "Connections")
connectionFrame.grid(row = 2, column = 0, rowspan = 2, sticky = 'nsew')
modeFrame = ttk.LabelFrame(root, text = "Mode")
modeFrame.grid(row = 3, column = 1, sticky = 'nsew')

def serialSetup():
    configWindow = Toplevel()
    Label(configWindow, text = "While the synth is disconected from the computer, press the SET button.").pack()
    Button(configWindow, text = "SET", command = serialfuncs.setSerial).pack()
    Label(configWindow, text = "After pressing SET, connect the synth and press DONE.").pack()
    Button(configWindow, text = "DONE", command = lambda x = configWindow : serialfuncs.finishSerial(x)).pack()
    
def apply(tracks, tempo, grids, speed):
    states.songSettingsApply(tracks, tempo, grids, speed)
    root.update()
    canvas.configure(scrollregion=canvas.bbox("all"))

noteFrame.grid_columnconfigure(0, weight=1)
noteFrame.grid_columnconfigure(1, weight=1)

connectionFrame.grid_columnconfigure(0, weight=1)
connectionFrame.grid_rowconfigure(0, weight=1)

modeFrame.grid_columnconfigure(0, weight=1)
modeFrame.grid_columnconfigure(1, weight=1)
modeFrame.grid_rowconfigure(0, weight=1)
modeFrame.grid_rowconfigure(1, weight=1)

cardimg = PhotoImage(file = "cardimg.png")
ttk.Label(visualFrame, image=cardimg).pack()

canvasScroll = ttk.Scrollbar(noteFrame, orient=VERTICAL)
canvasScroll.grid(row = 4, column = 2, sticky = "ns")
canvas = Canvas(noteFrame, width = 202, height = 476, scrollregion=(0,0,0,476), bd=0, highlightthickness=0, yscrollcommand = canvasScroll.set)
canvas.grid(row = 4, column = 0, columnspan = 2, sticky = "nsew")
canvasScroll['command'] = canvas.yview
scrollFrame = Frame(canvas)
window = canvas.create_window(0,0, window = scrollFrame, anchor = "nw", height = 476)


scrollFrame.rowconfigure(0, weight=1)
scrollFrame.columnconfigure(0, weight=1)
scrollFrame.rowconfigure(0, weight=1)
testFrame = ttk.LabelFrame(scrollFrame, text = "Track 1")
testFrame.grid(row = 0, column = 0, sticky = 'nsew')
testFrame.columnconfigure(0, weight=1)

tracks = [track(0, gridFrame, testFrame, noteFrame, root)]#, track(2, gridFrame, scrollFrame, noteFrame)]
tracks[0].drawTrack()
canvas.itemconfigure(window, width = noteFrame.winfo_width())

def resize(event):
    canvas.itemconfigure(window, width = noteFrame.winfo_width()-2)
    canvas.itemconfigure(window, height = noteFrame.winfo_height()+200)

#tracks[1].drawTrack()
root.bind("<Key>", lambda event, x = tracks, y = currentInstrument : states.keyPush(event, x, y))
root.bind("<KeyRelease>", states.keyRelease)
root.bind("<BackSpace>", lambda event, x = tracks : states.delPush(event, x))
root.bind("<Tab>", lambda event, x = tracks : states.breakPush(event, x))
root.bind("<Configure>", resize)
gridAdd = ttk.Button(gridFrame, text = '+', command = tracks[0].addGrid)
gridAdd.grid(row = 0, column = 0)
gridAdd = ttk.Button(gridFrame, text = '-', command = tracks[0].removeGrid)
gridAdd.grid(row = 1, column = 0)

ttk.Label(songFrame, text="Tempo").grid(row = 1, column = 0)
tempoSong = ttk.Entry(songFrame)
tempoSong.insert(0, "120")
tempoSong.grid(row = 1, column = 1)
ttk.Label(songFrame, text="Grids").grid(row = 2, column = 0)
gridsSong = ttk.Entry(songFrame)
gridsSong.insert(0, "16")
gridsSong.grid(row = 2, column = 1)
ttk.Label(songFrame, text="Grid Speed").grid(row = 3, column = 0)
speedSong = ttk.Entry(songFrame)
speedSong.insert(0, "4")
speedSong.grid(row = 3, column = 1)
applySong = ttk.Button(songFrame, text = "Apply", command = lambda t = tracks, x = tempoSong, y = gridsSong, z = speedSong : apply(t, x, y, z))
applySong.grid(row = 0, column = 0, columnspan = 2)

ttk.Label(pianoFrame, text= "Octave").grid(row = 0, column = 0, columnspan = 3)
createInstrument = ttk.Button(pianoFrame, text = "-", command = lambda x = pianoFrame : states.decreaseOctave(x))
createInstrument.grid(row = 1, column = 0)
ttk.Label(pianoFrame, text= str(states.pianoOctave)).grid(row = 1, column = 1)
deleteInstrument = ttk.Button(pianoFrame, text = "+", command = lambda x = pianoFrame : states.increaseOctave(x))
deleteInstrument.grid(row = 1, column = 2)

serialConnection = ttk.Button(connectionFrame, text = "Serial", command = serialSetup)
serialConnection.grid(row = 0, column = 0, sticky = 'nsew')

playFMode = ttk.Button(modeFrame, text = "Play Frame", command = lambda x = tracks[0], y = root : states.playFrame(x, y))
playFMode.grid(row = 0, column = 0, sticky = 'nsew')
stopMode = ttk.Button(modeFrame, text = "Stop", command = states.stopPlaying)
stopMode.grid(row = 0, column = 1, sticky = 'nsew', rowspan = 3)
playSMode = ttk.Button(modeFrame, text = "Play Song", command = lambda x = tracks[0], y = root : states.playSong(x, y))
playSMode.grid(row = 1, column = 0, sticky = 'nsew')

def quitProgram():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        quit()

root.protocol("WM_DELETE_WINDOW", quitProgram)

root.mainloop()
#while 1:
#    root.update()