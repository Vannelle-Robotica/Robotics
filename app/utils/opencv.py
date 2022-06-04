import math

import cv2 as cv

# Initialize video capture and image classifier
capture = cv.VideoCapture(0)
index = 0


while capture.isOpened():
    # Capture image
    ret, frame = capture.read()

    # Escape if capturing image failed
    if not ret:
        print('Failed to capture frame')
        capture.release()
        exit()

    converted = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    mask = cv.inRange(converted, (10, 75, 0), (20, 255, 255))
    filtered = cv.bitwise_and(frame, frame, mask=mask)

    filtered = cv.cvtColor(filtered, cv.COLOR_RGB2GRAY)
    contours, _ = cv.findContours(filtered, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)


    if len(contours) > 0:
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        #cv.drawContours(frame, contours, 0, (255, 0, 0), 3)

        # Draw bounding box
        contour = contours[0]
        approx = cv.approxPolyDP(contour, 0.009 * cv.arcLength(contour, True), True)
        cv.drawContours(frame, [approx], 0, (255, 0, 0), 3)

    cv.imshow('OpenCV', frame)
    if cv.waitKey(50) != -1:
        print('Captured frame')
        cv.imwrite(f'positive/{index}.jpg', frame)
        index += 1

capture.release()
print('Exit')
