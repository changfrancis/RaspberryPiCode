# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Jul  4 11:03:21 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!
import datetime, time, sys, thread, threading, signal, atexit, serial
from PyQt5 import QtCore, QtGui, QtWidgets
import RPi.GPIO as GPIO
import stepper_output		
import sensors
import aircon_output
import coldblock_output
import stepper_output
import hotend_output
import grovepi
import herkulex
from herkulex import servo
import camera_linedetection
import buzzer

class Ui_labelWindow(object):
	def __init__(self, _peltierfanpin1, _peltierfanpin2, _peltier1, _peltier2, _heater, _motor_step_pin, _motor_dir_pin, _motor_enable_pin, _buzzerpin, _ledcirclepin):
		self.peltierfanpin1 = _peltierfanpin1
		self.peltierfanpin2 = _peltierfanpin2
		self.peltier1 = _peltier1
		self.peltier2 = _peltier2
		self.heater = _heater
		self.motor_step_pin = _motor_step_pin
		self.motor_dir_pin = _motor_dir_pin
		self.motor_enable_pin = _motor_enable_pin
		self.motorStart = 0
		self.buzzerpin = _buzzerpin
		self.ledcirclepin = _ledcirclepin
		
	def updateTemperaturelabel(self):
		while True:
			self.labelReadAircon.setText("{:.1f} C".format(sensors.adc1_temp_cur))
			self.labelReadColdblock.setText("{:.1f} C".format(sensors.adc2_temp_cur))
			self.labelReadHotend.setText("{:.1f} C".format(sensors.adc3_temp_cur))
			#update image.jpg, havent write
			'''
			if(camera_linedetection.write_complete_flag):
				self.labelPic1.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image_auto.jpg"))
				self.labelPic2.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image_original.jpg"))
				self.labelPic3.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image_gray.jpg"))	
			#img = camera_linedetection.cur_image
			#myImage = QtGui.QImage(img.data, img.shape[1], img.shape[0], bytePerLine, QImage.Format_RGB888)
			#self.labelPic4.setPixmap(QtGui.QPixmap.fromImage(myImage))
			'''
			time.sleep(1) #update rate is set to x seconds
	
	def function_refreshCameravale(self):
		self.labelCValue1.setText("{:.1f}".format(self.scrollControl1.value()))
		self.labelCValue2.setText("{:.1f}".format(self.scrollControl2.value()))
		self.labelCValue3.setText("{:.1f}".format(self.scrollControl3.value()))
		self.labelCValue4.setText("{:.1f}".format(self.scrollControl4.value()))
		self.labelCValue5.setText("{:.1f}".format(self.scrollControl5.value()))
		self.labelCValue6.setText("{:.1f}".format(self.scrollControl6.value()))
		self.labelCValue7.setText("{:.1f}".format(self.scrollControl7.value()))
		self.labelCValue8.setText("{:.1f}".format(self.scrollControl8.value()))
		self.labelCValue9.setText("{:.1f}".format(self.scrollControl9.value()))
		camera_linedetection.CValue1 = self.scrollControl1.value()
		camera_linedetection.CValue2 = self.scrollControl2.value()
		camera_linedetection.CValue3 = self.scrollControl3.value()
		camera_linedetection.CValue4 = self.scrollControl4.value()
		camera_linedetection.CValue5 = self.scrollControl5.value()
		camera_linedetection.CValue6 = self.scrollControl6.value()
		camera_linedetection.CValue7 = self.scrollControl7.value()
		camera_linedetection.CValue8 = self.scrollControl8.value()
		camera_linedetection.CValue9 = self.scrollControl9.value()
		
	
	def updateSetpoint_all_threads(self):
			print("update set point")
	
	def function_Exit(self):
		print("Exiting...type2\n\n\n")
		buzzer.beep_click(self.buzzerpin)
		self.function_Estop()
		herkulex.alive = 0
		stepper_output.alive = 0
		coldblock_output.alive = 0
		hotend_output.alive = 0
		aircon_output.alive = 0
		sensors.alive = 0
		time.sleep(1.0)
		sensors.ambience_sensor_enabled = 0 
		sensors.adc1_sensor_enabled = 0 
		sensors.adc2_sensor_enabled = 0 
		sensors.adc3_sensor_enabled = 0 
		time.sleep(1.5)
		sys.exit()
	
	def turn_on_selected_LED(self):
		grovepi.ledCircleintensity(self.ledcirclepin, 10) #intensity is 0-255
		time.sleep(0.1)
	
	def function_scrollFilament(self):
		buf = self.scrollFilament.value()/100.0
		self.lcdFilament.setProperty("value", buf)
		herkulex.servo_enabled = 1
		herkulex.filament_dia = buf
		buzzer.beep_scroll(self.buzzerpin)
		#print(buf)
	
	def function_scrollFeedrate(self):
		buf = self.scrollFeedrate.value()
		self.lcdFeedrate.setProperty("value", buf)
		stepper_output.motor_feedrate = buf
		buzzer.beep_scroll(self.buzzerpin)
		#print(stepper_output.motor_feedrate)
		
	def function_scrollAircon(self):
		buf = self.scrollAircon.value()/10.0
		self.lcdAircon.setProperty("value", buf)
		aircon_output.aircon_setpoint = buf	
		buzzer.beep_scroll(self.buzzerpin)
	
	def function_scrollColdblock(self):
		buf = self.scrollColdblock.value()/10.0
		self.lcdcoldblock.setProperty("value", buf)
		coldblock_output.coldblock_setpoint = buf
		buzzer.beep_scroll(self.buzzerpin)
	
	def function_scrollHotend(self):
		buf = self.scrollHotend.value()/10.0
		self.lcdHotend.setProperty("value", buf)
		hotend_output.hotend_setpoint = buf
		buzzer.beep_scroll(self.buzzerpin)
	
	def function_ONaircon(self):
		self.lcdAircon.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		aircon_output.aircon_enabled = 1 
		buzzer.beep_click(self.buzzerpin)
		
	def function_OFFaircon(self):
		self.lcdAircon.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		aircon_output.aircon_enabled = 0 
		buzzer.beep_click(self.buzzerpin)	
	
	def function_ONcoldblock(self):
		self.lcdcoldblock.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		coldblock_output.coldblock_enabled = 1 
		buzzer.beep_click(self.buzzerpin)	
	
	def function_OFFcoldblock(self):
		self.lcdcoldblock.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		coldblock_output.coldblock_enabled = 0 
		buzzer.beep_click(self.buzzerpin)	
		
	def function_ONhotend(self):
		self.lcdHotend.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		hotend_output.hotend_enabled = 1
		buzzer.beep_click(self.buzzerpin) 	
	
	def function_OFFhotend(self):
		self.lcdHotend.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		hotend_output.hotend_enabled = 0
		buzzer.beep_click(self.buzzerpin) 	
		
	def function_motorStart(self):
		if(self.motorStart == 0):
			self.motorStart = 1
			#print("on")
			self.btnmotorStart.setStyleSheet("background-color: rgb(255,0,0);") #b,g,r format
			self.btnmotorStart.setText("Stop")
			stepper_output.motor_enabled = 1
		elif(self.motorStart == 1):
			self.motorStart = 0
			#print("off")
			self.btnmotorStart.setStyleSheet("background-color: rgb(0,255,0);")
			self.btnmotorStart.setText("Start")
			stepper_output.motor_enabled = 0
		buzzer.beep_click(self.buzzerpin)
		
	def function_Direction(self):
		if(stepper_output.motor_direction):
			self.btnDirection.setText("Reverse")
			stepper_output.motor_direction = 0
		else:
			self.btnDirection.setText("Forward")
			stepper_output.motor_direction = 1
		#print(stepper_output.motor_direction)
		buzzer.beep_click(self.buzzerpin)
	
	def function_Estop(self):
		try: 
			print("EStop - Activated")	
			#remember not to disable sensor reading
			aircon_output.aircon_enabled = 0 
			coldblock_output.coldblock_enabled = 0
			hotend_output.hotend_enabled = 0 
			stepper_output.motor_enabled = 0
			herkulex.servo_enabled = 0
			grovepi.analogWrite(self.peltierfanpin1,0)
			grovepi.analogWrite(self.peltierfanpin2,0)
			grovepi.ledCircle_off(self.ledcirclepin)
			time.sleep(0.1)
			self.peltier1.start(0)
			self.peltier2.start(0)
			self.heater.start(0)
			GPIO.output(self.motor_enable_pin,1) #set H to disable
			GPIO.output(self.motor_dir_pin,0) #set H to disable
			GPIO.output(self.motor_step_pin,0) #set H to disable
			print("Successful = Power down system")	
			buzzer.beep(self.buzzerpin,2)
		except Exception, e:
			print("Failed = Pls manual power down")
			print("Failed = Pls manual power down")	
			print("Failed = Pls manual power down")
			buzzer.beep_fail(self.buzzerpin)		
			print(str(e))

	def setupUi(self, labelWindow):
		labelWindow.setObjectName("labelWindow")
		labelWindow.resize(480, 728) #480, 800 offset 36, 740
		labelWindow.move(0,0)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(labelWindow.sizePolicy().hasHeightForWidth())
		labelWindow.setSizePolicy(sizePolicy)
		self.centralWidget = QtWidgets.QWidget(labelWindow)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
		self.centralWidget.setSizePolicy(sizePolicy)
		self.centralWidget.setObjectName("centralWidget")
		self.tabMenu = QtWidgets.QTabWidget(self.centralWidget)
		self.tabMenu.setGeometry(QtCore.QRect(0, 0, 481, 720))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.tabMenu.sizePolicy().hasHeightForWidth())
		self.tabMenu.setSizePolicy(sizePolicy)
		self.tabMenu.setObjectName("tabMenu")
		self.ControlTab = QtWidgets.QWidget()
		self.ControlTab.setObjectName("ControlTab")
		self.btnEstop = QtWidgets.QPushButton(self.ControlTab)
		self.btnEstop.setGeometry(QtCore.QRect(340, 470, 121, 150))
		font = QtGui.QFont()
		font.setPointSize(25)
		self.btnEstop.setFont(font)
		self.btnEstop.setDefault(True)
		self.btnEstop.setObjectName("btnEstop")
		self.boxSetTarget = QtWidgets.QGroupBox(self.ControlTab)
		self.boxSetTarget.setGeometry(QtCore.QRect(0, 0, 321, 720))
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.boxSetTarget.sizePolicy().hasHeightForWidth())
		self.boxSetTarget.setSizePolicy(sizePolicy)
		self.boxSetTarget.setObjectName("boxSetTarget")
		self.labelFilament = QtWidgets.QLabel(self.boxSetTarget)
		self.labelFilament.setGeometry(QtCore.QRect(10, 50, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setWeight(75)
		self.labelFilament.setFont(font)
		self.labelFilament.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFilament.setWordWrap(True)
		self.labelFilament.setObjectName("labelFilament")
		self.labelAircon = QtWidgets.QLabel(self.boxSetTarget)
		self.labelAircon.setGeometry(QtCore.QRect(10, 150, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setWeight(75)
		self.labelAircon.setFont(font)
		self.labelAircon.setAlignment(QtCore.Qt.AlignCenter)
		self.labelAircon.setWordWrap(True)
		self.labelAircon.setObjectName("labelAircon")
		self.labelColdblock = QtWidgets.QLabel(self.boxSetTarget)
		self.labelColdblock.setGeometry(QtCore.QRect(10, 260, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.labelColdblock.setFont(font)
		self.labelColdblock.setAlignment(QtCore.Qt.AlignCenter)
		self.labelColdblock.setWordWrap(True)
		self.labelColdblock.setObjectName("labelColdblock")
		self.labelHotend = QtWidgets.QLabel(self.boxSetTarget)
		self.labelHotend.setGeometry(QtCore.QRect(10, 370, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setWeight(75)
		self.labelHotend.setFont(font)
		self.labelHotend.setAlignment(QtCore.Qt.AlignCenter)
		self.labelHotend.setWordWrap(True)
		self.labelHotend.setObjectName("labelHotend")
		self.labelFeedrate = QtWidgets.QLabel(self.boxSetTarget)
		self.labelFeedrate.setGeometry(QtCore.QRect(10, 480, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(13)
		font.setBold(True)
		font.setWeight(75)
		self.labelFeedrate.setFont(font)
		self.labelFeedrate.setAlignment(QtCore.Qt.AlignCenter)
		self.labelFeedrate.setWordWrap(True)
		self.labelFeedrate.setObjectName("labelFeedrate")
		self.lcdFeedrate = QtWidgets.QLCDNumber(self.boxSetTarget)
		self.lcdFeedrate.setGeometry(QtCore.QRect(90, 460, 120, 100))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdFeedrate.setFont(font)
		self.lcdFeedrate.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdFeedrate.setAutoFillBackground(True)
		self.lcdFeedrate.setSmallDecimalPoint(False)
		self.lcdFeedrate.setDigitCount(5)
		self.lcdFeedrate.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdFeedrate.setProperty("value", 10.0)
		self.lcdFeedrate.setObjectName("lcdFeedrate")
		self.lcdFilament = QtWidgets.QLCDNumber(self.boxSetTarget)
		self.lcdFilament.setGeometry(QtCore.QRect(90, 20, 120, 100))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdFilament.setFont(font)
		self.lcdFilament.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdFilament.setAutoFillBackground(True)
		self.lcdFilament.setSmallDecimalPoint(False)
		self.lcdFilament.setDigitCount(5)
		self.lcdFilament.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdFilament.setProperty("value", 1.75)
		self.lcdFilament.setObjectName("lcdFilament")
		self.lcdcoldblock = QtWidgets.QLCDNumber(self.boxSetTarget)
		self.lcdcoldblock.setGeometry(QtCore.QRect(90, 240, 120, 100))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdcoldblock.setFont(font)
		self.lcdcoldblock.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdcoldblock.setAutoFillBackground(True)
		self.lcdcoldblock.setSmallDecimalPoint(False)
		self.lcdcoldblock.setDigitCount(5)
		self.lcdcoldblock.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdcoldblock.setProperty("value", 30.0)
		self.lcdcoldblock.setObjectName("lcdcoldblock")
		self.lcdAircon = QtWidgets.QLCDNumber(self.boxSetTarget)
		self.lcdAircon.setGeometry(QtCore.QRect(90, 130, 120, 100))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdAircon.setFont(font)
		self.lcdAircon.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdAircon.setAutoFillBackground(True)
		self.lcdAircon.setSmallDecimalPoint(False)
		self.lcdAircon.setDigitCount(5)
		self.lcdAircon.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdAircon.setProperty("value", 30.0)
		self.lcdAircon.setObjectName("lcdAircon")
		self.lcdHotend = QtWidgets.QLCDNumber(self.boxSetTarget)
		self.lcdHotend.setGeometry(QtCore.QRect(90, 350, 120, 100))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdHotend.setFont(font)
		self.lcdHotend.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdHotend.setAutoFillBackground(True)
		self.lcdHotend.setSmallDecimalPoint(False)
		self.lcdHotend.setDigitCount(5)
		self.lcdHotend.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdHotend.setProperty("value", 25.0)
		self.lcdHotend.setObjectName("lcdHotend")
		self.scrollFeedrate = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollFeedrate.setGeometry(QtCore.QRect(220, 460, 40, 100))
		self.scrollFeedrate.setAutoFillBackground(False)
		self.scrollFeedrate.setMinimum(1)
		self.scrollFeedrate.setMaximum(500)
		self.scrollFeedrate.setPageStep(1)
		self.scrollFeedrate.setProperty("value", 10)
		self.scrollFeedrate.setSliderPosition(10)
		self.scrollFeedrate.setOrientation(QtCore.Qt.Vertical)
		self.scrollFeedrate.setInvertedAppearance(False)
		self.scrollFeedrate.setInvertedControls(True)
		self.scrollFeedrate.setObjectName("scrollFeedrate")
		self.scrollHotend = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollHotend.setGeometry(QtCore.QRect(220, 350, 40, 100))
		self.scrollHotend.setAutoFillBackground(False)
		self.scrollHotend.setMinimum(250)
		self.scrollHotend.setMaximum(1600)
		self.scrollHotend.setPageStep(1)
		self.scrollHotend.setSliderPosition(250)
		self.scrollHotend.setOrientation(QtCore.Qt.Vertical)
		self.scrollHotend.setInvertedAppearance(False)
		self.scrollHotend.setInvertedControls(True)
		self.scrollHotend.setObjectName("scrollHotend")
		self.scrollColdblock = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollColdblock.setGeometry(QtCore.QRect(220, 240, 40, 100))
		self.scrollColdblock.setAutoFillBackground(False)
		self.scrollColdblock.setMinimum(150)
		self.scrollColdblock.setMaximum(300)
		self.scrollColdblock.setPageStep(1)
		self.scrollColdblock.setSliderPosition(300)
		self.scrollColdblock.setOrientation(QtCore.Qt.Vertical)
		self.scrollColdblock.setInvertedAppearance(False)
		self.scrollColdblock.setInvertedControls(True)
		self.scrollColdblock.setObjectName("scrollColdblock")
		self.scrollAircon = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollAircon.setGeometry(QtCore.QRect(220, 130, 40, 100))
		self.scrollAircon.setAutoFillBackground(False)
		self.scrollAircon.setMinimum(150)
		self.scrollAircon.setMaximum(300)
		self.scrollAircon.setPageStep(1)
		self.scrollAircon.setSliderPosition(300)
		self.scrollAircon.setOrientation(QtCore.Qt.Vertical)
		self.scrollAircon.setInvertedAppearance(False)
		self.scrollAircon.setInvertedControls(True)
		self.scrollAircon.setObjectName("scrollAircon")
		self.scrollFilament = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollFilament.setGeometry(QtCore.QRect(220, 20, 40, 100))
		self.scrollFilament.setAutoFillBackground(False)
		self.scrollFilament.setMinimum(130)
		self.scrollFilament.setMaximum(210)
		self.scrollFilament.setPageStep(1)
		self.scrollFilament.setSliderPosition(175)
		self.scrollFilament.setOrientation(QtCore.Qt.Vertical)
		self.scrollFilament.setInvertedAppearance(False)
		self.scrollFilament.setInvertedControls(True)
		self.scrollFilament.setObjectName("scrollFilament")
		self.btnONAircon = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnONAircon.setGeometry(QtCore.QRect(260, 140, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnONAircon.setFont(font)
		self.btnONAircon.setObjectName("btnONAircon")
		self.btnDirection = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnDirection.setGeometry(QtCore.QRect(170, 570, 140, 50))
		font = QtGui.QFont()
		font.setPointSize(25)
		self.btnDirection.setFont(font)
		self.btnDirection.setObjectName("btnDirection")
		self.btnmotorStart = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnmotorStart.setGeometry(QtCore.QRect(10, 570, 140, 50))
		font = QtGui.QFont()
		font.setPointSize(25)
		self.btnmotorStart.setFont(font)
		self.btnmotorStart.setAutoDefault(False)
		self.btnmotorStart.setDefault(False)
		self.btnmotorStart.setFlat(False)
		self.btnmotorStart.setObjectName("btnmotorStart")
		self.btnOFFAircon = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnOFFAircon.setGeometry(QtCore.QRect(260, 180, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnOFFAircon.setFont(font)
		self.btnOFFAircon.setObjectName("btnOFFAircon")
		self.btnONColdblock = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnONColdblock.setGeometry(QtCore.QRect(260, 250, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnONColdblock.setFont(font)
		self.btnONColdblock.setObjectName("btnONColdblock")
		self.btnOFFColdblock = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnOFFColdblock.setGeometry(QtCore.QRect(260, 290, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnOFFColdblock.setFont(font)
		self.btnOFFColdblock.setObjectName("btnOFFColdblock")
		self.btnONHotend = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnONHotend.setGeometry(QtCore.QRect(260, 360, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnONHotend.setFont(font)
		self.btnONHotend.setObjectName("btnONHotend")
		self.btnOFFHotend = QtWidgets.QPushButton(self.boxSetTarget)
		self.btnOFFHotend.setGeometry(QtCore.QRect(260, 400, 50, 40))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnOFFHotend.setFont(font)
		self.btnOFFHotend.setObjectName("btnOFFHotend")
		self.boxSensersReading = QtWidgets.QGroupBox(self.ControlTab)
		self.boxSensersReading.setGeometry(QtCore.QRect(320, 0, 151, 461))
		self.boxSensersReading.setObjectName("boxSensersReading")
		self.labelReadAircon = QtWidgets.QLabel(self.boxSensersReading)
		self.labelReadAircon.setGeometry(QtCore.QRect(30, 160, 100, 50))
		font = QtGui.QFont()
		font.setPointSize(23)
		font.setBold(True)
		font.setWeight(75)
		self.labelReadAircon.setFont(font)
		self.labelReadAircon.setAlignment(QtCore.Qt.AlignCenter)
		self.labelReadAircon.setObjectName("labelReadAircon")
		self.labelReadColdblock = QtWidgets.QLabel(self.boxSensersReading)
		self.labelReadColdblock.setGeometry(QtCore.QRect(30, 270, 100, 50))
		font = QtGui.QFont()
		font.setPointSize(23)
		font.setBold(True)
		font.setWeight(75)
		self.labelReadColdblock.setFont(font)
		self.labelReadColdblock.setAlignment(QtCore.Qt.AlignCenter)
		self.labelReadColdblock.setObjectName("labelReadColdblock")
		self.labelReadHotend = QtWidgets.QLabel(self.boxSensersReading)
		self.labelReadHotend.setGeometry(QtCore.QRect(30, 380, 100, 50))
		font = QtGui.QFont()
		font.setPointSize(23)
		font.setBold(True)
		font.setWeight(75)
		self.labelReadHotend.setFont(font)
		self.labelReadHotend.setAlignment(QtCore.Qt.AlignCenter)
		self.labelReadHotend.setObjectName("labelReadHotend")
		self.tabMenu.addTab(self.ControlTab, "")
		self.CameraTab = QtWidgets.QWidget()
		self.CameraTab.setObjectName("CameraTab")
		self.labelPic1 = QtWidgets.QLabel(self.CameraTab)
		self.labelPic1.setGeometry(QtCore.QRect(10, 10, 100, 400))
		self.labelPic1.setText("")
		self.labelPic1.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image.jpg"))
		self.labelPic1.setObjectName("labelPic1")
		self.labelPic2 = QtWidgets.QLabel(self.CameraTab)
		self.labelPic2.setGeometry(QtCore.QRect(130, 10, 100, 400))
		self.labelPic2.setText("")
		self.labelPic2.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image.jpg"))
		self.labelPic2.setObjectName("labelPic2")
		self.labelPic3 = QtWidgets.QLabel(self.CameraTab)
		self.labelPic3.setGeometry(QtCore.QRect(250, 10, 100, 400))
		self.labelPic3.setText("")
		self.labelPic3.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image.jpg"))
		self.labelPic3.setObjectName("labelPic3")
		self.labelPic4 = QtWidgets.QLabel(self.CameraTab)
		self.labelPic4.setGeometry(QtCore.QRect(370, 10, 100, 400))
		self.labelPic4.setText("")
		self.labelPic4.setPixmap(QtGui.QPixmap("/home/pi/Desktop/MyCode/image.jpg"))
		self.labelPic4.setObjectName("labelPic4")
		self.scrollControl1 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl1.setGeometry(QtCore.QRect(30, 440, 20, 200))
		self.scrollControl1.setMaximum(100)
		self.scrollControl1.setProperty("value", 50)
		self.scrollControl1.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl1.setInvertedControls(False)
		self.scrollControl1.setObjectName("scrollControl1")
		self.scrollControl2 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl2.setGeometry(QtCore.QRect(80, 440, 20, 200))
		self.scrollControl2.setMaximum(100)
		self.scrollControl2.setProperty("value", 50)
		self.scrollControl2.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl2.setInvertedControls(False)
		self.scrollControl2.setObjectName("scrollControl2")
		self.scrollControl3 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl3.setGeometry(QtCore.QRect(130, 440, 20, 200))
		self.scrollControl3.setMaximum(100)
		self.scrollControl3.setProperty("value", 50)
		self.scrollControl3.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl3.setInvertedControls(False)
		self.scrollControl3.setObjectName("scrollControl3")
		self.scrollControl4 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl4.setGeometry(QtCore.QRect(180, 440, 20, 200))
		self.scrollControl4.setMaximum(100)
		self.scrollControl4.setProperty("value", 50)
		self.scrollControl4.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl4.setInvertedControls(False)
		self.scrollControl4.setObjectName("scrollControl4")
		self.scrollControl5 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl5.setGeometry(QtCore.QRect(230, 440, 20, 200))
		self.scrollControl5.setMaximum(100)
		self.scrollControl5.setProperty("value", 50)
		self.scrollControl5.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl5.setInvertedControls(False)
		self.scrollControl5.setObjectName("scrollControl5")
		self.scrollControl6 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl6.setGeometry(QtCore.QRect(280, 440, 20, 200))
		self.scrollControl6.setMaximum(100)
		self.scrollControl6.setProperty("value", 50)
		self.scrollControl6.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl6.setInvertedControls(False)
		self.scrollControl6.setObjectName("scrollControl6")
		self.scrollControl7 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl7.setGeometry(QtCore.QRect(330, 440, 20, 200))
		self.scrollControl7.setMaximum(100)
		self.scrollControl7.setProperty("value", 50)
		self.scrollControl7.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl7.setInvertedControls(False)
		self.scrollControl7.setObjectName("scrollControl7")
		self.scrollControl8 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl8.setGeometry(QtCore.QRect(380, 440, 20, 200))
		self.scrollControl8.setMaximum(100)
		self.scrollControl8.setProperty("value", 50)
		self.scrollControl8.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl8.setInvertedControls(False)
		self.scrollControl8.setObjectName("scrollControl8")
		self.scrollControl9 = QtWidgets.QScrollBar(self.CameraTab)
		self.scrollControl9.setGeometry(QtCore.QRect(430, 440, 20, 200))
		self.scrollControl9.setMaximum(100)
		self.scrollControl9.setProperty("value", 50)
		self.scrollControl9.setOrientation(QtCore.Qt.Vertical)
		self.scrollControl9.setInvertedControls(False)
		self.scrollControl9.setObjectName("scrollControl9")
		self.labelControl1 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl1.setGeometry(QtCore.QRect(10, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl1.setFont(font)
		self.labelControl1.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl1.setWordWrap(True)
		self.labelControl1.setObjectName("labelControl1")
		self.labelControl2 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl2.setGeometry(QtCore.QRect(60, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl2.setFont(font)
		self.labelControl2.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl2.setWordWrap(True)
		self.labelControl2.setObjectName("labelControl2")
		self.labelControl3 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl3.setGeometry(QtCore.QRect(110, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl3.setFont(font)
		self.labelControl3.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl3.setWordWrap(True)
		self.labelControl3.setObjectName("labelControl3")
		self.labelControl4 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl4.setGeometry(QtCore.QRect(160, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl4.setFont(font)
		self.labelControl4.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl4.setWordWrap(True)
		self.labelControl4.setObjectName("labelControl4")
		self.labelControl5 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl5.setGeometry(QtCore.QRect(210, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl5.setFont(font)
		self.labelControl5.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl5.setWordWrap(True)
		self.labelControl5.setObjectName("labelControl5")
		self.labelControl6 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl6.setGeometry(QtCore.QRect(260, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl6.setFont(font)
		self.labelControl6.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl6.setWordWrap(True)
		self.labelControl6.setObjectName("labelControl6")
		self.labelControl7 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl7.setGeometry(QtCore.QRect(310, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl7.setFont(font)
		self.labelControl7.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl7.setWordWrap(True)
		self.labelControl7.setObjectName("labelControl7")
		self.labelControl8 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl8.setGeometry(QtCore.QRect(360, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl8.setFont(font)
		self.labelControl8.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl8.setWordWrap(True)
		self.labelControl8.setObjectName("labelControl8")
		self.labelControl9 = QtWidgets.QLabel(self.CameraTab)
		self.labelControl9.setGeometry(QtCore.QRect(410, 640, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelControl9.setFont(font)
		self.labelControl9.setAlignment(QtCore.Qt.AlignCenter)
		self.labelControl9.setWordWrap(True)
		self.labelControl9.setObjectName("labelControl9")
		self.labelCValue1 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue1.setGeometry(QtCore.QRect(10, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue1.setFont(font)
		self.labelCValue1.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue1.setWordWrap(True)
		self.labelCValue1.setObjectName("labelCValue1")
		self.labelCValue2 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue2.setGeometry(QtCore.QRect(60, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue2.setFont(font)
		self.labelCValue2.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue2.setWordWrap(True)
		self.labelCValue2.setObjectName("labelCValue2")
		self.labelCValue3 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue3.setGeometry(QtCore.QRect(110, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue3.setFont(font)
		self.labelCValue3.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue3.setWordWrap(True)
		self.labelCValue3.setObjectName("labelCValue3")
		self.labelCValue4 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue4.setGeometry(QtCore.QRect(160, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue4.setFont(font)
		self.labelCValue4.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue4.setWordWrap(True)
		self.labelCValue4.setObjectName("labelCValue4")
		self.labelCValue5 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue5.setGeometry(QtCore.QRect(210, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue5.setFont(font)
		self.labelCValue5.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue5.setWordWrap(True)
		self.labelCValue5.setObjectName("labelCValue5")
		self.labelCValue6 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue6.setGeometry(QtCore.QRect(260, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue6.setFont(font)
		self.labelCValue6.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue6.setWordWrap(True)
		self.labelCValue6.setObjectName("labelCValue6")
		self.labelCValue7 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue7.setGeometry(QtCore.QRect(310, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue7.setFont(font)
		self.labelCValue7.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue7.setWordWrap(True)
		self.labelCValue7.setObjectName("labelCValue7")
		self.labelCValue8 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue8.setGeometry(QtCore.QRect(360, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue8.setFont(font)
		self.labelCValue8.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue8.setWordWrap(True)
		self.labelCValue8.setObjectName("labelCValue8")
		self.labelCValue9 = QtWidgets.QLabel(self.CameraTab)
		self.labelCValue9.setGeometry(QtCore.QRect(410, 410, 60, 20))
		font = QtGui.QFont()
		font.setPointSize(7)
		font.setBold(True)
		font.setWeight(75)
		self.labelCValue9.setFont(font)
		self.labelCValue9.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCValue9.setWordWrap(True)
		self.labelCValue9.setObjectName("labelCValue9")
		self.tabMenu.addTab(self.CameraTab, "")
		labelWindow.setCentralWidget(self.centralWidget)
		self.menuBar = QtWidgets.QMenuBar(labelWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 480, 27))
		self.menuBar.setObjectName("menuBar")
		self.menuFile = QtWidgets.QMenu(self.menuBar)
		self.menuFile.setObjectName("menuFile")
		labelWindow.setMenuBar(self.menuBar)
		self.mainToolBar = QtWidgets.QToolBar(labelWindow)
		self.mainToolBar.setEnabled(False)
		self.mainToolBar.setObjectName("mainToolBar")
		labelWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
		self.statusBar = QtWidgets.QStatusBar(labelWindow)
		self.statusBar.setObjectName("statusBar")
		labelWindow.setStatusBar(self.statusBar)
		self.actionExit = QtWidgets.QAction(labelWindow)
		self.actionExit.setObjectName("actionExit")
		self.menuFile.addAction(self.actionExit)
		self.menuBar.addAction(self.menuFile.menuAction())

		self.retranslateUi(labelWindow)
		self.tabMenu.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(labelWindow)
		
		#My code for functions
		self.btnEstop.clicked.connect(self.function_Estop)
		self.btnEstop.setStyleSheet("background-color: rgb(255,0,0);")
		self.btnONAircon.clicked.connect(self.function_ONaircon)
		self.btnOFFAircon.clicked.connect(self.function_OFFaircon)
		self.btnONColdblock.clicked.connect(self.function_ONcoldblock)
		self.btnOFFColdblock.clicked.connect(self.function_OFFcoldblock)
		self.btnONHotend.clicked.connect(self.function_ONhotend)
		self.btnOFFHotend.clicked.connect(self.function_OFFhotend)
		self.btnmotorStart.clicked.connect(self.function_motorStart)
		self.btnmotorStart.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		self.btnDirection.clicked.connect(self.function_Direction)
		self.scrollFilament.valueChanged.connect(self.function_scrollFilament)
		self.scrollAircon.valueChanged.connect(self.function_scrollAircon)
		self.scrollColdblock.valueChanged.connect(self.function_scrollColdblock)
		self.scrollHotend.valueChanged.connect(self.function_scrollHotend)
		self.scrollFeedrate.valueChanged.connect(self.function_scrollFeedrate)
		self.actionExit.triggered.connect(self.function_Exit)
		self.lcdAircon.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		self.lcdcoldblock.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		self.lcdHotend.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		self.lcdFilament.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		self.lcdFeedrate.setStyleSheet("background-color: rgb(255,255,255);") #b,g,r format
		self.scrollControl1.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl2.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl3.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl4.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl5.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl6.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl7.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl8.valueChanged.connect(self.function_refreshCameravale)
		self.scrollControl9.valueChanged.connect(self.function_refreshCameravale)
		self.turn_on_selected_LED()
		
		#Update sensor display thread
		updateLabel = threading.Thread(target=self.updateTemperaturelabel)
		updateLabel.daemon = True
		updateLabel.start()
		
		self.function_refreshCameravale()
		
	def retranslateUi(self, labelWindow):
		_translate = QtCore.QCoreApplication.translate
		labelWindow.setWindowTitle(_translate("labelWindow", "The Extruder"))
		self.btnEstop.setText(_translate("labelWindow", "E-Stop"))
		self.boxSetTarget.setTitle(_translate("labelWindow", "User Input and Set Target"))
		self.labelFilament.setText(_translate("labelWindow", "Filament Diameter"))
		self.labelAircon.setText(_translate("labelWindow", "Aircon"))
		self.labelColdblock.setText(_translate("labelWindow", "ColdBlock"))
		self.labelHotend.setText(_translate("labelWindow", "HotEnd"))
		self.labelFeedrate.setText(_translate("labelWindow", "Feedrate"))
		self.btnONAircon.setText(_translate("labelWindow", "On"))
		self.btnDirection.setText(_translate("labelWindow", "Forward"))
		self.btnmotorStart.setText(_translate("labelWindow", "Start"))
		self.btnOFFAircon.setText(_translate("labelWindow", "Off"))
		self.btnONColdblock.setText(_translate("labelWindow", "On"))
		self.btnOFFColdblock.setText(_translate("labelWindow", "Off"))
		self.btnONHotend.setText(_translate("labelWindow", "On"))
		self.btnOFFHotend.setText(_translate("labelWindow", "Off"))
		self.boxSensersReading.setTitle(_translate("labelWindow", "Sensors Reading"))
		self.labelReadAircon.setText(_translate("labelWindow", "30.0C"))
		self.labelReadColdblock.setText(_translate("labelWindow", "30.0C"))
		self.labelReadHotend.setText(_translate("labelWindow", "30.0C"))
		self.tabMenu.setTabText(self.tabMenu.indexOf(self.ControlTab), _translate("labelWindow", "Control"))
		self.labelControl1.setText(_translate("labelWindow", "Crtl1"))
		self.labelControl2.setText(_translate("labelWindow", "Crtl2"))
		self.labelControl3.setText(_translate("labelWindow", "Crtl3"))
		self.labelControl4.setText(_translate("labelWindow", "Crtl4"))
		self.labelControl5.setText(_translate("labelWindow", "Crtl5"))
		self.labelControl6.setText(_translate("labelWindow", "Crtl6"))
		self.labelControl7.setText(_translate("labelWindow", "Crtl7"))
		self.labelControl8.setText(_translate("labelWindow", "Ctrl8"))
		self.labelControl9.setText(_translate("labelWindow", "Crtl9"))
		self.labelCValue1.setText(_translate("labelWindow", "Val1"))
		self.labelCValue2.setText(_translate("labelWindow", "Val2"))
		self.labelCValue3.setText(_translate("labelWindow", "Val3"))
		self.labelCValue4.setText(_translate("labelWindow", "Val4"))
		self.labelCValue5.setText(_translate("labelWindow", "Val5"))
		self.labelCValue6.setText(_translate("labelWindow", "Val6"))
		self.labelCValue7.setText(_translate("labelWindow", "Val7"))
		self.labelCValue8.setText(_translate("labelWindow", "Val8"))
		self.labelCValue9.setText(_translate("labelWindow", "Val9"))
		self.tabMenu.setTabText(self.tabMenu.indexOf(self.CameraTab), _translate("labelWindow", "Camera"))
		self.menuFile.setTitle(_translate("labelWindow", "File"))
		self.actionExit.setText(_translate("labelWindow", "Exit"))

'''
if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(function_cleanup)
    labelWindow = QtWidgets.QMainWindow()
    ui = Ui_labelWindow()
    ui.setupUi(labelWindow)
    labelWindow.show()
    sys.exit(app.exec_())
'''
