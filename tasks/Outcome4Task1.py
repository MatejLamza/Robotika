import cv2
from common import helper 
from helpers import motors as mt
from time import sleep

capture = cv2.VideoCapture(0)

def runProgram():
    
    while True:
        _, image = capture.read()

        if helper.detectSmile(image):
            print("Smile detected")
            mt.rotateOneCircle()

        cv2.imshow('Outcome 4 Task 1', image)
    
    capture.release()
    cv2.destroyAllWindows()

runProgram()
