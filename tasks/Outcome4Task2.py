import cv2
from common import helper 
from helpers import motors as mt
import time
import numpy as np

blue_lower, blue_upper = 100, 135
lowerb = np.array([100, 50, 20])
upperb = np.array([135, 255, 255])

center_treshold = 6

capture = cv2.Videocaptureture(0)

def runProgram():
    mt.rotateRightSlow()

    while True:

        _, image, imgHsv = helper.videoConvert(capture)

        img2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img2, lowerb, upperb)
        img_onlyball_hsv = cv2.bitwise_and(img2, img2, mask=mask)
        img_onlyball = cv2.cvtColor(img_onlyball_hsv, cv2.COLOR_HSV2BGR)

        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        imgx, imgy, _ = img_onlyball.shape
        cv2.circle(img_onlyball, (int(imgy / 2), int(imgx / 2)), 3, (0, 127, 0), -1)
        countoursList = list(contours)
        for i in range(len(countoursList)):
            contour = countoursList[i]
            if cv2.contourArea(contour) > 300:
                epsilon = 0.1 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.drawContours(img_onlyball, countoursList, i, (0, 255, 0), 1)
                    M = cv2.moments(contour)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv2.circle(img_onlyball, (cx, cy), 3, (255, 127, 255), -1)
                    cv2.putText(img_onlyball, str(len(approx)), tuple(approx[0][0]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, [255, 255, 0], 2, cv2.LINE_AA)

                    half = int(imgy / 2)
                    if half-half*center_treshold*0.01 < cx < half+half*center_treshold*0.01:
                        cv2.rectangle(img_onlyball, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        print("found")
                        mt.forwardBit()

        if(cv2.waitKey(1) & 0xFF) == ord('q'):
            break;

    capture.release()
    cv2.destroyAllWindows()


runProgram()
