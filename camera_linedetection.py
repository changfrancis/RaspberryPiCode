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
cameraPID_enabled = 0
x_resolution = 1088
y_resolution = 1920
x_crop1 = 252
x_crop2 = 639
y_crop1 = 470
y_crop2 = 1600#1920
imgPath01 = 0
edgesigma = 0.25
LineLength = 500
LineGap = 300
OutputDia1 = 0
OutputDia2 = 0
OutputDia3 = 0

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
	global imgPath01, edgesigma, minLineLength, maxLineGap, x_crop1, x_crop2, y_crop1, y_crop2, OutputDia1, OutputDia2, OutputDia3
	print(cameraThread + " ... Started")
	counter = 0
	while(alive):
		if(camera_enabled):
			image = get_image()
			crop_image = image[y_crop1:y_crop2, x_crop1:x_crop2] #crop from y h x w
			#print(type(image))
			gray = cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
			gauss = cv2.GaussianBlur(gray,(3,3),0)
			autoedged = auto_canny(gauss, edgesigma)
			edged = cv2.Canny(gauss, 25, 75)
			'''
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
			'''
			try:
				outputimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #Setup image
				outputimage = cv2.rectangle(outputimage, (x_crop1,y_crop1), (x_crop2,y_crop2), (0,0,255), 3) #highlight sensing region
				#outputimage = cv2.cvtColor(autoedged, cv2.COLOR_GRAY2RGB) #print(autoedged.shape[1]) #print(autoedged.shape[0])
				if(counter % 2 == 0):
					outputimage = getFilamentImageReading(outputimage, autoedged, 0, 50, 1)
					outputimage = getFilamentImageReading(outputimage, autoedged, 400, 425, 2)
					outputimage = getFilamentImageReading(outputimage, autoedged, 800, 825, 3)
				imgPath01 = QtGui.QImage(outputimage.data, outputimage.shape[1], outputimage.shape[0], QtGui.QImage.Format_RGB888)
				#cv2.imshow("Auto", autoedged)
				#cv2.imshow("manual", crop_image)
				#cv2.imwrite("image1.jpg", image)
				#cv2.waitKey(0)
			except Exception, e:
				print(str(e))
			counter = counter + 1
			if(counter >= 50):
				counter = 0
			time.sleep(0.33)
		else:
			time.sleep(0.5)
	
def getFilamentImageReading(_image, _autoedged, _range1, _range2, _changeOutput): 
	try:
		global x_crop1, x_crop2, y_crop1, y_crop2, OutputDia1, OutputDia2, OutputDia3
		image = _image
		col_width_min = 9999
		col_width_max = 0
		checkheight = _range2 - _range1
		sum_width = 0.0
		for i in range(_range1,_range2): #Row
			for j in range(len(_autoedged[i])): #Column
				if(_autoedged[i][j] == 255):
					image = cv2.circle(_image, (x_crop1+j,y_crop1+i), 5, (255,0,0), -1) #source, position, size, colour, fillthickness
					if(j <= col_width_min):
						col_width_min = j
						#print("MIN %d" %col_width_min)
					if(j >= col_width_max):
						col_width_max = j
						#print("MAX %d" %col_width_max)
			delta_width = col_width_max - col_width_min
			#print("Width %d" %delta_width)
			sum_width = sum_width + delta_width
		sum_width = float(sum_width / checkheight)
		#print("Width %.2f" %sum_width)
		if(_changeOutput == 1):
			OutputDia1 = sum_width
		elif(_changeOutput == 2):
			OutputDia2 = sum_width
		elif(_changeOutput == 3):
			OutputDia3 = sum_width
		return image
	except Exception, e:
		print(str(e))
		if(_changeOutput == 1):
			OutputDia1 = 9999
		elif(_changeOutput == 2):
			OutputDia2 = 9999
		elif(_changeOutput == 3):
			OutputDia3 = 9999
		image = _image
		return image
	
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

