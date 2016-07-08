#!/usr/bin/env python
#
# GrovePi Example for using the Grove LED Bar (http://www.seeedstudio.com/wiki/Grove_-_LED_Bar)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
import random

# Connect the Grove LED Bar to digital port D5
# DI,DCKI,VCC,GND
mycircle = 6

grovepi.pinMode(mycircle,"OUTPUT")
time.sleep(1)
i = 0

# LED Bar methods
# grovepi.ledBar_init(pin,orientation)
# grovepi.ledBar_orientation(pin,orientation)
# grovepi.ledBar_setLevel(pin,level)
# grovepi.ledBar_setLed(pin,led,state)
# grovepi.ledBar_toggleLed(pin,led)
# grovepi.ledBar_setBits(pin,state)
# grovepi.ledBar_getBits(pin)


while True:
	try:
		grovepi.ledCircle_init(mycircle)
		time.sleep(0.5)

		for i in range(0,25):
			print(i)
			grovepi.ledCircleselective_on(mycircle, i)
			time.sleep(.2)
		time.sleep(.3)
		
		for i in range(0,25):
			print(i)
			grovepi.ledCircleselective_off(mycircle, i)
			time.sleep(.2)
		time.sleep(.3)
		'''
		print ("Test 14) Step")
		# step through all 10 LEDs
		for i in range(0,25):
			grovepi.ledBar_setLevel(ledbar, i)
			time.sleep(.2)
		time.sleep(.3)
		
		print ("Test 2) Set level")
		# ledbar_setLevel(pin,level)
		# level: (0-10)
		for i in range(0,25):
			grovepi.ledBar_setLevel(ledbar, i)
			time.sleep(.2)
		time.sleep(.3)

		grovepi.ledBar_setLevel(ledbar, 8)
		time.sleep(.5)

		grovepi.ledBar_setLevel(ledbar, 2)
		time.sleep(.5)

		grovepi.ledBar_setLevel(ledbar, 5)
		time.sleep(.5)
		'''
	except KeyboardInterrupt:
		grovepi.ledCircle_off(mycircle)
		break
	except IOError:
		print ("Error")
