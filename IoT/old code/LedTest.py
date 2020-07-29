import sys, time
import RPi.GPIO as GPIO
redPin = 11
greenPin = 13
bluePin = 15
def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
def redOn():
    blink(redPin)
def greenOn():
    blink(greenPin)
def blueOn():
    blink(bluePin)
def yellowOn():
    blink(redPin)
    blink(greenPin)
def purpleOn():
    blink(redPin)
    blink(bluePin)
def redOff():
    turnOff(redPin)
def greenOff():
    turnOff(greenPin)
def blueOff():
    turnOff(bluePin)
def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)
def purpleOff():
    turnOff(redPin)
    turnOff(bluePin)
def allOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)
def main():
    while True:
        cmd = input('Choose an option:')
        if cmd == 'red on':
            redOn()
        elif cmd == 'red off':
            redOff()
        elif cmd == 'green on':
            greenOn()
        elif cmd == 'green off':
            greenOff()
        elif cmd == 'yellow on':
            yellowOn()
        elif cmd == 'yellow off':
            yellowOff()
        elif cmd == 'blue on':
            blueOn()
        elif cmd == 'blue off':
            blueOff()
        elif cmd == 'purple on':
            purpleOn()
        elif cmd == 'purple off':
            purpleOff()
        elif cmd == 'exit':
            allOff()
            break   
main()

        