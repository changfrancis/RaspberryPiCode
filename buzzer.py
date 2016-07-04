import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi

#Enable Variables
alertbuzzer_enabled = 0

def run(buzzerpin):
	global alertbuzzer_enabled
	print("Buzzer Alert ... Started")
	time.sleep(5)
	while True:
		if(alertbuzzer_enabled):	
			if(sensors.adc1_temp_cur <= -900):
				grovepi.digitalWrite(buzzerpin,1) 
				print("ALERT: Aircon Sensor - Failed")
				time.sleep(1)
				grovepi.digitalWrite(buzzerpin,0) 
			elif(sensors.adc2_temp_cur <= -900):
				grovepi.digitalWrite(buzzerpin,1)
				print("ALERT: Coldblock Sensor - Failed")
				time.sleep(1)
				grovepi.digitalWrite(buzzerpin,0)
			elif(sensors.adc3_temp_cur <= -900):
				grovepi.digitalWrite(buzzerpin,1)
				print("ALERT: Hotend Sensor - Failed")
				time.sleep(1)
				grovepi.digitalWrite(buzzerpin,0)
			else:
				grovepi.digitalWrite(buzzerpin,0)
			time.sleep(2)
		else:
			time.sleep(10)

def beep(buzzerpin, num):
	for i in range (0, num):
		grovepi.digitalWrite(buzzerpin,1)
		time.sleep(0.15) 
		grovepi.digitalWrite(buzzerpin,0)
		time.sleep(0.15)  
	grovepi.digitalWrite(buzzerpin,0)
	
def beep_click(buzzerpin):
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.02) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.01)

def beep_scroll(buzzerpin):
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.01) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.01)  	
	
def beep_fail(buzzerpin):
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.5) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.1)
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.2) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.1)
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.2) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.1) 
	grovepi.digitalWrite(buzzerpin,1)
	time.sleep(0.2) 
	grovepi.digitalWrite(buzzerpin,0)
	time.sleep(0.1)  
