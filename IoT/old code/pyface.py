import cv2
import numpy as np
import requests
import picamera
from time import sleep
import I2C_LCD_driver
from time import *
from time import sleep
import RPi.GPIO as GPIO

camera = picamera.PiCamera()
mylcd = I2C_LCD_driver.lcd()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#displayLCD = True
on = True
counter = 0
detecting = False
buttonPress = 0


def detect_faces():
    '''
    Check to see if the facial detection should occur. This should only occur when the button is in
    State 1 (on)
    '''
    global on
    global buttonPress
    global counter
    
    #while buttonPress % 2 == 1:
    if on:
        # Makes the camera capture and detect a face every 15 seconds
        if counter % 60 == 15:
            # Capture and store an image
            camera.capture('example.jpg')
            img = cv2.imread('example.jpg', -1)
            print("capturing image")
            print(type(img))
            img_copy = img.copy()
                
            # Correction for the image, noise cancelling
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
            # gets the parts of the image that contains a face
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
                payload = {'Metadata': '{"uid": "32UZSbhFX7bQGdmm"}'}
                files = [
                    ('file', open('img.jpg', 'rb'))
                ]
                headers = {}
                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                body = response.json()
                    
                # If there is no error
                try:
                    if body["error"] == False:
                        # If the face was detected but not verified with the API, re-scan the face 
                        if body['message'] == "No face has been found":
                            # Output a message to the LCD screen to tell the person that their face was not found
                            mylcd.lcd_display_string("Face not found", 1)
                            mylcd.lcd_display_string("Re-scanning...", 2)
                        # If the face was detected and verified, display a welcome message on the LCD screen    
                        else:
                            # Clear screen and output a message saying the face has been found
                            mylcd.lcd_clear()
                            print("Face Verified " + body['name'] + " - " + body['message'])
                            #if displayLCD == True:
                            mylcd.lcd_display_string("Welcome " + body['name'], 1)
                            sleep(3)
                            mylcd.lcd_clear()
                            return
                            displayLCD = False
                    # If there is an error print error onto console
                    else:
                        mylcd.lcd_display_string("Error...", 1)
                        mylcd.lcd_display_string("Please press the", 2)
                        mylcd.lcd_display_string("button again", 3)
                except:
                    mylcd.lcd_display_string("Error...", 1)
                    mylcd.lcd_display_string("Please press the", 2)
                    mylcd.lcd_display_string("button again", 3)
                    
              
    # Reset the frame counter when it reaches 61 so that it takes a picture every 60 seconds
    if counter == 61:
        counter = 0

    counter += 1

    # Press a key on the keyboard to turn off
    #k = cv2.waitKey(30) & 0xff
    #if k == 100:
        #print("switched")
        #on = not on

def button_callback(channel):
    """
    @param:
    @return:
    """
    global on
    global buttonPress
    global counter
    print("Button was pushed!")
    global buttonPress
    buttonPress += 1
    print(buttonPress)
    mylcd.lcd_clear()
    GPIO.cleanup() # Clean up
    
    #setting GPIO pins
    if buttonPress % 2 == 1:
        mylcd.lcd_display_string("Scanning...", 1)
        while buttonPress % 2 == 1:
            detect_faces()
            
            #GPIO.setwarnings(False) # Ignore warning
            #GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
            #GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
            #GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)


            #mylcd.lcd_display_string("Press button to scan", 1)
            #print("Press button to scan")
            #GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)
            #message = input("Press enter to quit\n\n") # Run until someone presses enter
    else:
        mylcd.lcd_display_string("Turned off", 1)
    


GPIO.setwarnings(False) # Ignore warning
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
#GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)


mylcd.lcd_display_string("Press button to scan", 1)
print("Press button to scan")
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up