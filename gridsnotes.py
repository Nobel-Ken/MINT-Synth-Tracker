from tkinter import *
from tkinter import ttk

class instrument:
    def __init__(self):
        self.type = "NONE"
        self.pitchList = []
        self.pitchSpeed = 1
        self.pitchLoop = False

class note:
    def __init__(self, key, octave, instrument):
        self.key = key
        self.octave = octave
        self.instrument = instrument

class grid:
    MAX_GRID_SIZE = 64
    OFFSET = 5
    COLUMNSPAN = 1
    def __init__(self, size, frame, column, name):
        self.size = size
        self.notes = []
        for i in range(grid.MAX_GRID_SIZE):
            self.notes.append(note("--", "-", "--"))
        self.widgets = []
        self.selected = -1
        self.playing = 0
        self.frame = frame
        self.column = column
        self.name = name
        
    def copy(self, grid):
        self.size = grid.size
        for i in range(self.size):
            self.notes[i] = grid.notes[i]
        self.frame = grid.frame
        self.column = grid.column
        self.name = grid.name
        
    def drawGrid(self):
        self.selected = -1
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        for i in range(self.size):
            if (len(self.notes[i].key) == 1):
                textBuf = self.notes[i].key + "  - " + str(self.notes[i].octave) + " - " + str(self.notes[i].instrument)
            else:
                textBuf = self.notes[i].key + " - " + str(self.notes[i].octave) + " - " + str(self.notes[i].instrument)
            self.widgets.append(ttk.Button(self.frame, text=textBuf, command = lambda x = i: self.selectRow(x)))
            self.widgets[i].grid(row = i + grid.OFFSET, column = self.column, sticky = 'nsew', columnspan = grid.COLUMNSPAN)
            if (i == self.playing):
                self.widgets[i].configure(state = ACTIVE)
            else:
                self.widgets[i].configure(state = NORMAL)
        
    def unloadGrid(self):
        self.selected = -1
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
            
    def changeSize(self, count):
        self.size = count
        if (self.size > grid.MAX_GRID_SIZE):
            self.size = grid.MAX_GRID_SIZE
        self.drawGrid()

    def selectRow(self, row):
        self.drawGrid()
        self.selected = row
        self.widgets[row].destroy()
        self.widgets[row] = ttk.Button(self.frame, text="?? - ? - ??", command = lambda x = row: self.selectRow(x))
        self.widgets[row].grid(row = row + grid.OFFSET, column = self.column, sticky = 'nsew', columnspan = grid.COLUMNSPAN)
    
    def deselectRow(self, row):
        self.drawGrid()
        self.widgets[row].destroy()
        self.widgets[row] = ttk.Button(self.frame, text=self.notes[row].key, command = lambda x = row: self.selectRow(x))
        self.widgets[row].grid(row = row, column = self.column, sticky = 'nsew')

    def assignNote(self, new):
        if (self.selected != -1):
            self.notes[self.selected] = new
            self.drawGrid()