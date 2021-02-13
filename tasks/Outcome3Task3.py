import cv2
from common import helper 
from common import motors as mt
import time

redLow1, redUp1 = 0, 15
redLow2, redUp2 = 160, 180
yellowLow, yellowUp = 16, 30
greenLow, greenUp = 45, 75


capture = cv2.VideoCapture(0)

def runProgram():
    while True:
        # Input source
        capture = cv2.VideoCapture(0)

        ret, img_bgr, img_hsv = helper.videoConvert(capture)
        if not ret:
            break

        ellipse_red, ellipse_yellow, ellipse_green = get_ellipses(img_hsv, img_bgr)

        if ellipse_red or ellipse_yellow or ellipse_green:
            process_ellipses(ellipse_red, ellipse_yellow, ellipse_green)

        cv2.imshow('Traffic light detection', img_bgr)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break
        
        capture.release()
    cv2.destroyAllWindows()


def fetchTrafficLightColours(imgHsv, ImageBg):
    redMask1 = helper.getMask(imgHsv, redLow1, redUp1, min_sat=110, min_val=60)
    redMask2 = helper.getMask(imgHsv, redLow2, redUp2, min_sat=110, min_val=60)
    redMask = redMask1 | redMask2

    redLight = helper.createEllipse(redMask, ImageBg)

    yellowMask = helper.getMask(imgHsv, yellowLow, yellowUp, min_sat=110, min_val=60)
    yellowLight = helper.createEllipse(yellowMask, ImageBg)

    greenMask = helper.getMask(imgHsv, greenLow, greenUp)
    greenLight = helper.createEllipse(greenMask, ImageBg)

    return redLight, yellowLight, greenLight


def processTrafficLight(redLight, yellowLight, greenLight):
    if redLight and not yellowLight and not greenLight:
        mt.stop()
    elif redLight and yellowLight and not greenLight:
        mt.stopThenForward()
        time.sleep(2)
    elif not redLight and yellowLight and not greenLight:
        mt.stop()
    elif not redLight and not yellowLight and greenLight:
        mt.forwardThenStop(5)
        time.sleep(2)
    else:
        time.sleep(1.5)


runProgram()