import picamera
import time
#hello world
camera = picamera.PiCamera()
camera.vflip = True
camera.start_recording('examplevid.h264')
time.sleep(5)
camera.stop_recording()
#camera.capture('example.jpg')