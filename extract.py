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

    for cnr in range(len(contours)):
        cnt = contours[cnr]
        area = cv.contourArea(cnt)
        perimeter = cv.arcLength(cnt, True)

        # calculates how round a object is
        if area > 5:
            factor = 4 * math.pi * area / perimeter ** 2

        if factor < 0.4:
            if area > 400 and area < 1100:
                cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)  # green

    if len(contours) == 0:
        continue

    # Write result to files
    output.write(f'positive/{file}  {index}\n')
    index += 1

    imshow('Drawed contours', img)
    waitKey(0)

output.close()
