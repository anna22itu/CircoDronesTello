import base64
from tkinter import *
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from tkinter import messagebox
from djitellopy import Tello
import time
import cv2
import os
import paho.mqtt.client as mqtt
import threading
from Gallery import GalleryMedia

class escenarioImagenes:

    def Open(self, master):
        self.drone = Tello()
        #self.galleryImages = galleryImages()
        self.galleryImages = GalleryMedia()

        myFont3 = font.Font(family='Arial', size=10, weight='bold')

        self.windowImage = Toplevel(master)

        # Variables
        self.takePictureBool = False
        self.take_off = False
        self.connected = False
        self.detectingBool = False
        self.photo = None
        self.vect_images = []
        self.count = 0

        # MQTT conexión
        print("aaaa")
        self.global_broker_address = "broker.hivemq.com"
        self.global_broker_port = 8000  # 8883

        self.client = mqtt.Client("VideoService", transport="websockets")
        # self.client.username_pw_set("dronsEETAC", "mimara1456.")
        self.client.connect(self.global_broker_address, self.global_broker_port)
        self.client.loop_start()

        # Configuration
        self.windowImage.geometry("900x600")
        self.windowImage.rowconfigure(0, weight=1)
        self.windowImage.rowconfigure(1, weight=1)
        self.windowImage.rowconfigure(2, weight=1)
        self.windowImage.rowconfigure(3, weight=1)

        self.windowImage.columnconfigure(1, weight=1)
        self.windowImage.columnconfigure(2, weight=1)
        self.windowImage.columnconfigure(3, weight=1)

        self.windowImage.title("Foto Page")

        self.imageCommand = Image.open("assets/cuadrado.png")
        self.imageCommand = self.imageCommand.resize((460, 450))
        self.photo = ImageTk.PhotoImage(self.imageCommand)
        image_label = tk.Label(self.windowImage, image=self.photo)
        image_label.place(x=460, y=85)

        # Title label
        self.titlelabel = tk.Label(self.windowImage, text="TAKE YOUR PICTURE!", height=3)
        self.titlelabel.place(x=400, y=15, anchor="nw")
        self.titlelabel['font'] = myFont3

        # Command label
        self.commandlabel = tk.Label(self.windowImage, text="Drone Commands", height=1)
        self.commandlabel.place(x=600, y=95, anchor="nw")
        self.commandlabel['font'] = myFont3

        # Connect button
        self.connectDButton = Button(self.windowImage, text="Connect", height=1, bg='#367E18',
                            fg='#F8F8FF', command=self.connect)
        self.connectDButton.place(x=633, y=155, anchor="nw")
        self.connectDButton['font'] = myFont3

        # TakeOff button
        self.takeoffDButton = Button(self.windowImage, text="Take Off", height=1, bg='#FF6103',
                                     fg='#F8F8FF', command=self.takeoff)
        self.takeoffDButton.place(x=590, y=205, anchor="nw")
        self.takeoffDButton['font'] = myFont3

        # Land button
        self.landDButton = Button(self.windowImage, text="Landing", height=1, bg='#FF6103',
                                     fg='#F8F8FF', command=self.land)
        self.landDButton.place(x=670, y=205, anchor="nw")
        self.landDButton['font'] = myFont3

        # Forward button
        self.forwardButton = Button(self.windowImage, text="Forward ", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.forward)
        self.forwardButton.place(x=630, y=265, anchor="nw")
        self.forwardButton['font'] = myFont3

        # Backward button
        self.backwardButton = Button(self.windowImage, text="Backward", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.backward)
        self.backwardButton.place(x=630, y=345, anchor="nw")
        self.backwardButton['font'] = myFont3

        # FLip button
        self.flipButton = Button(self.windowImage, text="  Flip  ", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.flip)
        self.flipButton.place(x=640, y=305, anchor="nw")
        self.flipButton['font'] = myFont3

        # Left button
        self.leftButton = Button(self.windowImage, text="  Left  ", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.left)
        self.leftButton.place(x=570, y=305, anchor="nw")
        self.leftButton['font'] = myFont3

        # Right button
        self.rightButton = Button(self.windowImage, text=" Right ", height=1, bg='#FF8C00',
                                  fg='#F8F8FF', command=self.right)
        self.rightButton.place(x=710, y=305, anchor="nw")
        self.rightButton['font'] = myFont3

        # Up button
        self.upButton = Button(self.windowImage, text="  Up  ", height=1, bg='#FF6103',
                                  fg='#F8F8FF', command=self.up)
        self.upButton.place(x=610, y=415, anchor="nw")
        self.upButton['font'] = myFont3

        # Down button
        self.downButton = Button(self.windowImage, text="Down", height=1, bg='#FF6103',
                                  fg='#F8F8FF', command=self.down)
        self.downButton.place(x=670, y=415, anchor="nw")
        self.downButton['font'] = myFont3

        # Gallery button
        self.galleryButton = Button(self.windowImage, text="Image gallery", height=1, bg='#458B74',
                                    fg='#F8F8FF', command=self.gallery)
        self.galleryButton.place(x=780, y=20, anchor="nw")
        self.galleryButton['font'] = myFont3

        # Canvas
        self.canvas1 = Canvas(self.windowImage, width=355, height=400, bg='white')
        self.canvas1.place(x=90, y=110, anchor="nw")

        # Take picture button
        self.takePictureButton = Button(self.windowImage, text="Take Picture", height=1, bg='#0000FF',
                                   fg='#F8F8FF', command=self.takePicture)
        self.takePictureButton.place(x=170, y=530, anchor="nw")
        self.takePictureButton['font'] = myFont3

        # Send picture button
        self.sendButton = Button(self.windowImage, text="Send Picture", height=1, bg='#0000FF',
                                 fg='#F8F8FF', command=self.sendSave)
        self.sendButton.place(x=270, y=530, anchor="nw")
        self.sendButton['font'] = myFont3

        # Close window button
        self.closeDButton = Button(self.windowImage, text="Close", height=1, bg='#8B0000',
                                 fg='#F8F8FF', command=self.closeImg)
        self.closeDButton.place(x=840, y=560, anchor="nw")
        self.closeDButton['font'] = myFont3

    def connect(self):
        try:
            self.connected = True
            # muestro el nivel de bateria
            self.connectDButton['text'] = str(self.drone.get_battery())
            self.connectDButton.place(x=650, y=155, anchor="nw")
            self.connectDButton['bg'] = '#8B0000'
            print("Te has conectado correctamente al dron!")

            if not self.detectingBool:
                self.detectingBool = True
                x = threading.Thread(target=self.detecting)
                x.start()
            print("Se estan transmitiendo las imágenes de la cámara del dron")

        except Exception as e:
            messagebox.showerror("Error de conexión", "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e), parent=self.windowImage)

    def takeoff(self):
        if self.connected:
            self.drone.takeoff()
            time.sleep(2)
            self.take_off = True
            self.takeoffDButton['text'] = 'flying'
            self.takeoffDButton['bg'] = '#8B0000'
            self.state = 'flying'
        else:
            messagebox.showwarning("Error", "Antes de despegar debes conectarte al dron", parent=self.windowImage)

    def land(self):
        self.drone.land()
        messagebox.showwarning("Success", "Ya estamos en casa", parent=self.windowImage)

    def forward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(50, 0, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def backward(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(-50, 0, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def flip(self):
        if self.take_off and self.connected:
            self.drone.send_control_command("flip l")
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def left(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, -50, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def right(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 50, 0, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def up(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, 50, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def down(self):
        if self.take_off and self.connected:
            self.drone.go_xyz_speed(0, 0, -50, 100)
            time.sleep(1)
        else:
            messagebox.showwarning("Error", "Primero despega el dron", parent=self.windowImage)

    def takePicture(self):
        if self.connected:
            self.count = self.count + 1
            self.frame = self.drone.get_frame_read().frame
            self.imgPicture = Image.fromarray(self.frame)
            self.imgPicture = self.imgPicture.resize((355, 400))

            self.photo = ImageTk.PhotoImage(self.imgPicture)
            self.canvas1.delete("all")  # Borramos cualquier contenido previo en el canvas
            self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas1.image = self.photo
            self.takePictureBool = True
            print("Foto tomada")
        else:
            messagebox.showwarning("Error", "Primero conéctate con el dron!", parent=self.windowImage)

    def sendSave(self):
        try:
            if self.photo and self.takePictureBool:
                self.vect_images.append(self.photo)
                frame_brg = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite("assets/telloImages/foto_tello" + str(self.count) + ".jpg", frame_brg)

                self.sendmqtt()

                print("Foto enviada y guardada")
                return self.photo
            else:
                print("No hay foto para enviar")
                return None
        except Exception as e:
            messagebox.showerror("Error de conexión",
                                 "No se pudo conectar al dron. Por favor, inténtalo de nuevo.\nError: " + str(e),
                                 parent=self.windowImage)

    def sendmqtt(self):
        image_path = "assets/telloImages/foto_tello" + str(self.count) + ".jpg"
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data)
            self.client.publish("ImagenAnna", payload=image_base64, qos=2)

    def gallery(self):
        type = 'Image'
        self.galleryImages.Open(self.windowImage,type)

    def closeImg(self):
        if len(self.vect_images) == 0:
            messagebox.showwarning("Error", "No has guardado ninguna imagen!", parent=self.windowImage)
        else:
            print("Has guardado " + str(len(self.vect_images)) + "imagenes: " + str(self.vect_images))
            self.drone.streamoff()
            self.detectingBool = False
            self.windowImage.destroy()
            cv2.destroyAllWindows()

    def detecting(self):
        self.drone.streamon()
        cv2.namedWindow("Tello Camera", cv2.WINDOW_NORMAL)

        while self.detectingBool and self.connected:
            frame = self.drone.get_frame_read().frame  # Captura un frame desde la cámara del Tello
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imshow("Tello Camera", frame_rgb)  # Muestra el frame en una ventana
            cv2.waitKey(1)

'''
class galleryImages:

    def Open(self, master):
        self.drone = Tello()

        myFont3 = font.Font(family='Arial', size=10, weight='bold')

        self.windowGallery = Toplevel(master)
        self.selected_image = None
        self.v_images = []
        self.canvas_list = []
        self.number_img = 0

        # MQTT conexión
        # MQTT conexión
        self.global_broker_address = "broker.hivemq.com"
        self.global_broker_port = 8000  # 8883

        self.client = mqtt.Client("VideoService", transport="websockets")
        # self.client.username_pw_set("dronsEETAC", "mimara1456.")
        self.client.connect(self.global_broker_address, self.global_broker_port)
        self.client.loop_start()

        # Title label
        self.titlelabel = tk.Label(self.windowGallery, text="Images Gallery", height=2)
        self.titlelabel.place(x=500, y=15, anchor="nw")
        self.titlelabel['font'] = myFont3

        self.windowGallery.geometry("1200x600")
        self.windowGallery.rowconfigure(0, weight=1)
        self.windowGallery.rowconfigure(1, weight=1)
        self.windowGallery.rowconfigure(2, weight=1)
        self.windowGallery.rowconfigure(3, weight=1)

        self.windowGallery.columnconfigure(1, weight=1)
        self.windowGallery.columnconfigure(2, weight=1)
        self.windowGallery.columnconfigure(3, weight=1)

        # Send pictures from gallery button
        self.sendGallerybtn = Button(self.windowGallery, text="Send Picture", height=1, bg='#0000FF',
                                     fg='#F8F8FF', command=self.sendGallery)
        self.sendGallerybtn.place(x=500, y=530, anchor="nw")
        self.sendGallerybtn['font'] = myFont3

        # Close gallery button
        self.closeGalleryButton = Button(self.windowGallery, text="Close", height=1, bg='#8B0000',
                                     fg='#F8F8FF', command=self.closeGallery)
        self.closeGalleryButton.place(x=1140, y=550, anchor="nw")
        self.closeGalleryButton['font'] = myFont3

        self.url_images = "assets/telloImages/"
        self.create_vector_images(self.url_images)

        if len(self.v_images) < 0:
            messagebox.showerror("Error", "No has guardado ninguna foto")
        else:
            self.create_gallery()

    def create_vector_images(self, folder_path):

        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.jpg'):
                file_path = os.path.join(folder_path, file_name)
                self.v_images.append(file_path)

    def create_gallery(self):
        num_images_per_row = 6  # Número deseado de imágenes por fila
        max_image_size = 300  # Tamaño máximo de las imágenes
        min_image_size = 200  # Tamaño mínimo de las imágenes
        starting_row = 0
        padding = 20

        total_images = len(self.v_images)

        for i, image_path in enumerate(self.v_images):
            img = Image.open(image_path)

            if total_images <= num_images_per_row:
                num_images_per_row = 4
                image_size = max_image_size
            else:
                image_size = min_image_size

            img.thumbnail((image_size, image_size))
            photo = ImageTk.PhotoImage(img)
            # photo_r = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)

            canvas = tk.Canvas(self.windowGallery, width=image_size, height=image_size)
            canvas.create_image(0, 0, anchor="nw", image=photo)

            row_position = starting_row + i // num_images_per_row
            col_position = i % num_images_per_row

            self.number_img += 1

            canvas.grid(row=row_position, column=col_position, padx=padding, pady=padding)
            canvas.bind("<Button-1>",
                        lambda event, img_path=image_path, count=self.number_img: self.select_image(img_path,
                                                                                                        count))

            self.canvas_list.append((canvas, photo))

    def select_image(self, img_path, count):
        self.selected_image = img_path
        print(f"Imagen seleccionada: {count}")

    def sendGallery(self):
        try:
            if self.selected_image:

                image_path = self.selected_image
                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()
                    image_base64 = base64.b64encode(image_data)
                    self.client.publish("ImagenAnna", payload=image_base64, qos=2)
            else:
                print("No hay foto para enviar")
                return None
        except Exception as e:
            messagebox.showerror("Error de conexión",
                                 "No se pudo enviar la imagen. Por favor, inténtalo de nuevo.\nError: " + str(e),
                                 parent=self.windowGallery)

    def closeGallery(self):
        self.windowGallery.destroy()'''
