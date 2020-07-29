import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)
print("working")
GPIO.output(14, GPIO.HIGH)
time.sleep(5)
GPIO.output(14, GPIO.LOW)
GPIO.cleanup()
print("done")
