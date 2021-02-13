import cv2
import numpy as np
from datetime import datetime
import time

face_cascade = cv2.CascadeClassifier('/home/pi/Python/Robotics/robotika/resources/face.xml')
smile_cascade = cv2.CascadeClassifier('/home/pi/Python/Robotics/robotika/resources/smile.xml')

fps_list_path = "/home/pi/Python/Robotics/robotika/resources/fps_list.txt"


def videoConvert(capture):
    ret, img_bgr = capture.read()
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    return ret, img_bgr, img_hsv


def getMask(img, min_hue, max_hue,
             min_sat=50, max_sat=255,
             min_val=50, max_val=255):
    lower_bound = np.array([min_hue, min_sat, min_val])
    upper_bound = np.array([max_hue, max_sat, max_val])
    mask = cv2.inRange(img, lower_bound, upper_bound)
    return mask


def getContours(mask, min_area=3000):
    _, thresh = cv2.threshold(mask, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return filter(lambda cnt: cv2.contourArea(cnt) > min_area, contours)


def createEllipse(mask, image):
    mask_circle = getMask(image, 0, 180)
    contours_circle = getContours(mask_circle)
    contours_mask = getContours(mask)
    contourList = list(contours_mask)
    for i in range(len(contourList)):
        contour = contourList[i]
        if cv2.arcLength(contour, True) and cv2.contourArea(contour) > 2000:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            if len(approx) > 7:
                x, y, w, h = cv2.boundingRect(contour)
                if 0.95 < float(w)/float(h) < 1.05:
                    ellipse = cv2.fitEllipse(contour)
                    cv2.ellipse(image, ellipse, (255, 0, 0), 3)
                    cv2.putText(image, str(float(w)/float(h)), tuple(approx[0][0]),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, [255, 255, 0], 2, cv2.LINE_AA)
                    return True
    return False


def getBiggestContour(contours):
    max_cnt = contours[0]
    for cnt in contours:
        cnt_area = cv2.contourArea(cnt)
        if cnt_area > cv2.contourArea(max_cnt):
            max_cnt = cnt
    return max_cnt


def detectSmile(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05,
                                          minNeighbors=5, minSize=(200, 200))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_gray = gray[y:y + h, x:x + w]
        face_color = image[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(face_gray, scaleFactor=1.8,
                                                minNeighbors=20, maxSize=(150, 150))
        for (ex, ey, ew, eh) in smiles:
            cv2.rectangle(face_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            return True;
        return False;

def getTimeStamp():
    return datetime.now().strftime("%H:%M:%S")


def GetImageSize(image):
    x, y, _ = image.shape
    return x * y


def GetImageSize2(image):
    x, y = image.shape
    return x * y