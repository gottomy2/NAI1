import cv2 as cv
import sys

cap = cv.VideoCapture(0)
max_value = 255
max_value_H = 360 // 2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
first = 'first'
second = 'second'
cv.namedWindow(first)
cv.namedWindow(second)


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H - 1, low_H)
    cv.setTrackbarPos("low_H", second, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H + 1)
    cv.setTrackbarPos("high_H", second, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S - 1, low_S)
    cv.setTrackbarPos("low_S", second, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S + 1)
    cv.setTrackbarPos("high_S", second, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V - 1, low_V)
    cv.setTrackbarPos("low_V", second, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V + 1)
    cv.setTrackbarPos("high_V", second, high_V)


cv.createTrackbar("low_H", second, low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar("high_H", second, high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar("low_S", second, low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar("high_S", second, high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar("low_V", second, low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar("high_V", second, high_V, max_value, on_high_V_thresh_trackbar)

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

    #Flipping the image
    flipped = cv.flip(frame, 1)
    # change color:
    hsv = cv.cvtColor(flipped, cv.COLOR_BGR2HSV)
    #blurring the image (src,out,borderType)
    blur = cv.GaussianBlur(hsv,(5,5),cv.BORDER_DEFAULT)

    #Check if run with parameters if so resize the image
    if len(sys.argv) > 1:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        final = cv.resize(blur,(width,height))
    else:
        final = cv.resize(blur, (320, 200))

    #Add display of inRange:
    zakres1 = "Low: {},{},{}".format(low_H,low_S,low_V)
    zakres2 = "High: {},{},{}".format(high_H, high_S, high_V)
    image = cv.putText(final, zakres1,(100,100),cv.FONT_ITALIC,1,(255,255,255))
    image = cv.putText(final, zakres2, (100, 150), cv.FONT_ITALIC, 1, (255, 255, 255))

    # Display the final images:
    cv.imshow(first, final)
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    cv.imshow(second, frame_threshold)

    #If 'x' has been pressed
    if cv.waitKey(33) == 120:
        # read image
        img_raw = cv.imread(first)
        # select ROI function
        roi = cv.selectROI(img_raw)

        print(roi)

        # Crop selected roi from raw image
        roi_cropped = img_raw[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]

        cv.imwrite("crop.jpeg", roi_cropped)
    #Break if 'esc' has been pressed
    if cv.waitKey(33) == 27:
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()