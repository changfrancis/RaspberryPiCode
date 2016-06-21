# cd /home/pi/Desktop/MyCode
# git status
# git commit -a 
# hit enter, key-in some comments
# git push 
# hit enter, key-in user and password
from Tkinter import *
import time, sys, thread, signal, atexit
import numpy as np
from time import sleep
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import PID
import screen
import sensors

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
	try:
		thread.start_new_thread(screen.display, ("ScreenThread",))
		thread.start_new_thread(sensors.read_ambience_sensor, ("AmbienceThread",))
		sensors.ambience_sensor_enabled = 1 #enable reading after thread start
		time.sleep(1)
		print("Boot-up ... Successful\n")
		while True:
			print("Ambience Temp = %.1f" %sensors.ambience_temp + "C")
			print("Ambience Humidity = %.1f" %sensors.ambience_humidity  + "%")
			time.sleep(5)
	except Exception, e:
		print(str(e))
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
