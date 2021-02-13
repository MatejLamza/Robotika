import RPi.GPIO as GPIO
from time import sleep
import time, threading


MotorA_en = 2
MotorA_fw = 3
MotorA_bw = 4

MotorB_en = 17
MotorB_fw = 27
MotorB_bw = 22

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(MotorA_en, GPIO.OUT)
GPIO.setup(MotorA_fw, GPIO.OUT)
GPIO.setup(MotorA_bw, GPIO.OUT)

GPIO.setup(MotorB_en, GPIO.OUT)
GPIO.setup(MotorB_fw, GPIO.OUT)
GPIO.setup(MotorB_bw, GPIO.OUT)

MotorA_PWM = GPIO.PWM(MotorA_en, 1000)
MotorB_PWM = GPIO.PWM(MotorB_en, 1000)

MotorA_PWM.start(0)
MotorB_PWM.start(0)


def startA(speed=100):
    MotorA_PWM.ChangeDutyCycle(speed)


def startB(speed=100):
    MotorB_PWM.ChangeDutyCycle(speed)


def stop():
    MotorA_PWM.ChangeDutyCycle(0)
    MotorB_PWM.ChangeDutyCycle(0)


def rotate():
    GPIO.output(MotorA_fw, GPIO.LOW)
    GPIO.output(MotorA_bw, GPIO.HIGH)

    GPIO.output(MotorB_fw, GPIO.HIGH)
    GPIO.output(MotorB_bw, GPIO.LOW)

    startA()
    startB()


def rotateCircle():
    rotate()
    
    sleep(0.3)
    stop()


def forward():
    GPIO.output(MotorA_fw, GPIO.HIGH)
    GPIO.output(MotorA_bw, GPIO.LOW)

    GPIO.output(MotorB_fw, GPIO.HIGH)
    GPIO.output(MotorB_bw, GPIO.LOW)

    startA()
    startB()



def backward():
    GPIO.output(MotorA_bw, GPIO.HIGH)
    GPIO.output(MotorA_fw, GPIO.LOW)

    GPIO.output(MotorB_bw, GPIO.HIGH)
    GPIO.output(MotorB_fw, GPIO.LOW)

    startA()
    startB()


def rotateLeft():
    GPIO.output(MotorA_fw, GPIO.LOW)
    GPIO.output(MotorA_bw, GPIO.HIGH)

    GPIO.output(MotorB_fw, GPIO.HIGH)
    GPIO.output(MotorB_bw, GPIO.LOW)

    startA()
    startB()


def rotateRight():
    GPIO.output(MotorA_bw, GPIO.LOW)
    GPIO.output(MotorA_fw, GPIO.HIGH)

    GPIO.output(MotorB_bw, GPIO.HIGH)
    GPIO.output(MotorB_fw, GPIO.LOW)


    startA()
    startB()

def rotateRightSlow():
    GPIO.output(MotorA_fw, GPIO.HIGH)
    GPIO.output(MotorA_bw, GPIO.LOW)

    GPIO.output(MotorB_fw, GPIO.LOW)
    GPIO.output(MotorB_bw, GPIO.HIGH)


    startA()
    startB()


def stopForward():
    MotorA_PWM.ChangeDutyCycle(0)
    MotorB_PWM.ChangeDutyCycle(0)
    forward()

def stopForwardBit():
    MotorA_PWM.ChangeDutyCycle(0)
    MotorB_PWM.ChangeDutyCycle(0)
    rotateRight()

def forwardBit():
    forward()
    threading.Timer(3, stopForwardBit).start()


def stopThenForward(duration=1):
    stop()
    threading.Timer(duration, forward).start()

def forwardThenStop(duration):
    forward()
    threading.Timer(duration, stop).start()

def backwardThenStop(duration):
    backward()
    threading.Timer(duration, stop).start()

def rotateOneCircle():
    rotateRight()
    threading.Timer(4, stop).start()

def turnLeftThenForward(duration=1.5):
    rotateLeft()
    threading.Timer(duration, stopForward).start()

def turnRightThenForward(duration=1.5):
    rotateRight()
    threading.Timer(duration, stopForward).start()


