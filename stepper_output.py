import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi
import math

#Enable Variables
motor_enabled = 0
motor_direction = 1
motor_feedrate = 10

def run(dir_pin, step_pin, enable_pin):
	global motor_enabled, motor_direction, motor_feedrate
	motor = Stepper(dir_pin, step_pin, enable_pin) #dir_pin, step_pin, enable_pin
	print("Motor Thread ... Started")
	next_call = time.time()
	while True:	
		while(motor_enabled == 0):
			time.sleep(0.25)
			motor.set_off()
		if(motor_enabled):
			motor.set_direction(motor_direction)
			motor.set_on()
			motor.do_step(motor_feedrate)
		time.sleep(0.01)
		
class Stepper:
	"""
	Handles  A4988 hardware driver for bipolar stepper motors
	"""
	def __init__(self, dir_pin, step_pin, enable_pin): #Pin 26, 19, 13
		self.step_pin = step_pin
		self.dir_pin = dir_pin
		self.enable_pin = enable_pin
		GPIO.output(self.enable_pin,0) #set Low to enable     
		self.pulserate = 100
		self.count = 0
		self.speed = 0
		self.MAX_ACCEL = 100   #equivallent to 100 x (periodicity of set_speed) usteps/sec/sec

	def set_direction(self, direct): #1 cw, 0 ccw
		if(direct):
			GPIO.output(self.dir_pin,0)
		else:
			GPIO.output(self.dir_pin,1)
		time.sleep(0.005) 

	def do_step(self, feedrate):   # called by timer interrupt every 100us
		'''
		PCD = 11mm
		circumference = 2 * PI * 5.5 = 34.5575
		(360/1.8deg)*16 microstep = 3200 steps per rev
		'''
		delay = float(1.0 / feedrate)/10.0

		#print(steps_to_turn)
		#print(delay)
		for i in range (1, 10):
			GPIO.output(self.step_pin,1) 
			time.sleep(delay) 
			GPIO.output(self.step_pin,0)
			time.sleep(delay)  
        '''
        if self.dir == 0:
            return
        self.count = (self.count+1)%self.pulserate
        if self.count == 0:
			GPIO.output(self.step_pin,1) 
			GPIO.output(self.step_pin,0) 
        '''
	def set_speed(self, speed): #called periodically
		if (self.speed - speed) > self.MAX_ACCEL:
			self.speed -= self.MAX_ACCEL
		elif (self.speed - speed)< -self.MAX_ACCEL:
			self.speed+=self.MAX_ACCEL
		else:
			self.speed = speed
		# set direction
		if self.speed>0:
			self.dir = 1
			GPIO.output(self.dir_pin,1) 
			GPIO.output(self.enable_pin,0)     
		elif self.speed<0:
			self.dir = -1
			GPIO.output(self.dir_pin,0) 
			GPIO.output(self.enable_pin,0)                    
		else:
			self.dir = 0
		if abs(self.speed)>0:
			self.pulserate = 10000//abs(self.speed)

	def set_off(self):
		GPIO.output(self.enable_pin,1) 

	def set_on(self):
		GPIO.output(self.enable_pin,0) 

	def get_speed(self):
		return self.speed


