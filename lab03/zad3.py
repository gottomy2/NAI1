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
    hsvFrame = cv.cvtColor(imageFrame, cv.COLOR_BGR2HSV)

    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv.inRange(hsvFrame, blue_lower, blue_upper)

    kernal = np.ones((5, 5), "uint8")

    # For blue color:
    blue_mask = cv.dilate(blue_mask, kernal)
    res_blue = cv.bitwise_and(imageFrame, imageFrame, blue_mask)

    first = 0
    second = 0
    contour1 = None
    contour2 = None
        # Creating contour to track red color
    contours, hierarchy = cv.findContours(blue_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if area > 1000:
            if area > first:
                first = area
                contour1 = contour

            elif first > area > second:
                second = area
                contour2 = contour

        x, y, w, h = cv.boundingRect(contour1)
        imageFrame = cv.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        cv.putText(imageFrame, "Blue", (x, y), cv.FONT_ITALIC, 1.0, (255, 0, 0))
        cx = x + int(w / 2)
        cy = y + int(h / 2)

        x2, y2, w2, h2 = cv.boundingRect(contour2)
        imageFrame1 = cv.rectangle(frame, (x2, y2), ((x2 + w2), (y2 + h2)), (255, 0, 0), 2)
        cv.putText(imageFrame, "Blue", (x, y), cv.FONT_ITALIC, 1.0, (255, 0, 0))
        cx2 = x2 + int(w2 / 2)
        cy2 = y2 + int(h2 / 2)
        #if x<v+e && x>v-e
        # if y == y2 or y + h == y + h2:
        if (y <= y2 < y + 60) or (y + h == y2 + h2):
            cv.line(imageFrame, (cx,cy), (cx2,cy2), (0, 0, 0),3,2)
    cv.imshow("Multiple Color Detection", imageFrame)

    #Break if 'esc' has been pressed
    if cv.waitKey(33) == 27:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()