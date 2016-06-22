import time
import grove_i2c_temp_hum_mini
import grove_i2c_adc

#Setting Variables

#Ambience Sensors
ht_sensor = grove_i2c_temp_hum_mini.th02()
ambience_sensor_enabled = 0
ambience_temp = 0
ambience_humidity = 0

#Tempepature Sensors Peltier, heater block
# You can initialize with a different address too: grove_i2c_adc.ADC(address=0x56)
adc = grove_i2c_adc.ADC()
adc1_sensor_enabled = 0
adc1_temp = 0
adc2_sensor_enabled = 0
adc2_temp = 0
adc3_sensor_enabled = 0
adc3_temp = 0

def read_sensors(threadName):
	print("Starting " + threadName)
	global ambience_sensor_enabled, ambience_temp, ambience_humidity, adc1_sensor_enabled, adc1_temp
	counter = 0
	while True:
		if(ambience_sensor_enabled == 1) and (counter % 20 == 0):
			ambience_temp = ht_sensor.getTemperature()
			time.sleep(0.2) 
			ambience_humidity = ht_sensor.getHumidity()
			time.sleep(0.2) 
			#print("Temp: %.2fC\tHumidity:%.2f" %(ambience_temp,ambience_humidity) + "%")
			#print("ht sensor updated")	
		if(adc1_sensor_enabled == 1) and (counter % 5 == 0):
			adc1_temp = adc.adc_read()
			time.sleep(0.2) 
			#print("Temp:" %(adc1_temp) + "C")
			#print("adc1 updated")
		counter = counter + 1
		#print(counter)
		if(counter >= 50):
			counter = 0
		time.sleep(0.1) #update rate is set to x seconds
