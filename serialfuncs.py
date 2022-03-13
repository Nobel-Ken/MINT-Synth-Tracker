from gridsnotes import note

from tkinter import *
from tkinter import messagebox

import serial.tools.list_ports

serialActive = 0
portsOld = serial.tools.list_ports.comports()
seriallink = 0

def setSerial():
    global serialActive
    global portsOld
    serialActive = 0
    portsOld = serial.tools.list_ports.comports()
    
def finishSerial(window):
    global serialActive
    global portsOld
    global seriallink
    portsNew = serial.tools.list_ports.comports()
    for x in portsNew:
        if (x not in portsOld):
            seriallink = serial.Serial(str(x.device), 115200)
            seriallink.timeout = 1
            messagebox.showinfo("Setup Finished!", "Device setup through port " + str(x.device))
            serialActive = 1
            break
    if (serialActive == 0):
        messagebox.showinfo("Setup Failed!", "Device not found!")
    window.destroy()

def packetEncode(pitch, leng):
    if (int(pitch) > 99999):
        pitch = 99999
    if (int(leng) > 9999):
        leng = 9999
    packet = "~"
    buf = str(pitch)
    loop = 5-(len(buf))
    for x in range(loop):
        packet += "0"
    packet += buf + "|"
    buf = str(leng)
    loop = 4-(len(buf))
    for x in range(loop):
        packet += "0"
    packet += buf + "~"
    return packet

def playNote(pitch, duration):
    if (serialActive == 1):
        seriallink.write(packetEncode(pitch, duration).encode())
