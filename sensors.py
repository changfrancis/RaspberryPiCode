import time
import grove_i2c_temp_hum_mini

#Ambience Sensors
ht_sensor = grove_i2c_temp_hum_mini.th02()
ambience_sensor_enabled = 0
ambience_temp = 0
ambience_humidity = 0

def read_ambience_sensor(threadName):
	print("Starting " + threadName)
	global ambience_sensor_enabled, ambience_temp, ambience_humidity
	while True:
		if(ambience_sensor_enabled == 1):
			ambience_temp = ht_sensor.getTemperature()
			ambience_humidity = ht_sensor.getHumidity()
			#print("Temp: %.2fC\tHumidity:%.2f" %(ambience_temp,ambience_humidity) + "%")
			#print("ht sensor updated")
			time.sleep(5) #update rate is set to x seconds
