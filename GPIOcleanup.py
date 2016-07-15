import RPi.GPIO as GPIO
import sys
from time import sleep
import time

GPIO.setmode(GPIO.BCM)

for i in range (2, 26):
	print i
	GPIO.setup(i, GPIO.OUT)
	
for i in range (2, 26):
	GPIO.setup(i, GPIO.LOW)
	
peltierpin1 = 21 #AC
peltierpin2 = 20 #Cold Block	
	
GPIO.setup(peltierpin1, GPIO.OUT) 
GPIO.output(peltierpin1,1)
GPIO.setup(peltierpin2, GPIO.OUT) 
GPIO.output(peltierpin2,1)
#peltier1.start(50)

while(True):
	print("hi")
	time.sleep(1)
	
GPIO.cleanup()

sys.exit(0)
