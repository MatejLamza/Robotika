import cv2
from common import helper
from common import motors as mt
import time

greenLow, greenUp = 44, 65
yellowLow, yellowUp = 25, 35
blueLow, blueUp = 75, 130
orangeLow, orangeUp = 5, 25

capture = cv2.VideoCapture(0)

def runProgram():
    while True:
        _, imageBg, iamgeHsv = helper.videoConvert(capture)

        greenCover = contour_covers_view(iamgeHsv, greenLow, greenUp)
        yellowCover = contour_covers_view(iamgeHsv, yellowLow, yellowUp)
        blueCover = contour_covers_view(iamgeHsv, blueLow, blueUp, 0.15)
        orangeCover = contour_covers_view(iamgeHsv, orangeLow, orangeUp, 0.15)

        if greenCover or yellowCover or blueCover or orangeCover:
            process_cover(greenCover, yellowCover, blueCover, orangeCover)

        cv2.imshow('Outcome 3 Task 2', imageBg)

    capture.release()
    cv2.destroyAllWindows()



def contour_covers_view(image, lower, upper, view_percent=0.5):
    mask = helper.getMask(image, lower, upper)
    contours = list(helper.getContours(mask))
    if len(contours) > 0:
        maxCountour = helper.getBiggestContour(contours)
        if cv2.contourArea(maxCountour) > helper.GetImageSize(image) * view_percent:
            return True
        return False


def process_cover(greenCover, yellowCover, blueCover, orangeCover):
    if greenCover:
        print("Looking at green")
        mt.forwardThenStop(3)
    elif yellowCover:
        print("Looking at yellow")
        mt.backwardThenStop(3)
    elif blueCover and orangeCover:
        print("Looking at orange")
        mt.rotateOneCircle()

runProgram()
