from cv2 import *

# Initialize video capture and image classifier
capture = VideoCapture(0)
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

    converted = cvtColor(frame, COLOR_BGR2RGB)
    mask = inRange(converted, (120, 60, 40), (180, 120, 100))
    filtered = bitwise_and(frame, frame, mask=mask)

    filtered = cvtColor(filtered, COLOR_RGB2GRAY)
    contours, _ = findContours(filtered, RETR_LIST, CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contours = sorted(contours, key=contourArea, reverse=True)
        # drawContours(frame, contours, 0, (255, 0, 0), 3)

        # Draw bounding box
        contour = contours[0]
        approx = approxPolyDP(contour, 0.009 * arcLength(contour, True), True)
        # drawContours(frame, [approx], 0, (255, 0, 0), 3)

    imshow('OpenCV', frame)
    waitKey(50)

capture.release()
print('Exit')
