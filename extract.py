import math
import os
import cv2 as cv

# Exit if no positive images are given
from cv2 import drawContours, imshow, waitKey

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
    # TODO: Cigarette mask
    mask = cv.inRange(converted, (10, 30, 120), (20, 255, 255))#orange
    #mask = cv.inRange(converted, (85, 140, 0), (140, 255, 255))#blue

    # Find contours on mask
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnr in range(len(contours)):
        cnt = contours[cnr]
        area = cv.contourArea(cnt)
        perimeter = cv.arcLength(cnt, True)


        # calculates how round a object is
        if area > 5:
            factor = 4 * math.pi * area / perimeter ** 2


        if factor > 0.4:
            exit  # cv.drawContours(img, [cnt], -1, (0, 255, 255), 3)  # yellow
        else:
            # print(area)

            if area > 600 and area < 1100:
                cv.drawContours(img, [cnt], -1, (0, 255, 0), 3)  # green


    if len(contours) == 0:
        continue

    # Sort contours by size and get position of the largest contour
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    x, y, width, height = cv.boundingRect(contours[0])


    # Write result to files
    output.write(f'positive/{file}  {index}  {x} {y} {width} {height}\n')
    index += 1



    imshow('Extracted', img)
    waitKey(-1)

output.close()
