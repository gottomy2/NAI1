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

    # Morphological Transform, Dilation
    # for each color and bitwise_and operator
    # between imageFrame and mask determines
    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    #For blue color:
    blue_mask = cv.dilate(blue_mask, kernal)
    res_blue = cv.bitwise_and(imageFrame, imageFrame,blue_mask)

        # Creating contour to track blue color
    centers = []
    contours, hierarchy = cv.findContours(blue_mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv.contourArea(contour)
        if area > 500:
            x, y, w, h = cv.boundingRect(contour)
            imageFrame = cv.rectangle(imageFrame, (x, y),(x + w, y + h),(255, 0, 0), 2)
            cv.putText(imageFrame, "Blue", (x, y), cv.FONT_ITALIC, 1.0, (255, 0, 0))

            M = cv.moments(contours[0])
            cy = int(M['m01'] / M['m00'])
            cx = int(M['m10'] / M['m00'])
            centers.append([cx, cy])
            imageFrame = cv.circle(imageFrame, (cx, cy), 7, (255, 255, 255), -1)


            #cv.line(imageFrame,(centers[0][0], centers[0][1]),(x + int(w / 2), y + int(h / 2)), (0, 0, 0), 3,cv.LINE_AA)
            #cv.line(imageFrame, (centers[0][0], centers[0][1]), (cx,cy), (0, 0, 0), 3,cv.LINE_AA)
        if len(centers) == 2:
            cv.line(imageFrame, (cx, cy), (x + int(w / 2), y + int(h / 2)), (0, 0, 0), 3,cv.LINE_AA)
            #cv.line(imageFrame, (centers[0][0], centers[0][1]), (centers[1][0], centers[1][1]), (0, 0, 0), 3,cv.LINE_AA)
    cv.imshow("Multiple Color Detection", imageFrame)

    #Break if 'esc' has been pressed
    if cv.waitKey(33) == 27:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()