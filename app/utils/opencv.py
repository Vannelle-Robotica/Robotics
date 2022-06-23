import cv2 as cv

# Blue square
BLUE_SQUARE = [(85, 140, 0), (140, 255, 255)]
# Cigarette mask
CIGARETTE = [(10, 100, 20), (25, 255, 255)]


def get_centroid(contour):
    """Get horizontal center position of contour"""
    M = cv.moments(contour)
    cX = int(M["m10"] / M["m00"])
    return cX


class Camera:

    def __init__(self):
        self.capture = cv.VideoCapture(0)

        ret, frame = self.capture.read()
        if not ret:
            self.writer = None
            return

        height, width, _ = frame.shape
        self.writer = cv.VideoWriter('/home/robotica/Documents/temp.avi', cv.VideoWriter_fourcc(*'DIVX'), 30,
                                     (width, height))

    def __del__(self):
        self.capture.release()

    def get_object(self, mask, min_size, max_size):
        """Finds the largest object with the specified mask in the frame"""
        # Capture frame
        ret, frame = self.capture.read()
        if ret is False:
            return None, 0, 0

        # Mask all blue and brown objects in image
        converted = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Mask image and find contours
        masked = cv.inRange(converted, mask[0], mask[1])
        contours, _ = cv.findContours(masked, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

        # Sort contours by size
        contours = sorted(contours, key=cv.contourArea, reverse=True)

        # Check if object is above minimum size
        if len(contours) > 0:
            for i in range(len(contours)):
                # Get contour size
                area = cv.contourArea(contours[i])

                # Break out of function if we reached smaller objects
                if area < min_size:
                    break

                # Return contour if it matches our bounds
                if area < max_size:
                    if self.writer is not None:
                        cv.drawContours(frame, contours, i, (255, 255, 255))
                        self.writer.write(frame)

                    _, width, _ = frame.shape
                    return contours[0], width, area
        return None, 0, 0
