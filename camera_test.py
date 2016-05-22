import picamera
import cv2
import time
import numpy as np
from time import sleep
import matplotlib.pyplot as plt


def doCanny(input, lowThresh, highThresh, aperture):
	if input.nChannels != 1:
		return(0)
	out = cv2.CreateImage((input.width, input.height), input.depth, 1)
	cv2.Canny(input, out, lowThresh, aperture)
	return out 

def CannyThreshold(lowThreshold):
	detected_edges = cv2.GaussianBlur(gray,(7,7),0)
	detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold*ratio, apertureSize = kernel_size)
	dst = cv2.bitwise_and(img,img,mask = detected_edges)
	cv2.imshow('canny demo',dst)
	return dst 

print "OpenCV Version:", cv2.__version__
print "Program Start"

camera = picamera.PiCamera()
camera.annotate_text = "hello"
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotate = 0
camera.hflip = False
camera.vflip = False
camera.resolution = (800, 400)
camera.crop = (0.0, 0.0, 1.0, 1.0)


lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3

while True:
	sleep(1)
	camera.capture('image.jpg')
	img = cv2.imread('image.jpg')
	edges = cv2.Canny(img,100,200)
	cv2.imshow(edges)

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.namedWindow('canny demo')
#cv2.createTrackbar('Min threhold','canny demo', lowThreshold, max_lowThreshold, CannyThreshold)
#CannyThreshold(1)
#if cv2.waitKey(0) == 27:
# cv2.destroyAllWindows()
# break;

camera.close()
