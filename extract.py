from cv2 import *

capture = VideoCapture(0)

while capture.isOpened():
    # Capture image
    ret, frame = capture.read()

    # Escape if capturing image failed
    if not ret:
        print('Failed to capture frame')
        capture.release()
        exit()

    # Convert to hsv and mask frame
    converted = cvtColor(frame, COLOR_BGR2HSV)
    # mask = inRange(converted, (25, 200, 160), (35, 220, 180))
    mask = inRange(converted, (85, 140, 0), (140, 255, 255))
    filtered = bitwise_and(frame, frame, mask=mask)

    # Find contours on mask
    contours, _ = findContours(mask, RETR_LIST, CHAIN_APPROX_SIMPLE)

    # Check if a box was found
    if len(contours) == 0:
        imshow('Masked image', frame)
        waitKey(1)
        continue

    # Draw contours of box
    contours = sorted(contours, key=contourArea, reverse=True)
    area = contourArea(contours[0])

    # Check if area is greater than 0
    if area == 0:
        continue

    # Get position of box contours and draw text
    # drawContours(frame, contours, 0, (255, 255, 255), 3)
    x, y, width, height = boundingRect(contours[0])
    # distance = (18 / area) * 100

    putText(filtered, 'Box', (x + int(width / 4), y - 5), FONT_ITALIC, 0.5, (255, 255, 255), 3)
    imshow('Masked image', frame[y:y + height if height > 100 else y + 100, x:x + width if width > 100 else x + 100])
    waitKey(1)
