import cv2
import numpy as np
vidcap = cv2.VideoCapture(0)
vidcap.set(3,640) #width
vidcap.set(4,480) #height
vidcap.set(10,150) #brightness
color = (0,0,0)
minArea = 50
maxArea = 300
count=0
resizeWindow = 480,100
nPlateCascade = cv2.CascadeClassifier('resources/haarcascade_russian_plate_number.xml')
while True:
    success, img = vidcap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',imgGray)
    numberPlate = nPlateCascade.detectMultiScale(imgGray, 1.2, 3)

    for (x, y, w, h) in numberPlate:
        area = w*h
        if(area>minArea ):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img,"No. Plate",(x,y-3),cv2.FONT_HERSHEY_PLAIN,1,color,2)
            #roi : region of interest
            imgROI= img[y:y+h,x:x+w]
            imgROI= cv2.resize(imgROI,(resizeWindow))
            cv2.imshow('ROI',imgROI)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Number Plate',img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Resources/Scanned/NoPlate_" + str(count) + ".jpg", imgROI)
        img2 = img.copy()
        cv2.rectangle(img2, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img2, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                    2, (0, 0, 255), 2)

        count += 1
        cv2.imshow("Saved", img2)
        cv2.waitKey(1)
