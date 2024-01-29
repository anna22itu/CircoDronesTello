import time
import tkinter
from tkinter import *
import tkinter as tk

import requests
from tkinter import font
from PIL import Image, ImageTk
from tkvideo import tkvideo
from DetectorClass import DetectorClass
from FollowClass import FollowDetector
import BodyControlClass
from djitellopy import Tello
from PoseGeneratorDetectorClass import PoseGenerarorDetector
from tkinter import messagebox


class Scene:

    configured = False

    def Open(self, master, callback):
        self.configured = False
        self.callback = callback
        self.newWindow = Toplevel(master)

        self.newWindow.title("Scene")
        self.newWindow.geometry("700x500")
        self.mainFrame = tk.Frame(self.newWindow)
        self.mainFrame.pack()
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)
        self.mainFrame.rowconfigure(3, weight=1)
        self.mainFrame.rowconfigure(4, weight=1)
        self.mainFrame.rowconfigure(5, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)
        self.mainFrame.columnconfigure(3, weight=1)
        titleLbl = tk.Label (self.mainFrame,text = "Configuración del escenario")
        titleLbl.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)

        anchuraLbl = tk.Label(self.mainFrame, text="Anchura")
        anchuraLbl.grid(row=1, column=0, padx=5, pady=25, sticky=N + S + E + W)
        self.anchuraEntry = tk.Entry(self.mainFrame)
        self.anchuraEntry.grid(row=1, column=1, padx=5, pady=25, sticky=N + S + E + W)
        self.anchuraEntry.insert(0,'4')

        alturaLbl = tk.Label(self.mainFrame, text="Altura")
        alturaLbl.grid(row=2, column=0, padx=5, pady=25, sticky=N + S + E + W)
        self.alturaEntry = tk.Entry(self.mainFrame)
        self.alturaEntry.grid(row=2, column=1, padx=5, pady=25, sticky=N + S + E + W)
        self.alturaEntry.insert(0, '4')

        profundidadLbl = tk.Label(self.mainFrame, text="Profundidad")
        profundidadLbl.grid(row=3, column=0, padx=5, pady=25, sticky=N + S + E + W)
        self.profundidadEntry = tk.Entry(self.mainFrame)
        self.profundidadEntry.grid(row=3, column=1, padx=5, pady=25, sticky=N + S + E + W)
        self.profundidadEntry.insert(0, '4')

        alarmaLbl = tk.Label(self.mainFrame, text="Alarma")
        alarmaLbl.grid(row=4, column=0, padx=5, pady=25, sticky=N + S + E + W)
        self.alarmaEntry = tk.Entry(self.mainFrame)
        self.alarmaEntry.grid(row=4, column=1, padx=5, pady=25, sticky=N + S + E + W)
        self.alarmaEntry.insert(0, '8')

        self.image = Image.open("assets/escenario.png")
        self.image = self.image.resize((300, 300))
        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = Canvas(self.mainFrame, width=300, height=300)
        canvas1.grid(row=1, column=2, rowspan=4, padx=20, pady=20, sticky=N + S + E + W)

        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        closeBtn = tk.Button(self.mainFrame, text="Cerrar", bg='#F57328', fg="white",
                                  command=self.closeScenario)
        closeBtn.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)


    '''
    Función closeScenario. Guarda los valores que le entramos de la configuración (anchura, altura, profundidad y alarma).
    Cambia el valor de la variable configured a True y cierra la ventana
    '''
    def closeScenario (self):
        self.configured = True
        self.callback(int(self.anchuraEntry.get()),
                int(self.alturaEntry.get()),
                int(self.profundidadEntry.get()),
                int(self.alarmaEntry.get())
        )
        self.newWindow.destroy()
        print('Escenario configurado!')


'''
class Circo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        # don't assume that self.parent is a root window.
        # instead, call `winfo_toplevel to get the root window
        self.winfo_toplevel().title("Circo de drones")
'''

class Camera(Frame):

    selectionCamera = False
    int_camera = 0

    def Open(self, master):
        self.newWindow = Toplevel(master)
        self.selectionCamera = False
        self.int_camera = 0
        self.newWindow.title("Camera")
        self.newWindow.geometry("300x300")
        self.mainFrame = tk.Frame(self.newWindow)
        self.mainFrame.pack()
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)
        self.mainFrame.rowconfigure(3, weight=1)
        self.mainFrame.rowconfigure(4, weight=1)
        self.mainFrame.rowconfigure(5, weight=1)
        self.mainFrame.rowconfigure(6, weight=1)
        self.mainFrame.rowconfigure(7, weight=1)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)
        self.mainFrame.columnconfigure(3, weight=1)

        self.cameraSelection = tk.IntVar()  # Variable de control para los radiobutton
        self.cameraSelection.set(2)  # Por defecto va estar puesto el ordendador

        phoneBtn = tk.Radiobutton(self.mainFrame, text="Cámara del Móvil", variable=self.cameraSelection, value=1, command=self.updateSelection)
        computerBtn = tk.Radiobutton(self.mainFrame, text="Cámara del Ordenador", variable=self.cameraSelection, value=2, command=self.updateSelection)
        closeSelectBtn = tk.Button(self.mainFrame, text="Cerrar y guardar selección", bg='#F57328', fg="white",
                             command=self.closeSelection)

        phoneBtn.grid(row=3, column=1, sticky='w', padx=20, pady=(80, 0))
        computerBtn.grid(row=4, column=1, sticky='w', padx=20, pady=(0, 10))
        closeSelectBtn.grid(row=7, column=0, columnspan=3, pady=(80, 0))

    def updateSelection(self):
        # Si seleccionas el radiobutton del móvil, deselecciona el radiobutton del ordenador
        if self.cameraSelection.get() == 1:
            self.cameraSelection.set(1)

        # Si seleccionas el radiobutton del ordenador, deselecciona el radiobutton del móvil
        if self.cameraSelection.get() == 2:
            self.cameraSelection.set(2)

    def closeSelection(self):
        if self.cameraSelection.get() == 1:
            self.int_camera = 1
            print('Has seleccionado usar la cámara del móvil!')
        if self.cameraSelection.get() == 2:
            self.int_camera = 2
            print('Has seleccionado usar la cámara del ordenador!')
        self.newWindow.destroy()
        self.selectionCamera = True



class CircoPoses:

    def Open (self, master):
        self.scenario = Scene()
        self.camera = Camera()
        self.drone = Tello()
        self.master = master
        self.connectDrone = False
        self.poseList = None
        self.photos = None

        self.configure()
        '''
        self.mixer.music.load('assets/circo.mp3')
        self.mixer.music.play(10)

        self.newWindow = Toplevel(self.master)

        self.newWindow.geometry("770x525")

        self.image = Image.open("assets/entrada.png")
        self.image = self.image.resize((770, 525), Image.ANTIALIAS)

        self.bg = ImageTk.PhotoImage(self.image)
        canvas1 = Canvas(self.newWindow, width=770, height=525)
        canvas1.pack(fill="both", expand=True)
        canvas1.create_image(0, 0, image=self.bg, anchor="nw")

        myFont = font.Font(family='Arial', size=18, weight='bold')
        drone = Tello()
        configuracion_escenario = [0,0,0,0]

        enterButton = Button(self.newWindow, text="El circo de las poses", height=1, bg='#367E18', fg='#FFE9A0', width=12,
                             command=self.configure)
        enterButton['font'] = myFont
        enterButton.place(x=300, y=300, anchor="nw")
        # enterButton_canvas = canvas1.create_window(770 / 2, 525 / 2 + 50, window=enterButton)

        # Execute tkinter
        self.newWindow.mainloop()
        '''


    def follow(self):

        followWindow = Toplevel(self.circusWindow)
        followWindow.title("Sígueme")
        followWindow.geometry("450x650")
        # Presentation mode
        BodyControlClass.main()
        # detector = FollowDetector()
        # frame = detector.buildFrame(newWindow)
        # frame.pack(fill="both", expand="yes", padx=10, pady=10)
        followWindow.mainloop()

    def fingers(self):
        fingerWindow = Toplevel(self.circusWindow)
        fingerWindow.title("Dedos")
        fingerWindow.geometry("400x700")
        detector = DetectorClass(self.drone, self.configuracion_escenario, self.poseList, self.photos, self.camera.int_camera)
        frame = detector.buildFrame(fingerWindow, 'fingers')
        frame.pack(fill="both", expand="yes")
        fingerWindow.mainloop()

    def pose(self):
        poseWindow = Toplevel(self.circusWindow)
        poseWindow.title("Pose")
        poseWindow.geometry("200x700")
        detector = DetectorClass(self.drone, self.configuracion_escenario, self.poseList, self.photos, self.camera.int_camera)
        frame = detector.buildFrame(poseWindow, 'pose')
        frame.pack(fill="both", expand="yes")
        poseWindow.mainloop()

    def faces(self):
        newWindow = Toplevel(self.circusWindow)
        newWindow.title("Pose")
        newWindow.geometry("450x650")
        detector = DetectorClass(self.drone, self.configuracion_escenario, None, None)
        frame = detector.buildFrame(newWindow, 'face')
        frame.pack(fill="both", expand="yes", padx=10, pady=10)
        newWindow.mainloop()

    def bye(self):
        bye = Toplevel(self.circusWindow)
        bye.geometry("770x525")

        self.image = Image.open("assets/bye.png")
        self.image = self.image.resize((770, 525))
        self.bg = ImageTk.PhotoImage(self.image)
        canvas2 = Canvas(bye, width=770, height=525)
        canvas2.pack(fill="both", expand=True)
        canvas2.create_image(0, 0, image=self.bg, anchor="nw")
        #self.circusWindow.destroy()

        bye.mainloop()


    def empezar(self):
        if self.scenario.configured and self.connectDrone and self.camera.selectionCamera:
            print('El espectáculo acaba de empezar')
            self.circusWindow = Toplevel(self.configurationWindow)
            self.circusWindow.title("Selecciona un acto")
            self.circusWindow.geometry("800x600")
            self.circusWindow.columnconfigure(0, weight=1)
            self.circusWindow.columnconfigure(1, weight=1)
            self.circusWindow.columnconfigure(2, weight=1)
            self.circusWindow.columnconfigure(3, weight=1)
            self.circusWindow.rowconfigure(0, weight=1)
            self.circusWindow.rowconfigure(1, weight=1)

            self.image2 = Image.open("assets/circoPoses.png")
            self.image2 = self.image2.resize((800, 520))
            self.bg2 = ImageTk.PhotoImage(self.image2)
            canvas2 = Canvas(self.circusWindow, width=800, height=520)
            canvas2.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
            canvas2.create_image(0, 0, image=self.bg2, anchor="nw")
            myFont4 = font.Font(family='Arial', size=12, weight='bold')
            followmeButton = Button(self.circusWindow, text="Sígueme", height=1, bg='#367E18', fg='#FFE9A0', width=8, command=self.follow)
            followmeButton.place(x=50, y=480, anchor="nw")
            followmeButton['font'] = myFont4
            poseButton = Button(self.circusWindow, text="Poses", height=1, bg='#367E18', fg='#FFE9A0', width=8, command=self.pose)
            poseButton.place(x=450, y=480, anchor="nw")
            poseButton['font'] = myFont4
            fingersButton = Button(self.circusWindow, text="Dedos", height=1, bg='#367E18', fg='#FFE9A0', width=8,
                                   command=self.fingers)
            fingersButton.place(x=300, y=480, anchor="nw")
            fingersButton['font'] = myFont4

            facesButton = Button(self.circusWindow, text="Caras", height=1, bg='#367E18', fg='#FFE9A0', width=8,
                                 command=self.faces)
            facesButton.place(x=650, y=480, anchor="nw")
            facesButton['font'] = myFont4

            byeButton = Button(self.circusWindow, text="Salir", height=1, bg='#FFE9A0', fg='#367E18', command=self.bye)
            byeButton.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
            byeButton['font'] = myFont4
            self.circusWindow.mainloop()

        if not self.camera.selectionCamera and self.scenario.configured and self.connectDrone:
            messagebox.showwarning("Error", "Antes de empezar debes seleccionar la camara!", parent=self.master)
        if not self.connectDrone and self.scenario.configured and self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de empezar debes conectarte al dron!", parent=self.master)
        if not self.connectDrone and self.scenario.configured and not self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de empezar debes conectarte al dron y seleccionar la cámara!", parent=self.master)
        if not self.connectDrone and not self.scenario.configured and self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de empezar debes configurar tu dron y conectarte a él!", parent=self.master)
        if not self.connectDrone and not self.scenario.configured and not self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de empezar debes configurar tu dron, seleccionar la cámara y conectarte al dron!", parent=self.master)

    def guardar(self, anchura, altura, profundidad, alarma):
        self.configuracion_escenario = [anchura, altura, profundidad, alarma]

    def configureScenario(self):
        self.scenario.Open(self.configurationWindow, self.guardar)

    def camaraSelection(self):
        self.camera.Open(self.configurationWindow)

    def storePoses (self, poseList, photos):
        print('ya tengo las poses ', poseList)
        self.poseList = poseList
        self.photos = photos
        self.createWindow.destroy()

    def createPoses (self):
        if self.scenario.configured and self.camera.selectionCamera:
            print('Crea tus propias poses!')
            poseGeneratorDetector = PoseGenerarorDetector(self.camera.int_camera)
            self.createWindow = Toplevel(self.configurationWindow)
            self.createWindow.geometry('480x480')
            frame = poseGeneratorDetector.BuildFrame(self.createWindow, self.storePoses)
            frame.pack(fill=BOTH, expand=True)
            self.createWindow.mainloop()
        if not self.camera.selectionCamera and self.scenario.configured:
            messagebox.showwarning("Error", "Antes de nada selecciona la cámara!", parent=self.master)
        if not self.scenario.configured and self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de nada debes configurar tu dron!", parent=self.master)
        if not self.scenario.configured and not self.camera.selectionCamera:
            messagebox.showwarning("Error", "Antes de nada debes configurar tu dron y seleccionar la cámara!", parent=self.master)


    def connect(self):
        if self.scenario.configured:
            try:
                self.drone.connect()
                self.batteryLbl['text'] = "Nivel de batería: " + str(self.drone.get_battery())
                print('Conexión realizada correctamente!')
                print('Nivel de batería:', str(self.drone.get_battery()))
                self.connectDrone = True
            except Exception as e:
                messagebox.showerror("Error de conexión",
                                     "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e),
                                     parent=self.master)
        else:
            messagebox.showwarning("Error", "Antes de nada debes configurar tu dron!", parent=self.master)


    def configure (self):

        myFont2 = font.Font(family='Arial', size=10, weight='bold')

        self.configurationWindow = Toplevel(self.master)
        self.configurationWindow.title("Configurar y conectar")
        self.configurationWindow.geometry("800x600")
        self.configurationWindow.columnconfigure(0, weight=1)
        self.configurationWindow.columnconfigure(1, weight=1)
        self.configurationWindow.columnconfigure(2, weight=1)
        self.configurationWindow.columnconfigure(3, weight=1)

        self.configurationWindow.rowconfigure(0, weight=1)

        self.image2 = Image.open("assets/gallery3.png")
        self.image2 = self.image2.resize((800, 520))
        self.bg2 = ImageTk.PhotoImage(self.image2)
        canvas2 = Canvas(self.configurationWindow, width=800, height=520)
        canvas2.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky=N + S + E + W)
        canvas2.create_image(0, 0, image=self.bg2, anchor="nw")

        # Configurar button
        escenarioButton = Button(self.configurationWindow, text="Configura tu escenario antes de empezar!", height=1,
                                 bg='#367E18', fg='#FFE9A0', command=self.configureScenario)
        escenarioButton.place(x=270, y=140, anchor="nw")
        escenarioButton['font'] = myFont2

        # Configurar cámara
        camaraButton = Button(self.configurationWindow, text="Selecciona la cámara", height=1,
                                 bg='#367E18', fg='#FFE9A0', command=self.camaraSelection)
        camaraButton.place(x=320, y=210, anchor="nw")
        camaraButton['font'] = myFont2

        # Crea poses button
        definePosesButton = Button(self.configurationWindow, text="Crea tus poses", height=1, bg='#367E18',
                                 fg='#FFE9A0', command=self.createPoses)
        definePosesButton.place(x=230, y=460, anchor="nw")
        definePosesButton['font'] = myFont2

        # Conectar dron button
        connectButton = Button(self.configurationWindow, text="Conecta con el dron", height=1, bg='#367E18',
                               fg='#FFE9A0', command=self.connect)
        connectButton.place(x=330, y=280, anchor="nw")
        connectButton['font'] = myFont2

        # Nivel bateria label
        self.batteryLbl = Label(self.configurationWindow, text= "Nivel de bateria: ????", height=1, bg='#696969',
                                fg='#FFE9A0', borderwidth=2)
        self.batteryLbl.place(x=610, y=40, anchor="nw")
        self.batteryLbl['font'] = myFont2


        # Empezar espectaculo button
        empezarButton = Button(self.configurationWindow, text="Empezar expectáculo", height=1, bg='#367E18',
                               fg='#FFE9A0', command=self.empezar)
        empezarButton.place(x=490, y=460, anchor="nw")
        empezarButton['font'] = myFont2

        self.configurationWindow.mainloop()

