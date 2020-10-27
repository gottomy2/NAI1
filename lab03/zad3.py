import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    _, imageFrame = cap.read()

    # Convert the imageFrame in
    # BGR(RGB color space) to
    # HSV(hue-saturation-value)
    # color space
    hsvFrame = cv.cvtColor(imageFrame, cv.COLOR_BGR2HSV)

    # Set range for red color and define mask
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    red_mask = cv.inRange(hsvFrame, red_lower, red_upper)

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # For red color
    red_mask = cv.dilate(red_mask, kernal)
    res_red = cv.bitwise_and(imageFrame, imageFrame,red_mask);

    # Creating contour to track red color
    contours, hierarchy = cv.findContours(red_mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv.boundingRect(contour)
            imageFrame = cv.rectangle(imageFrame, (x, y),(x + w, y + h),(0, 0, 255), 2)
            cv.putText(imageFrame, "Red Color", (x, y),cv.FONT_HERSHEY_SIMPLEX, 1.0,(0, 0, 255))


    cv.imshow("Multiple Red Color Detection", imageFrame)

    #Break if 'esc' has been pressed
    if cv.waitKey(33) == 27:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()