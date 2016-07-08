#from picamera.array import PiRGBArray
import picamera 
import picamera.array
import io
import cv2
import time
import numpy
from time import sleep
import matplotlib.pyplot as plt
import math
import time
import grovepi
import PIL

print "OpenCV Version:", cv2.__version__
print "Program Start"
mycircle = 6
grovepi.pinMode(mycircle,"OUTPUT")
grovepi.ledCircle_init(mycircle)
time.sleep(0.2)
grovepi.ledCircleintensity(mycircle,200)
time.sleep(0.1)

x_resolution = 1080
y_resolution = 1920
x_crop1 = 282
x_crop2 = 619
y_crop1 = 360
y_crop2 = 1920
'''
x_resolution = 480
y_resolution = 640
x_crop1 = 125
x_crop2 = 275
y_crop1 = 120
y_crop2 = 640
'''
def auto_canny(image, sigma=0.25):
	# compute the median of the single channel pixel intensities
	v = numpy.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

# Create the in-memory stream
def get_image():
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (x_resolution, y_resolution)
		camera.rotation = 90
		with picamera.array.PiRGBArray(camera) as stream:
			camera.capture(stream, format='bgr')
			image = stream.array
		camera.close()
	return image

try:
	while True:
		image = get_image()
		crop_image = image[y_crop1:y_crop2, x_crop1:x_crop2] #crop from y h x w
		#print(type(image))
		gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
		gauss = cv2.GaussianBlur(gray,(3,3),0)
		autoedged = auto_canny(gauss)
		edged = cv2.Canny(gauss, 25, 75)
		lines = cv2.HoughLinesP(autoedged, 1, math.pi/2, 2, minLineLength=500, maxLineGap=300)
		print(len(lines))
		img = edged.copy()
		if(len(lines) > 0):
			#print(lines)
			counter = 0
			for line in lines:
				#print(line)
				#print(line[0])
				cv2.line(crop_image,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(0,255,0),5)
				counter = counter + 1
				if(counter > 10):
					break
		cv2.imshow("Auto", autoedged)
		cv2.imshow("manual", crop_image)
		#cv2.imwrite("image1.jpg", image)
		cv2.waitKey(1)
		time.sleep(0.5)

except KeyboardInterrupt:
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)

except Exception, e:
	print(str(e))
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)

