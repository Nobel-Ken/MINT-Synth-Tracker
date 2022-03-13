from gridsnotes import grid

from tkinter import *
from tkinter import ttk

class track:
    
    DELETED_NAME = '1hfbeui'
    
    def __init__(self, label, songFrame, gridFrame, optionsFrame, root):
        self.column = label*3
        self.songFrame = songFrame
        self.gridFrame = gridFrame
        self.root = root
        self.currentGrid = 0 #index for the current row in the GRID tracker
        self.gridRows = 16
        self.grids = [grid(self.gridRows, self.gridFrame, self.column, "newgrid1")]
        self.gridNames = ["newgrid1"]
        self.trackGrids = [0]
        self.widgets = []
        
        self.nameEntry = ttk.Combobox(optionsFrame, values = self.gridNames)
        self.nameEntry.grid(row = 3, column = self.column, sticky = 'nsew', columnspan = 2)
        self.nameEntry.bind("<<ComboboxSelected>>", self.recallGrid)
        self.nameEntry.set(self.gridNames[0])
        self.nameApply = ttk.Button(optionsFrame, text = "Apply Name", command = self.renameGrid)
        self.nameApply.grid(row = 2, column = self.column, sticky = 'nsew')
        self.copyGrid = ttk.Button(optionsFrame, text = "Copy", command = self.copyGrid)
        self.copyGrid.grid(row = 2, column = self.column + 1, sticky = 'nsew')
        self.newGrid = ttk.Button(optionsFrame, text = "New", command = self.newGrid)
        self.newGrid.grid(row = 1, column = self.column, sticky = 'nsew')
        self.deleteGrid = ttk.Button(optionsFrame, text = "Delete", command = self.deleteGrid)
        self.deleteGrid.grid(row = 1, column = self.column + 1, sticky = 'nsew')
        
    def addGrid(self):
        self.trackGrids.append(self.trackGrids[-1])
        self.currentGrid += 1
        self.drawTrack()
        
    def newGrid(self):
        name = "newgrid"
        gridNum = 1
        while (name + str(gridNum) in self.gridNames):
            gridNum += 1
        name += (str(gridNum))
        self.grids.append(grid(self.gridRows, self.gridFrame, self.column, name))
        self.gridNames.append(name)
        self.nameEntry.configure(values = self.gridNames)
        self.nameEntry.set(name)
        self.loadGrid()
        self.drawTrack()
        
    def deleteGrid(self):
        if (len(self.gridNames) > 1):
            self.grids[self.trackGrids[self.currentGrid]].name = track.DELETED_NAME
            self.gridNames.clear()
            for grid in self.grids:
                if (grid.name != track.DELETED_NAME):
                    self.gridNames.append(grid.name)
            self.nameEntry.configure(values = self.gridNames)
        
    def copyGrid(self):
        name = self.grids[self.trackGrids[self.currentGrid]].name
        gridNum = '-'
        while (name + gridNum in self.gridNames):
            gridNum += '-'
        name += gridNum
        self.grids.append(grid(self.gridRows, self.gridFrame, self.column, name))
        self.gridNames.append(name)
        self.grids[-1].copy(self.grids[self.trackGrids[self.currentGrid]])
        self.grids[-1].name = name
        self.nameEntry.configure(values = self.gridNames)
        self.nameEntry.set(name)
        self.loadGrid()
        self.drawTrack()
        
    def removeGrid(self):
        if (len(self.trackGrids) > 1):
            self.currentGrid -= 1
            self.trackGrids.pop()
            self.drawTrack()
            
    def recallGrid(self, event):
        for i in range(len(self.grids)):
            if (self.grids[i].name == self.nameEntry.get()):
                self.trackGrids[self.currentGrid] = i
                break
        self.drawTrack()
            
    def loadGrid(self):
        for i in range(len(self.grids)):
            if (self.grids[i].name == self.nameEntry.get()):
                self.trackGrids[self.currentGrid] = i
                break
        self.drawTrack()
            
    def selectGrid(self, grid):
        self.grids[self.trackGrids[self.currentGrid]].unloadGrid()
        self.currentGrid = grid
        self.nameEntry.set(self.grids[self.trackGrids[self.currentGrid]].name)
        self.loadGrid()
        
    def renameGrid(self):
        name = self.nameEntry.get()
        if (name in self.gridNames and self.grids[self.trackGrids[self.currentGrid]].name != name):
            gridNum = 1
            while (name + str(gridNum) in self.gridNames):
                gridNum += 1
            name += str(gridNum)
        self.grids[self.trackGrids[self.currentGrid]].name = name
        self.gridNames.clear()
        for grid in self.grids:
            if (grid.name != track.DELETED_NAME):
                self.gridNames.append(grid.name)
        self.nameEntry.configure(values = self.gridNames)
        self.nameEntry.set(name)
        self.drawTrack()

    def drawTrack(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()
        for i in range(len(self.trackGrids)):
            textBuf = self.grids[self.trackGrids[i]].name
            if (i == self.currentGrid):
                textBuf += " <"
            self.widgets.append(ttk.Button(self.songFrame, text=textBuf, command = lambda x = i: self.selectGrid(x)))
            self.widgets[i].grid(row = i, column = round(self.column/3)+1, sticky = 'nsew')
        self.grids[self.trackGrids[self.currentGrid]].drawGrid()
        self.root.update()
        
    def playRow(self, row):
        self.grids[self.trackGrids[self.currentGrid]].playing = row
        self.grids[self.trackGrids[self.currentGrid]].drawGrid()
        return self.grids[self.trackGrids[self.currentGrid]].notes[row]

    def changeRows(self, count):
        for selected in self.grids:
            self.gridRows = count
            selected.changeSize(self.gridRows)
               
    def assignNote(self, new):
        self.grids[self.trackGrids[self.currentGrid]].assignNote(new)   