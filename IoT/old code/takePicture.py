from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()

camera.resolution = (2592, 1944)
camera.framerate = 15

camera.start_preview()
camera.annotate_background = Color('black')

#To take multiple images
#for i in range(5):
#    sleep(5)
#    camera.capture('/Users/manas/Desktop/image%s.jpg' % i)

sleep(5)
#Save image to a folder (for API to interact)
camera.capture('/Users/manas/Desktop/image.jpg')

#to record videos
#camera.start_recording
#sleep.(5)
#camera.stop_recording()

camera.stop_preview()
