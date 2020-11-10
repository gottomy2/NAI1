import cv2 as cv
import numpy as np
import mapper

cap = cv.VideoCapture('vid3.mp4')
if not cap.isOpened():
    print("Cannot open video")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    ratio = frame.shape[0] / 500.0
    frame = cv.rotate(frame,0,cv.ROTATE_90_CLOCKWISE);
    frame = cv.resize(frame, (300, 500))
    #flipped = cv.flip(frame, 1)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray,(5,5),0)
    edged = cv.Canny(gray,75,200)

    cv.imshow("Normal", frame)
    cv.imshow("Edged", edged)

    contours, hierarchy = cv.findContours(edged,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    scr = None

    for contour in contours:
        area = cv.contourArea(contour)

        if area > 800:
            peri = cv.arcLength(contour, True)
            approx = cv.approxPolyDP(contour, 0.02 * peri, True)

            if len(approx) == 4:
                scr = approx
                x, y, w, h = cv.boundingRect(contour)
                break
            else:
                continue

    if scr is not None:
        cv.drawContours(frame, [scr], -1, (0, 255, 0), 3)



    hsvFrame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)
    blue_mask = cv.inRange(hsvFrame, blue_lower, blue_upper)

    kernal = np.ones((5, 5), "uint8")

    # For blue color:
    blue_mask = cv.dilate(blue_mask, kernal)
    res_blue = cv.bitwise_and(frame, frame, blue_mask)

    contours, hierarchy = cv.findContours(blue_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    first = 0
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 300:
            if area > first:
                first = area
                contour1 = contour
            x, y, w, h = cv.boundingRect(contour1)
            imageFrame = cv.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
            cv.putText(imageFrame, "Blue", (x, y), cv.FONT_ITALIC, 1.0, (255, 0, 0))
    cv.imshow('Contours', frame)
    print("Number of Contours found = " + str(len(contours)))
    # a = None
    #
    # for contour in contours:
    #     area = cv.contourArea(contour)
    #     if area > 300:
    #         p = cv.arcLength(contour, True)
    #         a = cv.approxPolyDP(contour, 0.02 * p, True)
    #
    # if a is not None:
    #     cv.drawContours(frame, [a], -1, (0, 255, 0), 3)

    #Break if 'esc' has been pressed
    if cv.waitKey(33) == 27:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()