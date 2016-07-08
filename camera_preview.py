'''
For len focus tuning
'''
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
grovepi.ledCircle_on(mycircle)
time.sleep(0.3)

x_resolution = 1080
y_resolution = 1920

try:
	camera = picamera.PiCamera()
	camera.resolution = (x_resolution, y_resolution)
	camera.rotation = 90
	camera.start_preview()
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	camera.stop_preview()
	camera.close()
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)

except Exception, e:
	print(str(e))
	camera.stop_preview()
	camera.close()
	grovepi.ledCircle_off(mycircle)
	time.sleep(0.2)
