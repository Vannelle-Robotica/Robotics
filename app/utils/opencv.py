import cv2 as cv

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
        return contours[0]
    return None
