import cv2 as cv

# Initialize video capture and image classifier
capture = cv.VideoCapture(0)
index = 0
# classifier = CascadeClassifier('cascades/haarcascade_frontalface_alt.xml')

while capture.isOpened():
    # Capture image
    ret, frame = capture.read()

    # Escape if capturing image failed
    if not ret:
        print('Failed to capture frame')
        capture.release()
        exit()

    # Greyscale image and detect objects
    # greyscale = cvtColor(frame, COLOR_RGB2GRAY)
    # detected = classifier.detectMultiScale(greyscale)
    # lines = Canny(frame, threshold1=50, threshold2=150)

    # Draw rectangles around detected components
    # for (x, y, width, height) in detected:
    #     rectangle(frame, (x, y), (x + width, y + height), (255, 255, 255), 3)
    #     putText(frame, 'Mens', (int(x + width / 4), y - 20), FONT_ITALIC, 4, (0, 0, 255), 1)

    converted = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    mask = cv.inRange(converted, (227,171,120), (122,77,42))
    filtered = cv.bitwise_and(frame, frame, mask=mask)

    filtered = cv.cvtColor(filtered, cv.COLOR_RGB2GRAY)
    contours, _ = cv.findContours(filtered, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contours = sorted(contours, key=cv.contourArea, reverse=True)
        # drawContours(frame, contours, 0, (255, 0, 0), 3)

        # Draw bounding box
        contour = contours[0]
        approx = cv.approxPolyDP(contour, 0.009 * cv.arcLength(contour, True), True)
        # drawContours(frame, [approx], 0, (255, 0, 0), 3)

    cv.imshow('OpenCV', frame)
    if cv.waitKey(50) != -1:
        print('Captured frame')
        cv.imwrite(f'positive/{index}.jpg', frame)
        index += 1

capture.release()
print('Exit')
