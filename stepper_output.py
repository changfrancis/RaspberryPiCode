import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi
import math
import camera_linedetection

#Enable Variables
alive = 1
motor_enabled = 0
motor_direction = 1
motor_feedrate = 5
cameraP = 0
cameraI = 0
cameraD = 0
cameraPIDsetpoint = 0

def run(dir_pin, step_pin, enable_pin):
	global motor_enabled, motor_direction, motor_feedrate, cameraP, cameraI, cameraD, cameraPIDsetpoint
	#cameraPIDControl = PIDclass(0,0,0) #init P I D value
	#cameraPIDControl.setSampleTime(0)
	motor = Stepper(dir_pin, step_pin, enable_pin) #dir_pin, step_pin, enable_pin
	print("Motor Thread ... Started")
	next_call = time.time()
	while(alive):	
		try:
			while(motor_enabled == 0):
				time.sleep(0.5)
				motor.set_off()
			if(motor_enabled):
				motor.set_direction(motor_direction)
				motor.set_on()
				if(camera_linedetection.cameraPID_enabled):
					if(camera_linedetection.OutputDia1 < -999):
						motor.do_step(motor_feedrate)
						#print("ignore input")
					elif(cameraPIDsetpoint >= camera_linedetection.OutputDia1):
						buf = ((cameraPIDsetpoint - camera_linedetection.OutputDia1)/10.0) * cameraP 
						motor.do_step(motor_feedrate+buf)
					elif(cameraPIDsetpoint < camera_linedetection.OutputDia1):
						buf = ((camera_linedetection.OutputDia1 - cameraPIDsetpoint)/10.0) * cameraP 
						motor.do_step(motor_feedrate-buf)
					else:
						motor.do_step(motor_feedrate)
				else:
					motor.do_step(motor_feedrate)
		except Exception, e:
				print(str(e))
		time.sleep(0.02) #10-20ms
		
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

	def do_step(self, _feedrate):   # called by timer interrupt every 100us
		'''
		PCD = 11mm
		circumference = 2 * PI * 5.5 = 34.5575
		(360/1.8deg)*16 microstep = 3200 steps per rev
		'''
		if(_feedrate <= 1):
			feedrate = 1
		else:
			feedrate = _feedrate
		#print(feedrate)
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

class PIDclass:
    """PID Controller
    """
    def __init__(self, P, I, D):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value):
        """Calculates PID value for given reference feedback
        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        .. figure:: images/pid_1.png
           :align:   center
           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)
        """
        error = self.SetPoint - feedback_value

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time

