import cv2 as cv

from ColorDetector import ColorDetector

detector = ColorDetector()
cam = cv.VideoCapture(0)

while True:
    ret, frame = cam.read()

    a,b,c = detector.DetectColor(frame)
    cv.imshow("test", a)

    k = cv.waitKey(1)