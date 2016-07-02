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
import datetime, time, sys, thread, threading, signal, atexit, serial
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
import coldblock_output
import stepper_output
import hotend_output

# Exit handlers
def exitProgram():
	print("Exiting...\n\n\n")
	
	sensors.ambience_sensor_enabled = 0 
	sensors.adc1_sensor_enabled = 0 
	sensors.adc2_sensor_enabled = 0 
	sensors.adc3_sensor_enabled = 0 
	aircon_output.aircon_enabled = 0 
	coldblock_output.coldblock_enabled = 0
	hotend_output.hotend_enabled = 0 
	stepper_output.motor_enabled = 0
	
	grovepi.analogWrite(peltierfanpin1,0)
	grovepi.analogWrite(peltierfanpin2,0)
	peltier1.start(0)
	peltier2.start(0)
	heater.start(0)
	GPIO.output(motor_enable_pin,1) #set H to disable
	GPIO.output(motor_dir_pin,0) #set H to disable
	GPIO.output(motor_step_pin,0) #set H to disable
	GPIO.cleanup()
	time.sleep(1.5)
	sys.exit(0)
	
def Read_Temp_Humid():
	print("Temp: %.2fC\tHumidity:%.2f" %(ht_sensor.getTemperature(),ht_sensor.getHumidity()),"%")

def printit():
		threading.Timer(2.0, printit).start()
		print "hello, world"

if __name__ == "__main__": 
	try:
		print(sys.version)
		#Pin setting
		peltierpin1 = 21 #AC
		peltierpin2 = 20 #Cold Block
		heaterpin = 16 #HotEnd
		peltierfanpin1 = 5 #D5 AC
		peltierfanpin2 = 3 #D3 Cold block
		motor_dir_pin = 26 #Stepper motor
		motor_step_pin = 19
		motor_enable_pin = 13

		#/dev/ttyAMA0
		ser = serial.Serial("/dev/serial0", 9600, timeout=1)
		ser.close()
		ser.open()
		ser.flush()
		'''ser = serial.Serial(port='/dev/ttyAMA0',
		baudrate=9600,
		parity=serial.PARITY_NONE, 
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1)
		'''
		#Configuration of Pin IO
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False) #disable warning
		#Stepper Motor
		GPIO.setup(motor_step_pin, GPIO.OUT) 
		GPIO.setup(motor_dir_pin, GPIO.OUT)
		GPIO.setup(motor_enable_pin, GPIO.OUT)
        #Aircon
		GPIO.setup(peltierpin1, GPIO.OUT) 
		peltier1 = GPIO.PWM(peltierpin1, 50)
		peltier1.start(0)
		grovepi.pinMode(peltierfanpin1,"OUTPUT")
		#ColdBlock
		GPIO.setup(peltierpin2, GPIO.OUT) 
		peltier2 = GPIO.PWM(peltierpin2, 50)
		peltier2.start(0)
		grovepi.pinMode(peltierfanpin2,"OUTPUT")
		#HotEnd
		GPIO.setup(heaterpin, GPIO.OUT) 
		heater = GPIO.PWM(heaterpin, 50)
		heater.start(0)
		time.sleep(0.1)
		
		grovepi.analogWrite(peltierfanpin1,0) #aircon, 0-255
		grovepi.analogWrite(peltierfanpin2,255) #coldblock, 0-255
		
		#Starting Individual Thread
		#thread.start_new_thread(screen.display, ("ScreenThread",))
		
		thread.start_new_thread(sensors.read_sensors, ("SensorsThread",))
		
		aircon = threading.Thread(target=aircon_output.run, args = (peltierpin1,peltier1))
		aircon.daemon = True
		aircon.start()
		
		coldblock = threading.Thread(target=coldblock_output.run, args = (peltierpin2,peltier2))
		coldblock.daemon = True
		coldblock.start()
		
		hotend = threading.Thread(target=hotend_output.run, args = (heaterpin, heater))
		hotend.daemon = True
		hotend.start()
		
		motorthread = threading.Thread(target=stepper_output.run, args = (motor_dir_pin,motor_step_pin,motor_enable_pin))
		motorthread.daemon = True
		motorthread.start()
		
		#Enable the devices ans sensors
		sensors.ambience_sensor_enabled = 0 #enable temp reading after thread start
		sensors.adc1_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc2_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc3_sensor_enabled = 1 #enable adc reading after thread start
		aircon_output.aircon_enabled = 1 #enable power to pin
		coldblock_output.coldblock_enabled = 1 #enable power to pin
		hotend_output.hotend_enabled = 0 #enable power to pin
		stepper_output.motor_enabled = 1 #enable power to pin

		time.sleep(0.8)
		
		print("\n\n\nBoot-up ... Successful\n")
		time.sleep(0.2)
		
	except Exception, e:
		print(str(e))
		print("Boot-up ... Failed\n")
		GPIO.cleanup()

	while True:
		try:
			#print("Ambience Temp = %.1f" %sensors.ambience_temp + "C")
			#print("Ambience Humidity = %.1f" %sensors.ambience_humidity  + "%")
			#print("AC = %.1f" %sensors.adc1_temp_cur + "C")
			#print("ColdBlock = %.1f" %sensors.adc2_temp_cur + "C")
			#print("HotEnd = %.1f" %sensors.adc3_temp_cur + "C")
			#print('hello world1')
			#ser.write("dadasdada\n")
			#data = ser.read(10)
			#print('hellodasdasdasdasdasdadsworld2')
			time.sleep(1)
		except KeyboardInterrupt:
			print("\n\n\nKeyboard Shutdown")
			exitProgram()
			break
		except IOError, e:
			print(str(e))
			print("\n\n\nError")
			IOError
			exitProgram()
		except Exception, e:
			print(str(e))

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
