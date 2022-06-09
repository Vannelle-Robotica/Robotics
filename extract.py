import math
import os
import cv2 as cv
from cv2 import imshow, waitKey

if not os.path.exists('positive'):
    print('positive images not found')
    exit(1)

# Open file stream to positive.dat
output = open('positive.dat', 'w')
index = 0
factor = 0

# Process all jpgs in positive directory
for file in os.listdir('positive'):
    if not file.endswith('.jpg'):
        continue

    # Read image from positive directory
    img = cv.imread(f'positive/{file}')

    # Convert to hsv and mask frame
    converted = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(converted, (10, 30, 120), (20, 255, 255))  # orange
    # mask = cv.inRange(converted, (85, 140, 0), (140, 255, 255))#blue

    # Find contours on mask
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    __ , width, ___  = img.shape
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

        #rechter wielen moeten harder rijden
        if cX < lowerWidth:
            exit
        #linker wielen moeten harder rijden
        if cX > higherWidth:
            exit
        #beide niet dan rechtdoor rijden

        cv.circle(img, (cX, cY), 1, (0, 0, 0), 2)
        area = cv.contourArea(contour)
        perimeter = cv.arcLength(contour, True)

        # calculates how round a object is
        if area > 5:
            factor = 4 * math.pi * area / perimeter ** 2

        # Draw bounding box
        if factor < 0.4 and factor > 0.1:
            if area > 200 and area < 1000:
                approx = cv.approxPolyDP(contour, 0.009 * cv.arcLength(contour, True), True)
                cv.drawContours(img, [approx], 0, (255, 0, 0), 2)

    # Write result to files
    output.write(f'positive/{file}  {index}\n')
    index += 1

    imshow('Drawed contours', img)
    waitKey(0)

output.close()
