import cv2
import numpy as np
import requests
import picamera
from time import sleep
import I2C_LCD_driver
from time import *
from time import sleep
import RPi.GPIO as GPIO
import keypad as kp

camera = picamera.PiCamera()
mylcd = I2C_LCD_driver.lcd()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#displayLCD = True
on = False
counter = 0
button_counter = 0
display_turn_on_message = True
change_uid = True

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
uid = ''

"""
Set up keypad for uid
"""
L1 = 29 #GPIO 5
L2 = 31 #GPIO 6
L3 = 33 #GPIO 13
L4 = 35 #GPIO 19

C1 = 32 #GPIO 12
C2 = 36 #GPIO 16
C3 = 38 #GPIO 20
C4 = 40 #GPIO 21

kp.setup_keypad()

#Detect initial button press
GPIO.add_event_detect(10,GPIO.RISING)

while True: #Run forever
    '''
    Check to see if the facial detection should occur. This should only occur when the button is in
    State 1 (on)
    '''
    
    #If the facial detection has not turned on
    #display a message letting the user know to press the button to start facial detection
    if not on:
        
        if change_uid: #user is changing the uid
            print('starting to change uid')
            uid = kp.change_uid()
            change_uid = False
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Press button to", 1)
            mylcd.lcd_display_string("start class", 2)
            mylcd.lcd_display_string("Press # ", 3)
            mylcd.lcd_display_string("to change uid", 4)
            #display_turn_on_message = False
            
        else: #user is ready to start facial detection
            print('ready to start')
            if display_turn_on_message:
                mylcd.lcd_clear()
                mylcd.lcd_display_string("Press button to", 1)
                mylcd.lcd_display_string("start class", 2)
                mylcd.lcd_display_string("Press # ", 3)
                mylcd.lcd_display_string("to change uid", 4)
                display_turn_on_message = False
        
        #if the hash is clicked, flip the mini state
        if kp.hash_clicked():
            change_uid = not change_uid
        
    #When button is pressed and the facial detection is turned on
    if on:
        # Makes the camera capture and detect a face every 15 seconds
        if True:
            #Clear screen and display message that shows facial detection is happening
            mylcd.lcd_clear()
            mylcd.lcd_display_string("Detecting Face...", 1)
            
            # Capture and store an image
            camera.capture('example.jpg')
            img = cv2.imread('example.jpg', -1)
            print("capturing image")
            print(type(img))
            img_copy = img.copy()
                    
            # Correction for the image, noise cancelling
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
            # Gets the parts of the image that contains a face
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            face_found = False
                    
            # Draw a rectangle around the face
            for (x, y, w, h) in faces:
                cv2.rectangle(img_copy, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_found = True


            print(face_found)
                    
            # If a face is detected, check database and compare the feature vector of the image
            # to the verified feature vectors in the database through the Amazon Rekognition API
            if face_found:
                # Display a message that a face has been found on the LCD screen
                mylcd.lcd_display_string("Verifying face", 1)
                
                # Store the image locally in a file called img.jpg
                cv2.imwrite("img.jpg", img)
                
                # Access API to match the image taken to a verified face in the database
                url = "https://05ezlcm1cf.execute-api.us-east-1.amazonaws.com/FacialWorking/verifyimage"
                payload = {'Metadata': '{"uid": "' + uid + '"}'}
                files = [
                    ('file', open('img.jpg', 'rb'))
                ]
                headers = {}
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                body = response.json()
                        
                # If there is no error
                if body["error"] == False:
                    mylcd.lcd_clear() #Clear screen
                    
                    # If the face was detected but not verified with the API, re-scan the face 
                    if body['message'] == "No face has been found":
                        # Output a message to the LCD screen to tell the person that their face was not found
                        mylcd.lcd_display_string("Face not found", 1)
                        mylcd.lcd_display_string("Re-scanning...", 2)
                        print("face not found")
                    # If the face was detected and verified, display a welcome message on the LCD screen    
                    else:
                        # Clear screen and display a message saying that the face has been verified and the student's name
                        mylcd.lcd_clear()
                        print("Face Verified " + body['name'] + " - " + body['message'])
                        
                        mylcd.lcd_display_string("Welcome " + body['name'], 1)
                        sleep(5)
                        mylcd.lcd_clear()
                        
                # If there is an error, display an error message with instructions to press the button again
                else:
                    print("error")
                    mylcd.lcd_display_string("Error...", 1)
                    mylcd.lcd_display_string("Rescanning face...", 2)

                        
                  
    # Reset the frame counter when it reaches 61 so that it takes a picture every 60 seconds
    if counter == 61:
        counter = 0

    counter += 1
    
    #Detects if button has been pressed to turn on/off the facial detection
    if GPIO.event_detected(10) and len(uid) == 6:
        button_counter += 1
        if button_counter % 2 == 1:
            print("Turned on")
        else:
            print("Turned off")
            display_turn_on_message = True
            
        #Change the status of on and the facial detection
        on = not on
        
        if not on:
            display_turn_on_message = True
