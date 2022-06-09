import cv2 as cv
from app.hardware import motors

# Blue square mask
BLUE_SQUARE = [(85, 140, 0), (140, 255, 255)]

# Cigarette mask
CIGARETTE = [(10, 100, 0), (28, 255, 255)]


def get_object(frame, mask, min_size):
    """Finds the largest object with the specified mask in the frame"""
    # Mask all blue and brown objects in image
    converted = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Mask image and find contours
    masked = cv.inRange(converted, mask[0], mask[1])
    contours, _ = cv.findContours(masked, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # Sort contours by size
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    if len(contours) > 0 and cv.contourArea(contours[0]) > min_size:
        #turn_to_object(frame, contours)
        follow_cube(frame, contours)
        return contours[0]
    return None

def turn_to_object(frame, contours):
    __, width, ___ = frame.shape
    width = width / 2
    lowerWidth = width - 50
    higherWidth = width + 50

    M = cv.moments(contours[0])
    cX = int(M["m10"] / M["m00"])

    # rechter wielen moeten harder rijden
    if cX < lowerWidth:
        motors.move(motors,"rl",2)

    # linker wielen moeten harder rijden
    if cX > higherWidth:
        motors.move(motors,"rr",2)

    # beide niet dan rechtdoor rijden
    else:
        motors.move(motors,"f",2)
        cv.waitKey(3000)
        motors.move(motors, "s", 2)


def follow_cube(frame, contours):
    __, width, ___ = frame.shape
    width = width / 2
    lowerWidth = width - 50
    higherWidth = width + 50

    M = cv.moments(contours[0])
    cX = int(M["m10"] / M["m00"])

    # rechter wielen moeten harder rijden
    if cX < lowerWidth:
        motors.move(motors, "rl", 2)

    # linker wielen moeten harder rijden
    if cX > higherWidth:
        motors.move(motors, "rr", 2)


