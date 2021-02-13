import cv2
from common import helper
from common import motors as mts
import time

green_lower, green_upper = 44, 65
capture = cv2.VideoCapture(0)

def runProgram():
    mts.rotateRight()

    while True:
        _, imageBg, imgHsv = helper.videoConvert(capture)
       
        greenMask = helper.get_mask(imgHsv, green_lower, green_upper)
        contours = list(helper.getContours(greenMask))

        if len(contours) > 0:
            countoureArea = helper.getBiggestContour(contours)
            if cv2.contourArea(countoureArea) > helper.GetImageSize(imageBg) / 2:
                print("Captured green object")
                mts.forwardBit()

        cv2.imshow('Outcome 3 Task 1', imageBg)

    capture.release()
    cv2.destroyAllWindows()

# Function calls
runProgram()
