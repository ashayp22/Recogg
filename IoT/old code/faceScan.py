#python  --image rooster.jpg --prototxt dep[loy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel
import cv2
import argparse
import numpy np
import LedTest
import camera

#construct argument parse and parse the arguments
#allows user to input an image
ap = argopparse.ArgumentParser()

#for image
#ap.add_argument("-i", "/home/pi/image.jpg", required=True,
#    help="path to input image")
#Caffe prototxt file
#ap.add_argument("-p", "/home/pi/deep-learning-face-detection/deploy.prototxt.txt", required=True,
#    help="path to Caffe 'deploy' prototxt file")
#pretrained Caffe model
#ap.add_argument("-m", "/home/pi/deep-learning-face-detection/res10_300x300_ssd_iter_140000.caffemodel", required=True,
#    help="path to Caffe pre-trained model"

#overrite confidence threshold to .5
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

#these are the paths to the image
originalImage = "/home/pi/image.jpg"
prototxt = "/home/pi/deep-learning-face-detection/deploy.prototxt.txt"
model = "/home/pi/deep-learning-face-detection/res10_300x300_ssd_iter_140000.caffemodel"


#load model
print("[INFO] loading model...")
net = cv2.dnn.readNetfromCaffe(prototxt, model) #store model

#load image
image = cv2.imread(originalImage) #store image
(h, w) = image.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                             (300, 300), (104.0, 177.0, 123.0)) #takes care of preprocessing; use this moving forward

#pass blob through the network and obtain detections
#LED stays off through this process
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

#Now start detecting faces
#go through detections
for i in range(0, detections.shape[2]):
    #get the confidences for each of the images
    confidence = detections[0, 0, i, 2]
    
    #filter out weak (less than 50% confidence) detections
    if confidence > args["confidence"]:
        #LED turns yellow because we know there is a face and it will process
        LedTest.yellowOn()
        #here we need to send the image to API
        break
    if i = detections.shape[2]:
        break