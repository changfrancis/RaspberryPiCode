from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
import math

'''
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
'''

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(150, (1.0 - sigma) * v))
	upper = int(min(300, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

print "OpenCV Version:", cv2.__version__
print "Program Start"

mini = 25
maxi = 75
camera = PiCamera()
camera.resolution = (210, 400)
camera.framerate = 8
rawCapture = PiRGBArray(camera, size=(210, 400))
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	gauss = cv2.GaussianBlur(gray,(3,3),0)
	edges = cv2.Canny(gray,mini,maxi,apertureSize = 3)
	autoedged = auto_canny(image)
	lines = cv2.HoughLinesP(edges,1,math.pi/2,2,None, 30, 1)
	
	print(mini)
	mini = mini + 1
	maxi = maxi + 1
	print(len(edges))
	print(len(edges[0]))
	
	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()
	 
	# Change thresholds
	params.minThreshold = 0.1;
	params.maxThreshold = 200;
	 
	# Filter by Area.
	params.filterByArea = True
	params.minArea = 1
	 
	# Filter by Circularity
	params.filterByCircularity = True
	params.minCircularity = 0.1
	 
	# Filter by Convexity
	params.filterByConvexity = True
	params.minConvexity = 0.87
	 
	# Filter by Inertia
	params.filterByInertia = True
	params.minInertiaRatio = 0.01
	 
	# Create a detector with the parameters
	ver = (cv2.__version__).split('.')
	if int(ver[0]) < 3 :
		detector = cv2.SimpleBlobDetector(params)
	else : 
		detector = cv2.SimpleBlobDetector_create(params)
		
	keypoints = detector.detect(image)
	im_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	
	
	#print(edges[0])
	'''
	for rho,theta in lines[0]:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
		cv2.line(image,(x1,y1),(x2,y2),(0,0,255),2)
	'''	
	# show the frame
	cv2.imshow("Auto", autoedged)
	cv2.imshow('Manual', edges)
	#cv2.imshow('frame', im_with_keypoints)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

'''
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
camera.rotation = 0
camera.hflip = False
camera.vflip = False

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
	cv2.imshow('image.jpg')
'''
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.namedWindow('canny demo')
#cv2.createTrackbar('Min threhold','canny demo', lowThreshold, max_lowThreshold, CannyThreshold)
#CannyThreshold(1)
#if cv2.waitKey(0) == 27:
# cv2.destroyAllWindows()
# break;

camera.close()
