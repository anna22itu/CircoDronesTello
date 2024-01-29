
from tkinter import *
import tkinter as tk
from tkinter import font
import os
from djitellopy import Tello
import time
import cv2
import paho.mqtt.client as mqtt
import threading
from PIL import Image, ImageTk
from tkinter import messagebox
import base64
from slider import slider

class escenarioPanoramica:

    def Open(self, master):
        self.drone = Tello()
        self.pano_configuration = pano_configuration()

        myFont3 = font.Font(family='Arial', size=10, weight='bold')
        myFont4 = font.Font(family='Arial', size=8, weight='bold')

        self.windowPanoramic = Toplevel(master)

        # Variables
        self.detectingBool = False
        self.take_off = False
        self.connected = False
        self.panoramic = False

        # MQTT conexión
        self.global_broker_address = "broker.hivemq.com"
        self.global_broker_port = 8000  # 8883

        self.client = mqtt.Client("VideoService", transport="websockets")
        # self.client.username_pw_set("dronsEETAC", "mimara1456.")
        self.client.connect(self.global_broker_address, self.global_broker_port)
        self.client.loop_start()

        # Configuration
        self.windowPanoramic.geometry("900x600")
        self.windowPanoramic.rowconfigure(0, weight=1)
        self.windowPanoramic.rowconfigure(1, weight=1)
        self.windowPanoramic.rowconfigure(2, weight=1)
        self.windowPanoramic.rowconfigure(3, weight=1)

        self.windowPanoramic.columnconfigure(1, weight=1)
        self.windowPanoramic.columnconfigure(2, weight=1)
        self.windowPanoramic.columnconfigure(3, weight=1)

        self.windowPanoramic.title("Panoramic Page")

        self.imageCommand = Image.open("assets/cuadrado.png")
        self.imageCommand = self.imageCommand.resize((460, 450))
        self.photo = ImageTk.PhotoImage(self.imageCommand)
        image_label = tk.Label(self.windowPanoramic, image=self.photo)
        image_label.place(x=460, y=85)

        # Title label
        self.titlelabel = tk.Label(self.windowPanoramic, text="TAKE YOUR PANORAMIC!", height=3)
        self.titlelabel.place(x=400, y=15, anchor="nw")
        self.titlelabel['font'] = myFont3

        # Straight Line button
        self.panoramicButton = Button(self.windowPanoramic, text="Take your Panoramic", height=1, bg='#0000FF',
                                     fg='#F8F8FF', command=self.play_panoramic)
        self.panoramicButton.place(x=150, y=400, anchor="nw")
        self.panoramicButton['font'] = myFont3

        # Send Panoramic button
        self.sendPanoramicDButton = Button(self.windowPanoramic, text="Send", height=1, bg='#0000FF',
                                  fg='#F8F8FF', command=self.sendPanoramic)
        self.sendPanoramicDButton.place(x=330, y=400, anchor="nw")
        self.sendPanoramicDButton['font'] = myFont3

        # Command label
        self.commandlabel = tk.Label(self.windowPanoramic, text="Drone Commands", height=1)
        self.commandlabel.place(x=600, y=95, anchor="nw")
        self.commandlabel['font'] = myFont3

        # Connect button
        self.connectDButton = Button(self.windowPanoramic, text="Connect", height=1, bg='#367E18',
                                     fg='#F8F8FF', command=self.connect)
        self.connectDButton.place(x=633, y=155, anchor="nw")
        self.connectDButton['font'] = myFont3

        # TakeOff button
        self.takeoffDButton = Button(self.windowPanoramic, text="Take Off", height=1, bg='#FF6103',
                                     fg='#F8F8FF', command=self.takeoff)
        self.takeoffDButton.place(x=590, y=205, anchor="nw")
        self.takeoffDButton['font'] = myFont3

        # Land button
        self.landDButton = Button(self.windowPanoramic, text="Landing", height=1, bg='#FF6103',
                                  fg='#F8F8FF', command=self.land)
        self.landDButton.place(x=670, y=205, anchor="nw")
        self.landDButton['font'] = myFont3

        # Forward button
        self.forwardButton = Button(self.windowPanoramic, text="Forward ", height=1, bg='#FF8C00',
                                    fg='#F8F8FF', command=self.forward)
        self.forwardButton.place(x=630, y=265, anchor="nw")
        self.forwardButton['font'] = myFont3

        # Backward button
        self.backwardButton = Button(self.windowPanoramic, text="Backward", height=1, bg='#FF8C00',
                                     fg='#F8F8FF', command=self.backward)
        self.backwardButton.place(x=630, y=345, anchor="nw")
        self.backwardButton['font'] = myFont3

        # FLip button
        self.flipButton = Button(self.windowPanoramic, text="  Flip  ", height=1, bg='#FF8C00',
                                 fg='#F8F8FF', command=self.flip)
        self.flipButton.place(x=640, y=305, anchor="nw")
        self.flipButton['font'] = myFont3

        # Left button
        self.leftButton = Button(self.windowPanoramic, text="  Left  ", height=1, bg='#FF8C00',
                                 fg='#F8F8FF', command=self.left)
        self.leftButton.place(x=570, y=305, anchor="nw")
        self.leftButton['font'] = myFont3

        # Right button
        self.rightButton = Button(self.windowPanoramic, text=" Right ", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.right)
        self.rightButton.place(x=710, y=305, anchor="nw")
        self.rightButton['font'] = myFont3

        # Up button
        self.upButton = Button(self.windowPanoramic, text="  Up  ", height=1, bg='#FF6103',
                               fg='#F8F8FF', command=self.up)
        self.upButton.place(x=610, y=415, anchor="nw")
        self.upButton['font'] = myFont3

        # Down button
        self.downButton = Button(self.windowPanoramic, text="Down", height=1, bg='#FF6103',
                                 fg='#F8F8FF', command=self.down)
        self.downButton.place(x=670, y=415, anchor="nw")
        self.downButton['font'] = myFont3

        # Close window button
        self.closeButton = Button(self.windowPanoramic, text="Close", height=1, bg='#8B0000',
                                   fg='#F8F8FF', command=self.closePan)
        self.closeButton.place(x=840, y=560, anchor="nw")
        self.closeButton['font'] = myFont3

        # Info enter label
        self.infoEnterLabel = tk.Label(self.windowPanoramic, text="Enter your length:", height=3)
        self.infoEnterLabel.place(x=200, y=120, anchor="nw")
        self.infoEnterLabel['font'] = myFont3

        # Input metros label
        self.meterslabel = tk.Entry(self.windowPanoramic, validate="key", bg='white')
        self.meterslabel.place(x=200, y=170, anchor="nw")
        self.meterslabel['font'] = myFont3

        # Info label
        self.infoLabel = tk.Label(self.windowPanoramic,text="Distance guide:", height=3)
        self.infoLabel.place(x=200, y=210, anchor="nw")
        self.infoLabel['font'] = myFont3

        # Info1 label
        self.info1Label = tk.Label(self.windowPanoramic, text="Distance: 4 meters - Length: 50", height=1)
        self.info1Label.place(x=180, y=260, anchor="nw")
        self.info1Label['font'] = myFont3
        self.info1Label['fg'] = 'red'


        # Info2 label
        self.info2Label = tk.Label(self.windowPanoramic, text="Distance: 5.5 meters - Length: 80", height=1)
        self.info2Label.place(x=180, y=280, anchor="nw")
        self.info2Label['font'] = myFont3
        self.info2Label['fg'] = 'red'


    def connect(self):
        try:
            self.connected = True
            # muestro el nivel de bateria
            self.connectDButton['text'] = str(self.drone.get_battery())
            #self.panoramic = True
            self.connectDButton.place(x=650, y=155, anchor="nw")
            self.connectDButton['bg'] = '#8B0000'
            print("Te has conectado correctamente al dron!")

            if not self.detectingBool:
                self.detectingBool = True
                x = threading.Thread(target=self.detecting)
                x.start()
            print("Se estan transmitiendo las imágenes de la cámara del dron")

        except Exception as e:
            messagebox.showerror("Error de conexión", "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e), parent=self.windowPanoramic)

    def detecting(self):
        self.drone.streamon()
        cv2.namedWindow("Tello Camera", cv2.WINDOW_NORMAL)

        while self.detectingBool and self.connected:
            frame = self.drone.get_frame_read().frame  # Captura un frame desde la cámara del Tello
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Tello Camera", frame_rgb)  # Muestra el frame en una ventana
            cv2.waitKey(1)

    def takeoff(self):
        if self.connected:
            self.drone.takeoff()
            time.sleep(1)
            self.take_off = True
            self.panoramic = True
            self.takeoffDButton['text'] = 'flying'
            self.takeoffDButton['bg'] = '#8B0000'
            self.state = 'flying'
        else:
            messagebox.showwarning("Error", "Antes de despegar debes conectarte al dron", parent=self.windowPanoramic)

    def land(self):
        self.drone.land()
        messagebox.showwarning("Success", "Ya estamos en casa", parent=self.windowPanoramic)

    def forward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(25, 0, 0, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def backward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(-25, 0, 0, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def flip(self):
        if self.take_off and self.connected:
            self.drone.send_control_command("flip l")
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def left(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, -25, 0, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def right(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 25, 0, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def up(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, 75, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def down(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, -25, 100)
            time.sleep(0.5)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def play_panoramic(self):
        #self.panoramic = True
        if self.take_off and self.connected and self.panoramic:
            self.pano_configuration.Open(self.drone, self.meterslabel.get())
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowPanoramic)

    def sendPanoramic(self):
        image_path = "assets/telloPanoramic/result.jpg"
        quality = 50
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        with open(image_path, "rb") as image_file:
            image_data = cv2.imread(image_path)
            _, frameComp = cv2.imencode(".jpg", image_data, encode_param)
            image_base64 = base64.b64encode(frameComp)
            print('size: ', frameComp.shape[0])
            self.client.publish("PanoramicaAnna", payload=image_base64, qos=2)

    def closePan(self):
        self.windowPanoramic.destroy()
        cv2.destroyAllWindows()


class pano_configuration:

    def Open(self, drone, length):

        self.mySlider = slider()
        self.panoramicBool = False
        self.length = length
        print(drone.get_battery())
        self.record_pano(drone)

    def record_pano(self, mydrone):

        # 10 metros (150)
        # 5,6 metros (100)
        # length = 90
        print('length: ', self.length)
        images = []

        mydrone.set_video_direction(mydrone.CAMERA_FORWARD)

        folder_path = 'assets/telloPanoramic/'

        interval = 0

        self.panoramicBool = True
        while interval < self.length:
            if self.panoramicBool:
                filename = os.path.join(folder_path, f'image_{interval}.jpg')

                image = mydrone.get_frame_read().frame
                if image is not None:
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(filename, image)
                    images.append(image)
                    print('images', images)

                mydrone.send_rc_control(30, 0, 0, 0) #left_right_velocity: 30 (escala -100:100)
                #velocidad_actual = mydrone.get_speed_x()
                #print('velocidad',velocidad_actual)
                interval = interval + 5
                time.sleep(0.75)

        print('images', len(images))
        #stitcher = cv2.Stitcher_create()
        #self.result = stitcher.stitch((tuple(images)))
        #cv2.imwrite('assets/telloPanoramic/result.jpg', self.result[1])
        self.panoramicBool = False
        print('iresult')

        mydrone.land()
        self.makePano()
        self.callSlider()

    def makePano(self):
        images = []
        folder_path = 'assets/telloPanoramic/'

        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.jpg'):
                file_path = os.path.join(folder_path, file_name)
                img = cv2.imread(file_path)
                if img is not None:
                    images.append(img)
                else:
                    print(f"Error cargando la imagen: {file_path}")


        # Luego intenta realizar la unión de imágenes
        stitcher = cv2.Stitcher_create()
        result = stitcher.stitch(tuple(images))

        cv2.imwrite('assets/telloPanoramic/result.jpg', result[1])
        print('result')

    def callSlider(self):
        imagen_path = 'assets/telloPanoramic/result.jpg'  # Reemplaza con la ruta de tu imagen si quieres especificarla directamente.
        self.mySlider.agregar_borde_rojo_con_slider(imagen_path)