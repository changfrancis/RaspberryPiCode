import datetime, time, sys, thread, threading, signal, atexit
import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import sensors
import grovepi

#Enable Variables
alive = 1
aircon_enabled = 0
aircon_setpoint = 35.0 #higher safer

def run(peltierpin1, peltier1, peltierfanpin1):
	global aircon_enabled, aircon_setpoint
	aircon_pwm = 0
	peltier1.start(0)
	airconPID = PIDclass(18,6,5) #init P I D value
	airconPID.setSampleTime(0)
	print("Aircon PID ... Started")
	next_call = time.time()
	while(alive):
		airconPID.SetPoint = aircon_setpoint #target temperature in degree
		airconPID.update(sensors.adc1_temp_cur) #peltier blue 
		#print datetime.datetime.now()
		buf = airconPID.output * -1.0
		#print(buf)
		if(buf > 100):
			aircon_pwm = 100
		elif(buf <= 0):
			aircon_pwm = 0
		else:
			aircon_pwm = buf
			
		if(sensors.adc1_temp_cur <= -900):
			print("Error: Run away thermistor - Aircon")
			aircon_enabled = 0
			airconPID.clear()
			peltier1.start(0)
		else:
			if(aircon_enabled):
				peltier1.start(aircon_pwm)
				print("Aircon Temp = Tgt:%.1fC Cur:%.1fC PeltierOutput = %.1f" %(aircon_setpoint,sensors.adc1_temp_cur,aircon_pwm) + "%"  + " Enable = %d" %(aircon_enabled))
				if(sensors.adc1_temp_cur <= 25.5 or aircon_pwm >= 75.0): #dew point
					grovepi.analogWrite(peltierfanpin1,255) #full
				elif(aircon_pwm >= 50.0): 
					grovepi.analogWrite(peltierfanpin1,200) #full-half
				elif(aircon_pwm >= 10.0):
					grovepi.analogWrite(peltierfanpin1,125) #half
			else:
				peltier1.start(0)
				if(sensors.adc1_temp_cur <= 20.0): #dew point
					print("Aircon Self Protection : Fan On")
					grovepi.analogWrite(peltierfanpin1,255) #on
				else:
					grovepi.analogWrite(peltierfanpin1,0) #off
		next_call = next_call + 1
		time.sleep(next_call - time.time())
	peltier1.start(0)
	
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
