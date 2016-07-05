# cd /home/pi/Desktop/MyCode
# git status
# use "git add xxx.py" ,to add new files
# git commit -a 
# hit enter, key-in some comments
# git push 
# hit enter, key-in user and password
# user: changfrancis@hotmail.com
# pw: 8524879j

#GUI Compile command
#pyuic5 -x mainwindow.ui -o mainwindow.py

import datetime, time, sys, thread, threading, signal, atexit, serial
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from time import sleep
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import PID
import mainwindow
import sensors
import grovepi
import aircon_output
import coldblock_output
import stepper_output
import hotend_output
import herkulex
from herkulex import servo
import mainwindow
import buzzer

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
	herkulex.servo_enabled = 0
	grovepi.analogWrite(peltierfanpin1,0)
	grovepi.analogWrite(peltierfanpin2,0)
	grovepi.ledCircle_off(ledcirclepin)
	peltier1.start(0)
	peltier2.start(0)
	heater.start(0)
	GPIO.output(motor_enable_pin,1) #set H to disable
	GPIO.output(motor_dir_pin,0) #set H to disable
	GPIO.output(motor_step_pin,0) #set H to disable
	herkulex.clear_errors()
	servo1.torque_off()
	servo2.torque_off()
	servo3.torque_off()
	herkulex.close()
	GPIO.cleanup()
	time.sleep(1.5)
	sys.exit(0)
	
def Read_Temp_Humid():
	print("Temp: %.2fC\tHumidity:%.2f" %(ht_sensor.getTemperature(),ht_sensor.getHumidity()),"%")

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
		buzzerpin = 4 #buzzer
		ledcirclepin = 6 #led circular

		#Servo Motor Configuration
		herkulex.connect("/dev/ttyS0", 115200)
		herkulex.clear_errors()
		#servos = herkulex.scan_servos(0x01,0x02) #min and max range of ServoID
		#print(servos)
		servo1=servo(0x01,0x02) #ServoID, Model
		servo2=servo(0x02,0x02) #ServoID, Model
		servo3=servo(0x03,0x02) #ServoID, Model
		#servo1.set_servo_angle(50, 1, 0x00) #goaltime is 1 to 255
		time.sleep(0.1)
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
		#Fans
		grovepi.analogWrite(peltierfanpin1,0) #aircon, 0-255
		grovepi.analogWrite(peltierfanpin2,0) #coldblock, 0-255
		#Buzzer
		grovepi.pinMode(buzzerpin,"OUTPUT")
		grovepi.digitalWrite(buzzerpin,0) #off
		#LED Circular for Camera
		grovepi.pinMode(ledcirclepin,"OUTPUT")
		grovepi.ledCircle_init(ledcirclepin)
		
		#Starting Individual Thread
		#thread.start_new_thread(screen.display, ("ScreenThread",))
		thread.start_new_thread(sensors.read_sensors, ("SensorsThread",)) #start sensor thread
		
		aircon = threading.Thread(target=aircon_output.run, args = (peltierpin1,peltier1,peltierfanpin1))
		aircon.daemon = True
		aircon.start()
		
		coldblock = threading.Thread(target=coldblock_output.run, args = (peltierpin2,peltier2,peltierfanpin2))
		coldblock.daemon = True
		coldblock.start()
		
		hotend = threading.Thread(target=hotend_output.run, args = (heaterpin, heater))
		hotend.daemon = True
		hotend.start()
		
		motorthread = threading.Thread(target=stepper_output.run, args = (motor_dir_pin,motor_step_pin,motor_enable_pin))
		motorthread.daemon = True
		motorthread.start()
		
		herkulexthread = threading.Thread(target=herkulex.run, args = (servo1,servo2,servo3))
		herkulexthread.daemon = True
		herkulexthread.start()
		
		#Enable buzzer warning
		buzzer.alertbuzzer_enabled = 1
		thread.start_new_thread(buzzer.run, (buzzerpin,)) #start sensor thread
		
		#Enable the devices and sensors
		sensors.ambience_sensor_enabled = 0 #enable temp reading after thread start
		sensors.adc1_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc2_sensor_enabled = 1 #enable adc reading after thread start
		sensors.adc3_sensor_enabled = 1 #enable adc reading after thread start
		
		#Enable LED Circular lights - Camera
		grovepi.ledCircle_on(ledcirclepin)
		
		time.sleep(0.5)
		print("\n\n\nBoot-up ... Successful\n\n\n")
		buzzer.beep(buzzerpin, 1)
		
	except Exception, e:
		print(str(e))
		print("\n\n\nBoot-up ... Failed\n")
		buzzer.beep_fail(buzzerpin)
		GPIO.cleanup()

	app = QtWidgets.QApplication(sys.argv)
	app.aboutToQuit.connect(exitProgram)
	labelWindow = QtWidgets.QMainWindow()
	ui = mainwindow.Ui_labelWindow(peltierfanpin1,peltierfanpin2, peltier1, peltier2, heater, motor_step_pin, motor_dir_pin, motor_enable_pin, buzzerpin, ledcirclepin)
	ui.setupUi(labelWindow)
	ui.updateSetpoint_all_threads()
	labelWindow.show()
	sys.exit(app.exec_())
	GPIO.cleanup()
	
	'''
	while True:
		try:
			#print("Ambience Temp = %.1f" %sensors.ambience_temp + "C")
			#print("Ambience Humidity = %.1f" %sensors.ambience_humidity  + "%")
			#print("AC = %.1f" %sensors.adc1_temp_cur + "C")
			#print("ColdBlock = %.1f" %sensors.adc2_temp_cur + "C")
			#print("HotEnd = %.1f" %sensors.adc3_temp_cur + "C")
			#data = ser.read(10)
			#print('hellodasdasdasdasdasdadsworld2')
			servo1.torque_on()
			servo1.set_servo_angle(150, 100, 0x00) #goaltime is 1 to 255
			servo2.torque_on()
			servo2.set_servo_angle(150, 100, 0x00) #goaltime is 1 to 255
			servo3.torque_on()
			servo3.set_servo_angle(150, 100, 0x00) #goaltime is 1 to 255
			time.sleep(1)
			herkulex.clear_errors()
			#print(servo1.get_servo_status_detail())
			#print(servo2.get_servo_status_detail())
			#print(servo3.get_servo_status_detail())
			
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
	'''
