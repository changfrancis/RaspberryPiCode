#from picamera.array import PiRGBArray
import picamera 
from picamera.array import PiRGBArray
import io
import cv2
import time
import numpy
from time import sleep
import matplotlib.pyplot as plt
import math
import time
import grovepi
from PIL import Image

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = numpy.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(25, (1.0 - sigma) * v))
	upper = int(min(75, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

print "OpenCV Version:", cv2.__version__
print "Program Start"
mycircle = 6
grovepi.pinMode(mycircle,"OUTPUT")
grovepi.ledCircle_init(mycircle)
time.sleep(0.2)
grovepi.ledCircle_on(mycircle)
time.sleep(0.2)

#x_resolution = 1080
#y_resolution = 1920
#x_crop1 = 282
#x_crop2 = 619
#y_crop1 = 360
#y_crop2 = 1920

x_resolution = 480
y_resolution = 640
x_crop1 = 125
x_crop2 = 275
y_crop1 = 120
y_crop2 = 640

stream = io.BytesIO()
'''
with picamera.PiCamera() as camera:
	#camera = PiCamera()
	camera.resolution = (x_resolution,y_resolution) #(1080,1920) max resolution of 30 fps but can pi prcoess other information fast enough ?
	camera.rotation = 90
	camera.capture(stream, format='jpeg')
	#camera.crop = (10, 10, 0.1, 0.1)
'''
camera = picamera.PiCamera()
camera.resolution = (x_resolution,y_resolution)
camera.rotation = 90
camera.framerate = 8
camera.start_preview()
time.sleep(2)
rawCapture = PiRGBArray(camera)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	buff = frame.array
	print(buff)
	#crop_image = image[y_crop1:y_crop2, x_crop1:x_crop2] #crop from y h x w
	gray = cv2.cvtColor(buff,cv2.COLOR_BGR2GRAY)
	gauss = cv2.GaussianBlur(gray,(3,3),0)
	autoedged = auto_canny(gauss)
	cv2.imshow("Auto", autoedged)
	#cv2.imwrite("image1.jpg", autoedged)
	#cv2.imwrite("image2.jpg", crop_image)
	cv2.waitKey(1)
	#stream.flush()
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	print("hi")
	#time.sleep(0.5)


try:	
	#for frame in camera.capture_continuous(stream, format="jpeg"):
	while True:
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
		image = cv2.imdecode(buff,1)
		crop_image = image[y_crop1:y_crop2, x_crop1:x_crop2] #crop from y h x w
		gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
		gauss = cv2.GaussianBlur(gray,(3,3),0)
		autoedged = auto_canny(gauss)
		cv2.imshow("Auto", autoedged)
		time.sleep(1)
		cv2.imwrite("image1.jpg", autoedged)
		cv2.imwrite("image2.jpg", crop_image)
		cv2.waitKey(1)
		# clear the stream in preparation for the next frame
		stream.truncate(0)
		print("hi")

except KeyboardInterrupt:
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)
	camera.close()

except Exception, e:
	print(str(e))
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)
	camera.close()
	

'''
mini = 25
maxi = 75

camera = PiCamera()
camera.resolution = (210, 400)
camera.framerate = 8
camera.rotation = 90
rawCapture = PiRGBArray(camera, size=(210, 400))

grovepi.ledCircle_init(mycircle)
time.sleep(0.5)
grovepi.ledCircle_on(mycircle)
time.sleep(0.5)

try:
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
		# show the frame
		cv2.imshow("Auto", autoedged)
		cv2.imshow('Manual', edges)
		cv2.imwrite("image.jpg", edges)
		#cv2.imshow('frame', im_with_keypoints)
		key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
			
except KeyboardInterrupt:
	grovepi.ledCircle_off(mycircle)
	camera.close()
'''
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


