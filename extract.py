import os

import cv2 as cv

# Exit if no positive images are given
if not os.path.exists('positive'):
    print('positive images not found')
    exit(1)

# Open file stream to positive.dat
output = open('positive.dat', 'w')
index = 0

# Process all jpgs in positive directory
for file in os.listdir('positive'):
    if not file.endswith('.png'):
        continue

    # Read image from positive directory
    img = cv.imread(f'positive/{file}')

    # Convert to hsv and mask frame
    converted = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    # TODO: Cigarette mask
    mask = cv.inRange(converted, (10, 100, 0), (28, 255, 255))#orange
    #mask = cv.inRange(converted, (85, 140, 0), (140, 255, 255))#blue

    # Find contours on mask
    contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        continue

    # Sort contours by size and get position of the largest contour
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    x, y, width, height = cv.boundingRect(contours[0])

    # Write result to files
    output.write(f'positive/{file}  {index}  {x} {y} {width} {height}\n')
    index += 1

output.close()
