import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi

#Enable Variables
alive = 1
hotend_enabled = 0
hotend_setpoint = 25.0 #lower safer

def run(heaterpin, heater):
	global hotend_enabled, hotend_setpoint
	hotend_pwm = 0
	heater.start(0)
	hotendPID = PIDclass(8,1,4.5) #init P I D value
	hotendPID.setSampleTime(0)
	print("Hotend PID ... Started")
	next_call = time.time()
	while(alive):
		try:
			hotendPID.SetPoint = hotend_setpoint #target temperature in degree
			hotendPID.update(sensors.adc3_temp_cur) #peltier blue 
			#print datetime.datetime.now()
			buf = hotendPID.output * 1.0
			#print(buf)
			if(buf >= 50):
				hotend_pwm = 50
			elif(buf <= 0):
				hotend_pwm = 0
			else:
				hotend_pwm = buf
			if(sensors.adc3_temp_cur <= -900):
				print("Error: Run away thermistor - Hotend")
				hotend_enabled = 0
				hotendPID.clear()
				heater.start(0)
			else:
				if(hotend_enabled and sensors.adc3_temp_cur <= 160.0):
					heater.start(hotend_pwm)
					print("Hotend Temp = Tgt:%.1fC Cur:%.1fC HeaterOutput = %.1f" %(hotend_setpoint,sensors.adc3_temp_cur,hotend_pwm) + "%"  + " Enable = %d" %(hotend_enabled))
				else:
					heater.start(0)
			next_call = next_call + 1
			time.sleep(next_call - time.time())
		except Exception, e:
			print(str(e))
	heater.start(0)
	
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

