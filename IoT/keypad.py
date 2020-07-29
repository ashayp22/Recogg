# This example is a hello world example
# for using a keypad with the Raspberry Pi

import RPi.GPIO as GPIO
import time
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()
uid_array = []
uid = None
entering_uid = True
new_uid = True

L1 = 29 #GPIO 5
L2 = 31 #GPIO 6
L3 = 33 #GPIO 13
L4 = 35 #GPIO 19

C1 = 32 #GPIO 12
C2 = 36 #GPIO 16
C3 = 38 #GPIO 20
C4 = 40 #GPIO 21

"""
Setup for the keypad
Connect the keypad characters to the GPIO pins

@param none
@return none
"""
def setup_keypad():
    GPIO.setwarnings(False)
    #BCM before
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

"""
Reads the line on the keypad based on what iis pressed

@param line - the the GPIO pin to which an output needs to be provided
@param characters - an array of the chracters in a row of the keypad
@return chracters[i] - The 4 possible characters for that specific GPIO pin
"""

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    c_list = [C1, C2, C3, C4]
    #Get the list of characters in the line that was pressed based on the C list of GPIO pins
    for i in range(4):
        if GPIO.input(c_list[i]) == 1:
            GPIO.output(line, GPIO.LOW)
            return characters[i]
    GPIO.output(line, GPIO.LOW)
    return None

"""
Returns a character if pressed; else it returns None

@param none
@return temp - the character that was pressed
"""    
def getCharacter():
    #List of GPIO pins
    l_list = [L1, L2, L3, L4]
    #List of the GPIO pins' corresponding possible values
    b_list = [["1","2","3","A"], ["4","5","6","B"], ["7","8","9","C"], ["*","0","#","D"]]
    
    #Return the character pressed
    for i in range(4):
        temp = readLine(l_list[i], b_list[i])
        if temp is not None:
            return temp
        
    return None
    
"""
Driver function - reads the characters pressed and returns the final product

@param none
@return ''.join(uid_array) - the string for the uid of the class
"""    
    
def change_uid():
    global uid_array
    global new_uid
    
    uid_array = []
    
    while len(uid_array) < 6:
        
        character = getCharacter()
        #Append the character to the uid_array unless it is a '#' or a '*'
        #If '#' or '*' are clicked, perform their respective functions
        #'*' clears the uid
        #'#' do nothing because the uid is already being changed
        if character is not None:
            if character == '*':
                uid_array = []
                mylcd.lcd_clear()
            elif character == '#':
                continue
            else:
                uid_array.append(character)    
        print(uid_array)
        if new_uid: #Only clear once, not everytime - prevents words from flashing
            mylcd.lcd_clear()
            new_uid = False
        #Display the chracters pressed so far onto the screen
        mylcd.lcd_display_string("Uid: " + ''.join(uid_array), 1)
        #Message telling the user how to finish entering the uid
        mylcd.lcd_display_string("Press * to clear uid", 3)
        
            
        time.sleep(0.3)
    new_uid = True
    return ''.join(uid_array)

"""
Tells us if a '#' has been pressed or not

@param none
@return True or False based on whether a '#' was clicked or not
"""
def hash_clicked():
    return getCharacter() == '#'
