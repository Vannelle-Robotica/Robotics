import cv2 as cv

from app.hardware.motors import Motors

BLUE_SQUARE = [(85, 140, 0), (140, 255, 255)]
# Cigarette mask
CIGARETTE = [(10, 100, 0), (28, 255, 255)]

Speed = 60

stop = 0


class Camera:
    def get_object(self, mask, min_size, motors):
        """Finds the largest object with the specified mask in the frame"""
        # Mask all blue and brown objects in image
        converted = cv.cvtColor(self, cv.COLOR_BGR2HSV)

        # Mask image and find contours
        masked = cv.inRange(converted, mask[0], mask[1])
        contours, _ = cv.findContours(masked, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Sort contours by size
        contours = sorted(contours, key=cv.contourArea, reverse=True)

        if len(contours) > 0 and cv.contourArea(contours[0]) > min_size:
            # turn_to_object(frame, contours)
            # Arduino.write(6)
            self.follow_cube(self, contours)
            return contours[0]
        return None

    def get_centroid(self, frame, contours):
        # Get width of screen and take a margin of the middle
        __, width, ___ = self.shape
        width = width / 2
        lowerWidth = width - 50
        higherWidth = width + 50

        M = cv.moments(contours[0])
        cX = int(M["m10"] / M["m00"])

        return lowerWidth, higherWidth, cX

    def turn_to_object(self, frame, contours):
        """this function turns to the founded cigarette and drives to it"""
        (lowerWidth, higherWidth, cX) = self.get_centroid(frame, contours)

        # rechter wielen moeten harder rijden
        if cX < lowerWidth:
            Motors.move("rl", Speed)
            Motors.speed(Speed)

        # linker wielen moeten harder rijden
        if cX > higherWidth:
            Motors.move("rr", Speed)
            Motors.speed(Speed)

        # beide niet dan rechtdoor rijden
        else:
            Motors.move("f", Speed)
            Motors.speed(Speed)
            cv.waitKey(5000)
            Motors.move("s", stop)

    def follow_cube(self, frame, contours):

        (lowerWidth, higherWidth, cX) = self.get_centroid(frame, contours)
        # rechter wielen moeten harder rijden
        if cX < lowerWidth:
            Motors.move("rl", Speed)
            Motors.speed(Speed)
        # linker wielen moeten harder rijden
        if cX > higherWidth:
            Motors.move("rr", Speed)
            Motors.speed(Speed)
        else:
            print('No turn')
