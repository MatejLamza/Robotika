import cv2
import numpy as np
from common import helper
from common import motors as mt
from PIL import Image

# Input source
cap = cv2.VideoCapture(0)

def runProgram():
    print("Detecting paper")
    mt.forward()
    while True:
        ret, image = cap.read()
        paper = image
        ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY), 170, 255, cv2.THRESH_BINARY)
        image, contours = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        listCountours = list(contours)
        if len(listCountours) > 0:
            max_cnt = helper.getBiggestContour(listCountours)
            if helper.GetImageSize2(image) / 2.75 < cv2.contourArea(max_cnt) < helper.GetImageSize2(image) / 1.5:
                _, _, angle = cv2.fitEllipse(max_cnt)
                if 80 < angle < 100:
                    rect = cv2.minAreaRect(max_cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    print(angle)
                    mt.stop()
                    cv2.drawContours(paper, [box], 0, (0, 255, 0), 1)

        cv2.imshow('frame', paper)
        show_contours = []
        if(cv2.waitKey(1) & 0xFF) == ord('q'):
            break;

    capture.release()
    cv2.destroyAllWindows()

runProgram()
