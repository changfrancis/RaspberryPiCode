from PyQt5 import QtCore, QtGui, QtWidgets
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

#Enable Variables
alive = 1
camera_enabled = 0
x_resolution = 1088
y_resolution = 1920
x_crop1 = 282
x_crop2 = 619
y_crop1 = 360
y_crop2 = 1920
imgPath01 = 0
edgesigma = 0.25
LineLength = 500
LineGap = 300

def auto_canny(image, sigma):
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

def run(cameraThread):  
	global imgPath01, edgesigma, minLineLength, maxLineGap
	print(cameraThread + " ... Started")
	while(alive):
		if(camera_enabled):
			image = get_image()
			crop_image = image[y_crop1:y_crop2, x_crop1:x_crop2] #crop from y h x w
			#print(type(image))
			gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
			gauss = cv2.GaussianBlur(gray,(3,3),0)
			autoedged = auto_canny(gauss, edgesigma)
			edged = cv2.Canny(gauss, 25, 75)
			lines = cv2.HoughLinesP(autoedged, 1, math.pi/2, 2, minLineLength=LineLength, maxLineGap=LineGap)
			img = edged.copy()
			if(lines is not None):
				if(len(lines) > 0):
					#print(len(lines))
					counter = 0
					for line in lines:
						#print(line)
						#print(line[0])
						cv2.line(crop_image,(line[0][0],line[0][1]),(line[0][2],line[0][3]),(0,255,0),5)
						counter = counter + 1
						if(counter > 10):
							break
			outputimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			imgPath01 = QtGui.QImage(outputimage.data, outputimage.shape[1], outputimage.shape[0], QtGui.QImage.Format_RGB888)
			#cv2.imshow("Auto", autoedged)
			#cv2.imshow("manual", crop_image)
			#cv2.imwrite("image1.jpg", image)
			#cv2.waitKey(0)
			time.sleep(0.25)
		else:
			time.sleep(0.1)
	
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

