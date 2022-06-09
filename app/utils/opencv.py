import math
import cv2 as cv

# Initialize video capture and image classifier
capture = cv.VideoCapture(0)
index = 0
factor = 0

while capture.isOpened():
    # Capture image
    ret, frame = capture.read()

    # Escape if capturing image failed
    if not ret:
        print('Failed to capture frame')
        capture.release()
        exit()

    converted = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(converted, (10, 75, 0), (20, 255, 255))
    filtered = cv.bitwise_and(frame, frame, mask=mask)
    filtered = cv.cvtColor(filtered, cv.COLOR_RGB2GRAY)
    contours, _ = cv.findContours(filtered, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    __, width, ___ = capture.shape
    width = width / 2
    lowerWidth = width - 50
    higherWidth = width + 50

    if len(contours) > 0:
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        contour = contours[0]

        # Draws a Centroid in the circle with this fomula
        M = cv.moments(contours[0])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # rechter wielen moeten harder rijden
        if cX < lowerWidth:
            exit
        # linker wielen moeten harder rijden
        if cX > higherWidth:
            exit
        # beide niet dan rechtdoor rijden

        cv.circle(capture, (cX, cY), 1, (0, 0, 0), 2)

        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)

        # calculates how round a object is
        if area > 5:
            factor = 4 * math.pi * area / perimeter ** 2

        # Draw bounding box
        if factor < 0.4 and factor > 0.1:
            if area > 200 and area < 1000:
                approx = cv.approxPolyDP(contour, 0.009 * cv.arcLength(contour, True), True)
                cv.drawContours(frame, [approx], 0, (255, 0, 0), 3)

    cv.imshow('OpenCV', frame)
    if cv.waitKey(50) != -1:
        print('Captured frame')
        cv.imwrite(f'positive/{index}.jpg', frame)
        index += 1

capture.release()
print('Exit')
