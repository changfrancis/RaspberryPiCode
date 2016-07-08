import time
import grove_i2c_temp_hum_mini
import grove_i2c_adc

#Ambience Sensors
alive = 1
ht_sensor = grove_i2c_temp_hum_mini.th02()
ambience_sensor_enabled = 0
ambience_temp = 25
ambience_humidity = 80

#Tempepature Sensors Peltier, heater block
# You can initialize with a different address too: grove_i2c_adc.ADC(address=0x56)
adc1 = grove_i2c_adc.ADC1()
adc2 = grove_i2c_adc.ADC2()
adc3 = grove_i2c_adc.ADC3()
adc1_sensor_enabled = 0 #AC
adc1_temp_cur = 28
adc1_temp_old = 28
adc2_sensor_enabled = 0 #Cold block
adc2_temp_cur = 28
adc2_temp_old = 28
adc3_sensor_enabled = 0 #hot end
adc3_temp_cur = 28
adc3_temp_old = 28

#SemiTec 104GT2 Lookuptable
temperaturetable = [[-50,8],[-40,16],[-30,32],[-20,60],[-10,107],[0,183],[10,299],[20,465],[30,687],[40,962],[50,1276],[60,1606],[70,1926],[80,2216],[90,2466],[100,2671],[110,2835],[120,2963],[130,3062],[140,3138],[150,3196],[160,3241],[170,3276],[180,3302],[190,3323],[200,3340],[210,3353],[220,3363],[230,3372],[240,3378],[250,3384],[260,3388],[270,3392],[280,3395],[290,3398],[300,3400]]

def read_sensors(threadName):
	print("Starting " + threadName)
	global alive, ambience_sensor_enabled, ambience_temp, ambience_humidity, adc1_sensor_enabled, adc1_temp_cur, adc1_temp_old, adc2_sensor_enabled, adc2_temp_cur, adc2_temp_old, adc3_sensor_enabled, adc3_temp_cur, adc3_temp_old
	counter = 0
	while(alive):
		if(ambience_sensor_enabled == 1) and (counter % 20 == 0):
			ambience_temp = ht_sensor.getTemperature()
			time.sleep(0.1) 
			ambience_humidity = ht_sensor.getHumidity()
			time.sleep(0.1) 
			print("DHT Temp: %.2fC\tHumidity:%.2f" %(ambience_temp,ambience_humidity) + "%")
			#print("dht sensor updated")	
		if(adc1_sensor_enabled == 1) and (counter % 2 == 0):
			buf = get_semitecindegree(adc1.adc_read())
			adc1_temp_cur = (buf +  adc1_temp_old) / 2
			adc1_temp_old = adc1_temp_cur
			#print("Aircon Temp: %.1f" %(adc1_temp_cur) + "C")
			#print("adc1 updated")
		if(adc2_sensor_enabled == 1) and (counter % 2 == 0):
			buf = get_semitecindegree(adc2.adc_read())
			adc2_temp_cur = (buf +  adc2_temp_old) / 2
			adc2_temp_old = adc2_temp_cur
			#print("Coldblock Temp: %.1f" %(adc2_temp_cur) + "C")
			#print("adc2 updated")
		if(adc3_sensor_enabled == 1) and (counter % 2 == 0):
			buf = get_semitecindegree(adc3.adc_read())
			adc3_temp_cur = (buf +  adc3_temp_old) / 2
			adc3_temp_old = adc3_temp_cur
			#print("Hotend Temp: %.1f" %(adc3_temp_cur) + "C")
			#print("adc3 updated")
		counter = counter + 1
		#print(counter)
		if(counter >= 50):
			counter = 0
		time.sleep(0.25) #update rate is set to x seconds

def get_semitecindegree(adcreading):
	global temperaturetable
	for i in range(len(temperaturetable)):
		#print (i)
		if(adcreading <= 7): #becasue lowest we have is reading=8
			return -999 #error in conversion
		elif(temperaturetable[i][1] > adcreading):
			buf1 = (temperaturetable[i][1] - temperaturetable[i-1][1]) / 10.0
			buf2 = adcreading - temperaturetable[i-1][1]
			buf3 = (buf2/buf1) + temperaturetable[i-1][0]
			#print("Temperature reading is %.2f"%(buf3))	
			return buf3 #normal temp
	return -999 #error in conversion
