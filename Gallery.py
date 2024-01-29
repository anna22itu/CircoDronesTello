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


class GalleryMedia():

    def Open(self, master, typeImage):
        self.drone = Tello()

        myFont3 = font.Font(family='Arial', size=10, weight='bold')

        self.windowGallery = Toplevel(master)
        self.selected_image = None
        self.v_media = []
        self.canvas_list = []
        self.number_img = 0
        self.typeImage = typeImage

        # MQTT conexión
        # MQTT conexión
        self.global_broker_address = "broker.hivemq.com"
        self.global_broker_port = 8000  # 8883

        self.client = mqtt.Client("VideoService", transport="websockets")
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

        if self.typeImage == 'Image':
            self.url_images = "assets/telloImages/"
            self.create_vector(self.url_images)

            if len(self.v_media) < 0:
                messagebox.showerror("Error", "No has guardado ninguna foto")
            else:
                self.create_gallery()

        if self.typeImage == 'Video':
            self.url_video = "assets/telloVideo/"
            self.create_vector(self.url_video)

            if len(self.v_media) < 0:
                messagebox.showerror("Error", "No hay guardado ningún vídeo")
            else:
                self.create_gallery()

    def create_vector(self, folder_path):

        for file_name in os.listdir(folder_path):
            if self.typeImage == 'Image':
                if file_name.lower().endswith('.jpg'):
                    file_path = os.path.join(folder_path, file_name)
                    self.v_media.append(file_path)
            if self.typeImage == 'Video':
                if file_name.lower().endswith('.mp4'):
                    file_path = os.path.join(folder_path, file_name)
                    self.v_media.append(file_path)

    def create_gallery(self):
        num_images_per_row = 6  # Número deseado de imágenes por fila
        max_image_size = 300  # Tamaño máximo de las imágenes
        min_image_size = 200  # Tamaño mínimo de las imágenes
        starting_row = 0
        padding = 20

        total_media = len(self.v_media)

        for i, media_path in enumerate(self.v_media):

            if total_media <= num_images_per_row:
                num_images_per_row = 4
                image_size = max_image_size
            else:
                image_size = min_image_size


            if self.typeImage == 'Image':
                img = Image.open(media_path)
                img.thumbnail((image_size, image_size))
                photo = ImageTk.PhotoImage(img)
            if self.typeImage == 'Video':
                cap = cv2.VideoCapture(media_path)
                ret, frame = cap.read()
                thumbnail = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                thumbnail.thumbnail((image_size, image_size))
                photo = ImageTk.PhotoImage(thumbnail)


            canvas = tk.Canvas(self.windowGallery, width=image_size, height=image_size)
            canvas.create_image(0, 0, anchor="nw", image=photo)

            row_position = starting_row + i // num_images_per_row
            col_position = i % num_images_per_row

            self.number_img += 1

            canvas.grid(row=row_position, column=col_position, padx=padding, pady=padding)
            canvas.bind("<Button-1>",
                        lambda event, img_path=media_path, count=self.number_img: self.select_image(img_path,
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

                    if self.typeImage == 'Image':
                        self.client.publish("ImagenAnna", payload=image_base64, qos=2)
                    if self.typeImage == 'Video':
                        self.client.publish("FileAnna", payload=image_base64, qos=2)
            else:
                print("No hay foto para enviar")
                return None
        except Exception as e:
            messagebox.showerror("Error de conexión",
                                 "No se pudo enviar la imagen. Por favor, inténtalo de nuevo.\nError: " + str(e),
                                 parent=self.windowGallery)

    def closeGallery(self):
        self.windowGallery.destroy()