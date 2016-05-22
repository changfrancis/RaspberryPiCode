import time, sys, threading, signal, atexit
import numpy as np
from time import sleep
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import grove_i2c_temp_hum_mini
import PID

class ADC:
	address = None
	
	REG_ADDR_RESULT = 0x00
	REG_ADDR_ALERT  = 0x01
	REG_ADDR_CONFIG = 0x02
	REG_ADDR_LIMITL = 0x03
	REG_ADDR_LIMITH = 0x04
	REG_ADDR_HYST   = 0x05
	REG_ADDR_CONVL  = 0x06
	REG_ADDR_CONVH  = 0x07

	def __init__(self,address=0x55):
		self.address=address
		#bus.write_byte_data(self.address, self.REG_ADDR_CONFIG,0x20)

	def adc_read(self):
		#data=bus.read_i2c_block_data(self.address, self.REG_ADDR_RESULT, 2)
		raw_val=(data[0]&0x0f)<<8 | data[1]
		return raw_val

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class
    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID.PID(P, I, D)

    pid.SetPoint=0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint > 0:
            feedback += (output - (1/i))
        if i>9:
            pid.SetPoint = 1
        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = spline(time_list, feedback_list, time_smooth)

    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
    plt.xlim((0, L))
    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

    plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()

# Exit handlers
def exitProgram():
	print "Exiting"
	sys.exit(0)
	
def Read_Temp_Humid():
	print("Temp: %.2fC\tHumidity:%.2f" %(ht_sensor.getTemperature(),ht_sensor.getHumidity()),"%")

def printit():
		threading.Timer(2.0, printit).start()
		print "hello, world"

if __name__ == "__main__": 
	ht_sensor = grove_i2c_temp_hum_mini.th02()
	adc = ADC()
	#test_pid(1.2, 1, 0.001, L=50)
	printit()
	while True:
		adc.address
		Read_Temp_Humid() 
		print(adc.address)
		time.sleep(1)
