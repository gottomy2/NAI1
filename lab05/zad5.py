import cv2 as cv

cascade_src = 'cars.xml'
video_src = 'video.avi'
cap = cv.VideoCapture(video_src)

def detectCars(frame):
    car_cascade = cv.CascadeClassifier(cascade_src)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    count = 0;
    for (x, y, w, h) in cars:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
        count += 1
        print(count)
    cv.imshow('video', frame)

while True:
    ret, frame = cap.read()
    if (type(frame) == type(None)):
        break

    detectCars(frame)
    if cv.waitKey(33) == 27:
        break

cv.destroyAllWindows()