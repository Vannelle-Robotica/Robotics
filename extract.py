import os

from cv2 import *

# Exit if no positive images are given
if not os.path.exists('positive'):
    print('Positive images not found')
    exit(-1)

# Open file stream to positive.dat
output = open('positive.dat', 'w')
index = 0

# Process all jpgs in positive directory
for file in os.listdir('positive'):
    if not file.endswith('.jpg'):
        continue

    # Read image from positive directory
    img = imread(f'positive/{file}')

    # Convert to hsv and mask frame
    converted = cvtColor(img, COLOR_BGR2HSV)
    # TODO: Cigarette mask
    # mask = inRange(converted, (25, 200, 160), (35, 220, 180))
    mask = inRange(converted, (85, 140, 0), (140, 255, 255))

    # Find contours on mask
    contours, _ = findContours(mask, RETR_LIST, CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        continue

    # Sort contours by size and get position of the largest contour
    contours = sorted(contours, key=contourArea, reverse=True)
    x, y, width, height = boundingRect(contours[0])

    # Write result to files
    output.write(f'positive/{file}  {index}  {x} {y} {width} {height}\n')
    index += 1

    # Draw contours and show image
    drawContours(img, contours, 0, (255, 255, 255), 3)
    imshow('Extracted', img)
    waitKey(-1)

output.close()
