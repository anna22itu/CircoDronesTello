import cv2 as cv
from djitellopy import Tello
from ColorDetector import ColorDetector
from Calibrador import Calibrador
from tkinter import *
from tkinter.ttk import *
import tkinter as tk

def Conectar():
    tello.connect()
    print(tello.get_battery())

def Calibrar():
    calibrador = Calibrador()
    calibrador.Open(main, tello, colorDetector)

def Verificar ():
    tello.streamon()
    while True:
        img = tello.get_frame_read().frame
        img, color = colorDetector.DetectColor(img)
        cv.imshow('frame', img)
        cv.waitKey(1)



main = Tk()
main.title  ("Ventana principal")
conectarBtn = tk.Button(main,
                   text="Conectar con el dron",
                     bg='red',
                   command=Conectar)
conectarBtn.pack()
calibrarBtn = tk.Button(main,
                   text="Calibrar",
                   command=Calibrar)
calibrarBtn.pack()
verificarBtn = tk.Button(main,
                   text="Verificar",
                   command=Verificar)
verificarBtn.pack()

tello = Tello()
colorDetector = ColorDetector()

main.mainloop()
'''
tello = Tello()
colorDetector = ColorDetector()
tello.connect()
print(tello.get_battery())


tello.streamon()
while True:
    img = tello.get_frame_read().frame
    img, color = colorDetector.DetectColor(img)
    img = colorDetector.MarkFrameForCalibration(img)
    cv.imshow('frame', img)
    cv.waitKey(1)

'''

