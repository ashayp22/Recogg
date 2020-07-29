import cv2
import numpy



cap = cv2.VideoCapture(0) #capture the video camera

#update loop updating every frame

while True:

    ret, img = cap.read()

    '''
    Check to see if the facial detection should occur. This should only occur when the button is in
    State 1 (on)
    '''

    '''
    If the facal detection should happen, capture the frame every 1 second
    '''

    #check if a request has been made

    #store the frame locally

    #apply the facial detection classifier


    #if a face is detected, call the API

        #if the face was verified, then update the LCD screen

    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
