import cv2 as cv

cascade_src = 'cars.xml'
video_src = 'vid.mp4'
cap = cv.VideoCapture(video_src)

min_contour_width = 40
min_contour_height = 40
approx = 10
line_height = 350
matches = []
count = 0

def getCenter(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)

while True:
    ret, frame = cap.read()
    if (type(frame) == type(None)):
        break

    #Using the cars cascade to identify cars:
    car_cascade = cv.CascadeClassifier(cascade_src)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)

    for (x, y, w, h) in cars:
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)
        if not contour_valid:
            continue
        cv.rectangle(frame, (x - approx, y - approx), (x + w + approx, y + h + approx), (0), 2)

        center = getCenter(x, y, w, h)
        matches.append(center)
        cv.circle(frame, center, 5, (255, 0, 0), -1)
    for (x, y) in matches:
        if y < (line_height + approx) and y > (line_height - approx):
            count += 1
            matches.remove((x, y))
            print(count)
    cv.line(frame, (0, line_height), (3000, line_height), (0, 0, 255), 2)
    cv.putText(frame, "Count: " + str(count), (10, 50), cv.FONT_ITALIC, 1, (0, 0, 0), 2)

    cv.imshow('video', frame)

    if cv.waitKey(1) == 27:
        break

cv.destroyAllWindows()