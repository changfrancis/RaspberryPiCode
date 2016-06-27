# cd /home/pi/Desktop/MyCode
# git status
# use "git add xxx.py" ,to add new files
# git commit -a 
# hit enter, key-in some comments
# git push 
# hit enter, key-in user and password
# user: changfrancis@hotmail.com
# pw: 8524879j

from Tkinter import *
import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import PID
import screen
import sensors
import grovepi
import aircon_output

# Exit handlers
def exitProgram():
	print("\n\n\nExiting...\n")
	grovepi.analogWrite(peltierfanpin1,0)
	peltier1.start(0)
	peltier2.start(0)
	heater.start(0)
	GPIO.cleanup()
	time.sleep(1)
	sys.exit(0)
	
def Read_Temp_Humid():
	print("Temp: %.2fC\tHumidity:%.2f" %(ht_sensor.getTemperature(),ht_sensor.getHumidity()),"%")

def printit():
		threading.Timer(2.0, printit).start()
		print "hello, world"

if __name__ == "__main__": 
	try:
		peltierpin1 = 16
		peltierpin2 = 20
		heaterpin = 21
		peltierfanpin1 = 3
		peltierfanpin2 = 5

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(peltierpin1, GPIO.OUT)
		GPIO.setup(peltierpin2, GPIO.OUT)
		GPIO.setup(heaterpin, GPIO.OUT)
		peltier1 = GPIO.PWM(peltierpin1, 50)
		peltier1.start(0)
		peltier2 = GPIO.PWM(peltierpin2, 50)
		peltier2.start(0)
		heater = GPIO.PWM(heaterpin, 50)
		heater.start(0)
		grovepi.pinMode(peltierfanpin1,"OUTPUT")
		time.sleep(1)
		grovepi.analogWrite(peltierfanpin1,255) #0-255
		time.sleep(0.2)
		
		
		sensors.ambience_sensor_enabled = 0 #enable temp reading after thread start
		sensors.adc1_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc2_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc3_sensor_enabled = 1 #enable adc reading after thread start
		#thread.start_new_thread(screen.display, ("ScreenThread",))
		#time.sleep(0.2)
		thread.start_new_thread(sensors.read_sensors, ("SensorsThread",))
		time.sleep(0.2)
		print("Boot-up ... Successful\n")
	except Exception, e:
		print(str(e))
		print("Boot-up ... Failed\n")
		GPIO.cleanup()

	aircon = threading.Thread(target=aircon_output.run)
	aircon.daemon = True
	aircon.start()
	
	while True:
		try:
			#print("Ambience Temp = %.1f" %sensors.ambience_temp + "C")
			#print("Ambience Humidity = %.1f" %sensors.ambience_humidity  + "%")
			print("ADC1 Temp = %.1f" %sensors.adc1_temp_cur + "C")
			#print("ADC2 Temp = %.1f" %sensors.adc2_temp_cur + "C")
			#print("ADC3 Temp = %.1f" %sensors.adc3_temp_cur + "C")
			time.sleep(0.75)
		except KeyboardInterrupt:
			print("\nKeyboard Shutdown\n")
			exitProgram()
			break
		except IOError:
			print("Error")
			exitProgram()
	GPIO.cleanup()
'''
	root = Tk()
	topFrame = Frame(root)
	topFrame.pack(side=TOP)
	bottomFrame = Frame(root)
	bottomFrame.pack(side=BOTTOM)
	
	button1 = Button(topFrame, text="Start", bg="white", fg="green")
	button2 = Button(topFrame, text="End", bg="white", fg="blue")
	button3 = Button(topFrame, text="Exit", bg="white", fg="red", command=exitProgram)
	button4 = Button(bottomFrame, text="Bottom", bg="black", fg="yellow")
	button5 = Button(bottomFrame, text="Fill", bg="black", fg="yellow")
	entry1 = Entry(bottomFrame)
	
	c = Checkbutton(bottomFrame, text="checkbox")
	
	button1.pack(side=LEFT, fill=X)
	button2.pack(side=LEFT, fill=Y)
	button3.pack(side=LEFT)
	
	button4.grid(row=0,column=0, sticky="N")
	button5.grid(row=0,column=1, sticky="E")
	entry1.grid(row=1,column=0, sticky="S")
	c.grid(columnspan=2, sticky="S")
	
	theLabel = Label(topFrame, text="hi hello world")
	theLabel.pack(side=TOP)
	
	root.mainloop()
	
	ht_sensor = grove_i2c_temp_hum_mini.th02()
	adc = ADC()
	#test_pid(1.2, 1, 0.001, L=50)
	printit()
	while True:
		adc.address
		Read_Temp_Humid() 
		print(adc.address)
		time.sleep(3)
'''
