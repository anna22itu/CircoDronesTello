import cv2

import paho.mqtt.client as mqtt

import cv2 as cv2
import numpy as np
import base64

class VideoStreamer:

    def on_messageStreamer(self, cli, userdata, message):
        command = message.topic
        if command == 'videoFrameAnna':
            image = base64.b64decode(bytes(message.payload.decode("utf-8"), "utf-8"))
            npimg = np.frombuffer(image, dtype=np.uint8)
            frame = cv2.imdecode(npimg, 1)
            img = cv2.resize(frame, (450, 600))
            self.current_img = cv2.flip(img, 1)


    def __init__(self, camera):
        self.img = None
        self.current_img = None
        self.source = camera
        self.client = None

        self.global_broker_address = "classpip.upc.edu"
        self.global_broker_port = 8000  # 8883

        if self.source == 1:
            # Cámara del móvil
            self.client = mqtt.Client("VideoService", transport="websockets")
            self.client.username_pw_set("dronsEETAC", "mimara1456.")

            self.client.on_message = self.on_messageStreamer  # Callback function executed when a message is received
            self.client.connect(self.global_broker_address, self.global_broker_port)
            self.client.subscribe('videoFrameAnna')
            print('Waiting connection ...')
            self.client.loop_start()

        if self.source == 2:
            # Cámara del ordenador
            self.cap = cv2.VideoCapture(0)

    def getFrame (self):
        if self.source == 1:
            # Cámara del móvil
            if self.current_img is None:
                return False, self.current_img
            return True, self.current_img
        if self.source == 2:
            # Cámara del ordenador
            success, res = self.cap.read()
            img = cv2.resize(res, (800, 600))
            image = cv2.flip(img, 1)
            return success, image

    def disconnect(self):
        if self.source == 1:
            # Cámara del móvil
            self.client.disconnect()
            self.client.loop_stop()
        elif self.source == 2:
            # Cámara del ordenador
            self.cap.release()

    '''def connect(self):
        if self.source == 1:
            # Cámara del móvil
            self.client.connect(self.global_broker_address, self.global_broker_port)
            self.client.subscribe('videoFrameAnna')
            self.client.loop_start()'''
