
import time
from datetime import datetime
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import Scale, Button


class slider:
    def agregar_borde_rojo_con_slider(imagen_path, grosor_inicial=5):
        global img
        global grosor_borde_superior, grosor_borde_inferior, grosor_borde_izquierdo, grosor_borde_derecho
        global grosor_top_slider, grosor_bottom_slider, grosor_left_slider, grosor_right_slider

        def agregar_marco_rojo(img):
            global grosor_borde_superior, grosor_borde_inferior, grosor_borde_izquierdo, grosor_borde_derecho

            # Obtiene las dimensiones de la imagen
            alto, ancho = img.shape[:2]

            # Define el color rojo en formato BGR (azul, verde, rojo)
            color_rojo = (0, 0, 255)
            top= grosor_borde_superior
            botton= grosor_borde_inferior
            left = grosor_borde_izquierdo
            right = grosor_borde_derecho

            for j in range(top):
                for i in range(ancho):
                    img[j, i] = color_rojo
            for j in range(alto - botton, alto):
                for i in range(ancho):
                    img[j, i] = color_rojo
            for j in range(alto):
                for i in range(left):
                    img[j, i] = color_rojo
            for j in range(alto):
                for i in range(ancho - right, ancho):
                    img[j, i] = color_rojo
            # Naming a window
            return img

        def actualizar_borde_superior(valor):
            global img
            global grosor_borde_superior

            grosor_borde_superior = int (valor)
            img = agregar_marco_rojo(img)
            cv2.imshow("Resized_Window", img)

        def actualizar_borde_inferior(valor):
            global img
            global grosor_borde_inferior


            grosor_borde_inferior = int(valor)
            img = agregar_marco_rojo(img)
            cv2.imshow("Resized_Window", img)

        def actualizar_borde_izquierdo(valor):
            global img
            global grosor_borde_izquierdo


            grosor_borde_izquierdo= int(valor)
            img = agregar_marco_rojo(img)
            cv2.imshow("Resized_Window", img)

        def actualizar_borde_derecho(valor):
            global img
            global grosor_borde_derecho


            grosor_borde_derecho= int(valor)
            img = agregar_marco_rojo(img)
            cv2.imshow("Resized_Window", img)


        def cortar ():
            global grosor_borde_superior, grosor_borde_inferior, grosor_borde_izquierdo, grosor_borde_derecho
            global img, crop_img

            marco = 50
            alto, ancho = img.shape[:2]

            a = grosor_borde_superior - marco
            b = alto - grosor_borde_inferior + marco
            c = grosor_borde_izquierdo -marco
            d = ancho - grosor_borde_derecho + marco


            crop_img = img[a:b, c:d]
            font = cv2.FONT_HERSHEY_SIMPLEX

            fecha_actual = datetime.now()
            formato_espanol = "%d/%m/%Y"
            fecha_formateada = fecha_actual.strftime(formato_espanol)
            frase = 'Gracias por su visita al campus de la UPC en Castelldefels ('+ fecha_formateada+')'
            textSize = cv2.getTextSize( frase, fontFace=font, fontScale=1, thickness=2)
            pos = (d - textSize [0][0])//2
            cv2.putText(crop_img, frase, (pos, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


            cv2.namedWindow("cropped", cv2.WINDOW_NORMAL)

            # Using resizeWindow()
            cv2.resizeWindow("cropped", d // 4, b// 4)
            cv2.imshow("cropped", crop_img)

        def descargar ():
            global crop_img
            cv2.imwrite('assets/telloPanoramic/res.jpg',  crop_img)

        def reiniciar ():
            global grosor_borde_superior, grosor_borde_inferior, grosor_borde_izquierdo, grosor_borde_derecho
            global img
            global  grosor_top_slider,grosor_bottom_slider,grosor_left_slider,grosor_right_slider

            img = cv2.imread(imagen_path)

            grosor_borde_superior = 50
            grosor_borde_inferior = 50
            grosor_borde_izquierdo = 50
            grosor_borde_derecho = 50
            grosor_top_slider.set(50)
            grosor_bottom_slider.set(50)
            grosor_left_slider.set(50)
            grosor_right_slider.set(50)

            img = agregar_marco_rojo(img)
            cv2.imshow("Resized_Window", img)

        ventana = tk.Tk()
        ventana.title("Agregar Borde Rojo")

        etiqueta_imagen = tk.Label(ventana)
        etiqueta_imagen.pack(padx=10, pady=10)

        grosor_top_slider = Scale(ventana, from_=50, to=500, orient=tk.HORIZONTAL, label="Borde superior", length=300, command=actualizar_borde_superior)
        grosor_top_slider.set(50)
        grosor_top_slider.pack(padx=10, pady=10)

        grosor_bottom_slider = Scale(ventana, from_=50, to=500, orient=tk.HORIZONTAL, label="Borde inferior", length=300,
                              command=actualizar_borde_inferior)
        grosor_bottom_slider.set(50)
        grosor_bottom_slider.pack(padx=10, pady=10)

        grosor_left_slider = Scale(ventana, from_=50, to=500, orient=tk.HORIZONTAL, label="Borde izquierdo", length=300,
                              command=actualizar_borde_izquierdo)
        grosor_left_slider.set(50)
        grosor_left_slider.pack(padx=10, pady=10)

        grosor_right_slider = Scale(ventana, from_=50, to=500, orient=tk.HORIZONTAL, label="Borde derecho", length=300,
                              command=actualizar_borde_derecho)
        grosor_right_slider.set(50)
        grosor_right_slider.pack(padx=10, pady=10)

        B = Button(ventana, text="Cortar", command=cortar)
        B.pack(padx=10, pady=10)
        C = Button(ventana, text="Descargar", command=descargar)
        C.pack(padx=10, pady=10)

        C = Button(ventana, text="Reiniciar", command=reiniciar)
        C.pack(padx=10, pady=10)

        #img = cv2.imread(imagen_path)
        img = cv2.imread('assets/telloPanoramic/result.jpg')

        grosor_borde_superior = 50
        grosor_borde_inferior = 50
        grosor_borde_izquierdo = 50
        grosor_borde_derecho = 50

        img = agregar_marco_rojo(img)
        alto, ancho = img.shape[:2]
        cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

        # Using resizeWindow()
        cv2.resizeWindow("Resized_Window", ancho//4, alto//4)

        # Displaying the image
        cv2.imshow("Resized_Window", img)




        ventana.mainloop()

