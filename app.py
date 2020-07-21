from ReadWriteMemory import ReadWriteMemory
import threading
import keyboard
import psutil
import os
import subprocess, signal
import sys

lifeTotal = 100
pointer = 0xA35B011C
minimumLife = 20
intervalCheck = 0.5
debug = True

process_name = "PathOfExileSteam"
pid = None

for proc in psutil.process_iter():
    if process_name in proc.name():
       pid = proc.pid
    else:
        print('ERROR: Path of Exile needs to be open!')
        sys.exit()

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

rwm = ReadWriteMemory()

process = rwm.get_process_by_name('PathOfExileSteam.exe')
process.open()

life_pointer = process.get_pointer(pointer)
lifeTotal = process.read(life_pointer)

def stay_safe(): 
    life = process.read(life_pointer)
    realLife = 100*life/lifeTotal
    percentLife = int(realLife)
    if debug is True:
        print(str(percentLife) + "%")

    if(percentLife <= minimumLife):
        os.system('taskkill /f /im PathOfExileSteam.exe')
        print('Exit!')
        sys.exit()

set_interval(stay_safe, intervalCheck)