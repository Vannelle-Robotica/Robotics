import cv2 as cv
# from utils.VideoCapture import VideoCaptureThreading

BLUE_SQUARE = [(85, 140, 0), (140, 255, 255)]
# Cigarette mask
CIGARETTE = [(10, 100, 0), (28, 255, 255)]


def get_centroid(contour):
    """Get horizontal center position of contour"""
    M = cv.moments(contour)
    cX = int(M["m10"] / M["m00"])
    return cX


class Camera:

    def __init__(self):
        self.capture = cv.VideoCapture(0)

    def __del__(self):
        self.capture.release()

    def get_object(self, mask, min_size):
        """Finds the largest object with the specified mask in the frame"""
        # Capture frame
        ret, frame = self.capture.read()
        if ret is False:
            return None, 0

        # Mask all blue and brown objects in image
        converted = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Mask image and find contours
        masked = cv.inRange(converted, mask[0], mask[1])
        contours, _ = cv.findContours(masked, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Sort contours by size
        contours = sorted(contours, key=cv.contourArea, reverse=True)

        # Check if object is above minimum size
        if len(contours) > 0 and cv.contourArea(contours[0]) > min_size:
            height, width, _ = frame.shape
            print(f'Size: {cv.contourArea(contours[0])}')
            return contours[0], width
        return None, 0
