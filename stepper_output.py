import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi
import screen
import math

#Enable Variables
motor_enabled = 0

def run(dir_pin, step_pin, enable_pin):
	global motor_enabled
	motor = Stepper(dir_pin, step_pin, enable_pin) #dir_pin, step_pin, enable_pin
	print("Motor Thread ... Started")
	next_call = time.time()
	while True:	
		if(motor_enabled):
			motor.do_step(400,100)
		#else:
		#	motor.set_off()
		next_call = next_call + 2
		time.sleep(next_call - time.time())
		

class Stepper:
    """
    Handles  A4988 hardware driver for bipolar stepper motors
    """
    
    def __init__(self, dir_pin, step_pin, enable_pin): #Pin 26, 19, 13
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        GPIO.output(self.enable_pin,0) #set Low to enable     
        self.dir = 0
        self.pulserate = 100
        self.count = 0
        self.speed = 0
        self.MAX_ACCEL = 100   #equivallent to 100 x (periodicity of set_speed) usteps/sec/sec
        
	def set_direction(direct): #1 cw, 0 ccw
		self.dir = direct
		GPIO.output(self.dir_pin,self.dir)
		time.sleep(0.00005) 

    def do_step(self, length, mm_per_sec):   # called by timer interrupt every 100us
        '''
        PCD = 11mm
        circumference = 2 * PI * 5.5 = 34.5575
        (360/1.8deg)*16 microstep = 3200 steps per rev
        '''
        circumference = 2 * math.pi * 5.5
        mm_per_step = circumference / 3200
        one_mm_equal = int(1 / mm_per_step)
        #print(one_mm_equal)
        
        steps_to_turn = int(length / mm_per_step)
        fastest = 0.000002
        slowest = 0.5
        start_speed = 0.01
        delay = 0.000005
        
        steps_to_turn = length
        
        #print(steps_to_turn)
        for i in range (1, steps_to_turn):
			GPIO.output(self.step_pin,1) 
			time.sleep(0.0010) 
			GPIO.output(self.step_pin,0)
			time.sleep(0.0010)  
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


