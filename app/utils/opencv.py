import cv2 as cv
from app.utils.VideoCapture import VideoCaptureThreading



BLUE_SQUARE = [(85, 140, 0), (140, 255, 255)]
# Cigarette mask
CIGARETTE = [(10, 100, 0), (28, 255, 255)]

Speed = 60

stop = 0

class Camera:
    def get_object(self, frame, mask, min_size, motors, arduino):
        """Finds the largest object with the specified mask in the frame"""
        # Mask all blue and brown objects in image
        converted = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Mask image and find contours
        masked = cv.inRange(converted, (85, 140, 0), (140, 255, 255))
        contours, _ = cv.findContours(masked, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Sort contours by size
        contours = sorted(contours, key=cv.contourArea, reverse=True)

        if len(contours) > 0 and cv.contourArea(contours[0]) > min_size:
            # turn_to_object(frame, contours, motors)
            # Arduino.write(6)
            self.follow_cube(frame, contours, motors, arduino)
            return contours[0]
        return None

    def get_centroid(self, frame, contours):
        # Get width of screen and take a margin of the middle
        height, width, ___ = frame.shape
        width = width / 2
        lowerWidth = width - 50
        higherWidth = width + 50
        print(width)
        M = cv.moments(contours[0])
        cX = int(M["m10"] / M["m00"])

        return lowerWidth, higherWidth, cX

    def turn_to_object(self, frame, contours, motors):
        """this function turns to the founded cigarette and drives to it"""
        (lowerWidth, higherWidth, cX) = self.get_centroid(frame, contours)

        # rechter wielen moeten harder rijden
        if cX < lowerWidth:
            motors.move("rl", Speed)
            motors.speed(Speed)

        # linker wielen moeten harder rijden
        if cX > higherWidth:
            motors.move("rr", Speed)
            motors.speed(Speed)

        # beide niet dan rechtdoor rijden
        else:
            motors.move("f", Speed)
            motors.speed(Speed)
            cv.waitKey(5000)
            motors.move("s", stop)

    def follow_cube(self, frame, contours, motors, arduino):
        (lowerWidth, higherWidth, cX) = self.get_centroid(frame, contours)
        # rechter wielen moeten harder rijden/ wielen klappen uit
        if cX < lowerWidth:
            # motors.move("rl", speed)
            # motors.speed(Speed)
            arduino.toggle_wheels()
        # linker wielen moeten harder rijden/wielen klappen in
        if cX > higherWidth:
            # motors.move("rr", Speed)
            # motors.speed(Speed)
            arduino.toggle_wheels()
        else:
            print('No turn')
