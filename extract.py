import os

from cv2 import *

# Exit if no positive images are given
if not os.path.exists('positive'):
    print('Positive images not found')
    exit(-1)

# Open file stream to info.dat
info = open('info.dat', 'w')
index = 0

# Process all jpgs in positive directory
# TODO: Fix loop occasionally duplicating & replacing images
for file in os.listdir('positive'):
    if not file.endswith('.jpg'):
        continue

    # Read image from file
    img = imread(f'positive/{file}')
    os.remove(f'positive/{file}')

    # Convert to hsv and mask frame
    converted = cvtColor(img, COLOR_BGR2HSV)
    # TODO: Cigarette mask
    # mask = inRange(converted, (25, 200, 160), (35, 220, 180))
    mask = inRange(converted, (85, 140, 0), (140, 255, 255))

    # Find contours on mask
    contours, _ = findContours(mask, RETR_LIST, CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        continue

    # Filter contours, get position of largest contour and delete existing image
    contours = sorted(contours, key=contourArea, reverse=True)
    x, y, width, height = boundingRect(contours[0])

    # Write result to files
    info.write(f'positive/{index}.jpg  {index}  {x} {y} {width} {height}\n')
    imwrite(f'positive/{index}.jpg', img)
    index += 1
