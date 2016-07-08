import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from time import sleep

imgPath01 = 'image.jpg'
imgPath02 = 'image.jpg'
imgPath03 = 'image.jpg'
imgPath04 = 'image.jpg'
CValue1 = 0
CValue2 = 0
CValue3 = 0
CValue4 = 0
CValue5 = 0
CValue6 = 0
CValue7 = 0
CValue8 = 0
CValue9 = 0
imageWidth = 210
imageHeight = 400
cur_image = 0
write_complete_flag = 0

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(150, (1.0 - sigma) * v))
	upper = int(min(300, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

def run(camera):
	global cur_image, CValue1, CValue2, CValue3, CValue4, CValue5, CValue6, CValue7, CValue8, CValue9, imageWidth, imageHeight, write_complete_flag    
	print "OpenCV Version:", cv2.__version__
	print(camera + " ... Started")
	camera = PiCamera()
	camera.resolution =  (imageWidth, imageHeight)
	camera.framerate = 8
	camera.rotation = 90
	rawCapture = PiRGBArray(camera, size= (imageWidth, imageHeight))
	time.sleep(1)
	counter = 1
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		image = frame.array
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		gauss = cv2.GaussianBlur(gray,(3,3),0)
		edges = cv2.Canny(gray,25,75,apertureSize = 3)
		autoedged = auto_canny(image)
		#lines = cv2.HoughLinesP(edges,1,math.pi/2,2,None, 30, 1)

		#cv2.imwrite(cur_image, edges)
		#print(cur_image)
		#cur_image = edges
		#cv2.imwrite("image.jpg", image)
		
		#cv2.imshow('Manual', edges)
		#print(CValue1)
		
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		counter = counter + 1
		if(counter % 10 == 0):
			write_complete_flag = 0
			#cv2.imwrite("/home/pi/Desktop/MyCode/image_auto.jpg", autoedged)
			#cv2.imwrite("/home/pi/Desktop/MyCode/image_original.jpg", image)
			#cv2.imwrite("/home/pi/Desktop/MyCode/image_gray.jpg", gray)
			print("update image")
			counter = 1
			write_complete_flag = 1
		cv2.imshow("Auto", autoedged)
		time.sleep(1)
	#camera.close()
	
class LineDetection:
    """LineDetection Controller
    """
    def __init__(self, _pixel, _threshold, _minLineLength, _maxLineGap):
        self.pixel=_pixel
        self.threshold=_threshold
        self.minLineLength=_minLineLength
        self.maxLineGap=_maxLineGap
        
	def auto_canny(self, image, sigma=0.33):
		# compute the median of the single channel pixel intensities
		v = np.median(image)
	 
		# apply automatic Canny edge detection using the computed median
		lower = int(max(150, (1.0 - sigma) * v))
		upper = int(min(300, (1.0 + sigma) * v))
		edged = cv2.Canny(image, lower, upper)
		# return the edged image
		return edged

