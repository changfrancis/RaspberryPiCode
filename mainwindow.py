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
		self.cameraStart = 0
		self.CameraPID = 0
		self.buzzerpin = _buzzerpin
		self.ledcirclepin = _ledcirclepin
		
	def updateTemperaturelabel(self):
		while True:
			self.labelReadAircon.setText("{:.1f} C".format(sensors.adc1_temp_cur))
			self.labelReadColdblock.setText("{:.1f} C".format(sensors.adc2_temp_cur))
			self.labelReadHotend.setText("{:.1f} C".format(sensors.adc3_temp_cur))
			#update image
			try:
				if(sensors.adc3_temp_cur >= 165.0):
					buzzer.beep(self.buzzerpin,2)
				if(self.cameraStart):
					self.labelCameraview.setPixmap(QtGui.QPixmap(camera_linedetection.imgPath01))
					self.lcdOutputDia1.setProperty("value", camera_linedetection.OutputDia1)
					self.lcdOutputDia2.setProperty("value", camera_linedetection.OutputDia2)
					self.lcdOutputDia3.setProperty("value", camera_linedetection.OutputDia3)
				else:
					self.labelCameraview.setPixmap(QtGui.QPixmap("../../../../../"))
			except Exception, e:
				print(str(e))
			time.sleep(0.30) #update rate is set to x seconds
	
	def function_Exit(self):
		print("Exiting...type2\n\n\n")
		buzzer.beep_click(self.buzzerpin)
		self.function_Estop()
		grovepi.analogWrite(self.peltierfanpin1,0) #aircon, 0-255
		grovepi.analogWrite(self.peltierfanpin2,0) #coldblock, 0-255
		grovepi.ledCircle_off(self.ledcirclepin)
		herkulex.alive = 0
		camera_linedetection.alive = 0
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
		time.sleep(1.0)
		sys.exit()
		
	def function_cameraStart(self):
		if(self.cameraStart == 0):
			self.cameraStart = 1
			#print("on")
			self.btnCamera.setStyleSheet("background-color: rgb(255,0,0);") #b,g,r format
			self.btnCamera.setText("Camera Off")
			camera_linedetection.camera_enabled = 1
			#turn lights on
			grovepi.ledCircle_init(self.ledcirclepin)
			time.sleep(0.2)
			grovepi.ledCircle_on(self.ledcirclepin) #intensity is 0-255
			time.sleep(0.15)
		elif(self.cameraStart == 1):
			self.cameraStart = 0
			#print("off")
			self.btnCamera.setStyleSheet("background-color: rgb(0,255,0);")
			self.btnCamera.setText("Camera On")
			camera_linedetection.camera_enabled = 0
			#turn listopghts off
			#grovepi.ledCircleintensity(self.ledcirclepin, buf)
			grovepi.ledCircle_off(self.ledcirclepin) #intensity is 0-255
			time.sleep(0.15)
		buzzer.beep_click(self.buzzerpin)
		
	def function_cameraPID(self):
		if(self.CameraPID == 0 and stepper_output.motor_enabled and camera_linedetection.camera_enabled):
			self.CameraPID = 1
			#print("on")
			self.btnCameraPID.setStyleSheet("background-color: rgb(255,0,0);") #b,g,r format
			self.btnCameraPID.setText("PID Disable")
			stepper_output.cameraP = self.spinCameraP.value()
			stepper_output.cameraI = self.spinCameraI.value()
			stepper_output.cameraD = self.spinCameraD.value()
			stepper_output.cameraPIDsetpoint = self.spinTargetdia.value()
			camera_linedetection.cameraPID_enabled = 1
		elif(self.CameraPID == 1):
			self.CameraPID = 0
			#print("off")
			self.btnCameraPID.setStyleSheet("background-color: rgb(0,255,0);")
			self.btnCameraPID.setText("PID Enable")
			camera_linedetection.cameraPID_enabled = 0
		else:
			print("Check - Stepper not started ?")
		buzzer.beep_scroll(self.buzzerpin)
	
	def function_cameraPIDValue(self):
		buf1 = self.spinCameraP.value()
		buf2 = self.spinCameraI.value()
		buf3 = self.spinCameraD.value()
		stepper_output.cameraP = buf1
		stepper_output.cameraI = buf2
		stepper_output.cameraD = buf3
		#print(buf1)
		#print(buf2)
		#print(buf3)
		buzzer.beep_scroll(self.buzzerpin)
		
	def function_nozzledia(self):
		buf = self.spinTargetdia.value()
		#print(buf)
		stepper_output.cameraPIDsetpoint = buf
		buzzer.beep_scroll(self.buzzerpin)	
		
	def function_cameraedgesigma(self):
		buf = self.spinEdgesigma.value()/100
		camera_linedetection.edgesigma = buf
		#print(camera_linedetection.edgesigma)
		buzzer.beep_scroll(self.buzzerpin)
	
	def function_line_length_gap(self):
		buf1 = self.spinLinegap.value()
		buf2 = self.spinLinelength.value()
		camera_linedetection.LineGap = buf1
		camera_linedetection.LineLength = buf2
		#print(camera_linedetection.LineGap)
		#print(camera_linedetection.LineLength)
		buzzer.beep_scroll(self.buzzerpin)
		
	def turn_on_selected_LED(self):
		grovepi.ledCircle_init(self.ledcirclepin)
		time.sleep(0.2)
		grovepi.ledCircle_on(self.ledcirclepin) #intensity is 0-255
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
			self.btnmotorStart.setText("Motor Stop")
			stepper_output.motor_enabled = 1
		elif(self.motorStart == 1):
			self.motorStart = 0
			#print("off")
			self.btnmotorStart.setStyleSheet("background-color: rgb(0,255,0);")
			self.btnmotorStart.setText("Motor Start")
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
			camera_linedetection.camera_enabled = 0
			herkulex.servo_enabled = 0
			grovepi.analogWrite(self.peltierfanpin1,0)
			grovepi.analogWrite(self.peltierfanpin2,0)
			#grovepi.ledCircle_off(self.ledcirclepin)
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
			print("--- Failed = Pls manual power down ---\n")
			print("--- Failed = Pls manual power down ---\n")	
			print("--- Failed = Pls manual power down ---\n")
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
		self.lcdFeedrate.setProperty("value", 5.0)
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
		self.scrollFeedrate.setMaximum(50)
		self.scrollFeedrate.setPageStep(1)
		self.scrollFeedrate.setProperty("value", 5)
		self.scrollFeedrate.setSliderPosition(5)
		self.scrollFeedrate.setOrientation(QtCore.Qt.Vertical)
		self.scrollFeedrate.setInvertedAppearance(False)
		self.scrollFeedrate.setInvertedControls(True)
		self.scrollFeedrate.setObjectName("scrollFeedrate")
		self.scrollHotend = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollHotend.setGeometry(QtCore.QRect(220, 350, 40, 100))
		self.scrollHotend.setAutoFillBackground(False)
		self.scrollHotend.setMinimum(250)
		self.scrollHotend.setMaximum(1600)
		self.scrollHotend.setPageStep(10)
		self.scrollHotend.setSingleStep(10)
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
		self.scrollColdblock.setPageStep(10)
		self.scrollColdblock.setSingleStep(10)
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
		self.scrollAircon.setPageStep(10)
		self.scrollAircon.setSingleStep(10)
		self.scrollAircon.setSliderPosition(300)
		self.scrollAircon.setOrientation(QtCore.Qt.Vertical)
		self.scrollAircon.setInvertedAppearance(False)
		self.scrollAircon.setInvertedControls(True)
		self.scrollAircon.setObjectName("scrollAircon")
		self.scrollFilament = QtWidgets.QScrollBar(self.boxSetTarget)
		self.scrollFilament.setGeometry(QtCore.QRect(220, 20, 40, 100))
		self.scrollFilament.setAutoFillBackground(False)
		self.scrollFilament.setMinimum(140)
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
		font.setPointSize(18)
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
		#Camera Tab
		self.CameraTab = QtWidgets.QWidget()
		self.CameraTab.setObjectName("CameraTab")
		self.boxOutputfilament = QtWidgets.QGroupBox(self.CameraTab)
		self.boxOutputfilament.setGeometry(QtCore.QRect(0, 0, 241, 261))
		self.boxOutputfilament.setObjectName("boxOutputfilament")
		self.labelOutputDia1 = QtWidgets.QLabel(self.boxOutputfilament)
		self.labelOutputDia1.setGeometry(QtCore.QRect(10, 30, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.labelOutputDia1.setFont(font)
		self.labelOutputDia1.setAlignment(QtCore.Qt.AlignCenter)
		self.labelOutputDia1.setWordWrap(True)
		self.labelOutputDia1.setObjectName("labelOutputDia1")
		self.lcdOutputDia1 = QtWidgets.QLCDNumber(self.boxOutputfilament)
		self.lcdOutputDia1.setGeometry(QtCore.QRect(99, 20, 121, 71))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdOutputDia1.setFont(font)
		self.lcdOutputDia1.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdOutputDia1.setAutoFillBackground(True)
		self.lcdOutputDia1.setSmallDecimalPoint(False)
		self.lcdOutputDia1.setDigitCount(5)
		self.lcdOutputDia1.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdOutputDia1.setProperty("value", 12.3)
		self.lcdOutputDia1.setObjectName("lcdOutputDia1")
		self.labelOutputDia2 = QtWidgets.QLabel(self.boxOutputfilament)
		self.labelOutputDia2.setGeometry(QtCore.QRect(11, 110, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.labelOutputDia2.setFont(font)
		self.labelOutputDia2.setAlignment(QtCore.Qt.AlignCenter)
		self.labelOutputDia2.setWordWrap(True)
		self.labelOutputDia2.setObjectName("labelOutputDia2")
		self.lcdOutputDia2 = QtWidgets.QLCDNumber(self.boxOutputfilament)
		self.lcdOutputDia2.setGeometry(QtCore.QRect(100, 100, 121, 71))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdOutputDia2.setFont(font)
		self.lcdOutputDia2.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdOutputDia2.setAutoFillBackground(True)
		self.lcdOutputDia2.setSmallDecimalPoint(False)
		self.lcdOutputDia2.setDigitCount(5)
		self.lcdOutputDia2.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdOutputDia2.setProperty("value", 12.3)
		self.lcdOutputDia2.setObjectName("lcdOutputDia2")
		self.lcdOutputDia3 = QtWidgets.QLCDNumber(self.boxOutputfilament)
		self.lcdOutputDia3.setGeometry(QtCore.QRect(99, 180, 121, 71))
		font = QtGui.QFont()
		font.setFamily("MS Shell Dlg 2")
		self.lcdOutputDia3.setFont(font)
		self.lcdOutputDia3.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.lcdOutputDia3.setAutoFillBackground(True)
		self.lcdOutputDia3.setSmallDecimalPoint(False)
		self.lcdOutputDia3.setDigitCount(5)
		self.lcdOutputDia3.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
		self.lcdOutputDia3.setProperty("value", 12.3)
		self.lcdOutputDia3.setObjectName("lcdOutputDia3")
		self.labelOutputDia3 = QtWidgets.QLabel(self.boxOutputfilament)
		self.labelOutputDia3.setGeometry(QtCore.QRect(10, 190, 80, 50))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		self.labelOutputDia3.setFont(font)
		self.labelOutputDia3.setAlignment(QtCore.Qt.AlignCenter)
		self.labelOutputDia3.setWordWrap(True)
		self.labelOutputDia3.setObjectName("labelOutputDia3")
		self.boxCameraview = QtWidgets.QGroupBox(self.CameraTab)
		self.boxCameraview.setGeometry(QtCore.QRect(0, 260, 241, 431))
		self.boxCameraview.setObjectName("boxCameraview")
		self.labelCameraview = QtWidgets.QLabel(self.boxCameraview)
		self.labelCameraview.setGeometry(QtCore.QRect(5, 20, 225, 400))
		self.labelCameraview.setText("")
		self.labelCameraview.setPixmap(QtGui.QPixmap("../../../../../"))
		self.labelCameraview.setScaledContents(True)
		self.labelCameraview.setObjectName("labelCameraview")
		self.boxCameracontol = QtWidgets.QGroupBox(self.CameraTab)
		self.boxCameracontol.setGeometry(QtCore.QRect(250, 0, 221, 691))
		self.boxCameracontol.setObjectName("boxCameracontol")
		self.spinTargetdia = QtWidgets.QSpinBox(self.boxCameracontol)
		self.spinTargetdia.setGeometry(QtCore.QRect(100, 20, 111, 81))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.spinTargetdia.setFont(font)
		self.spinTargetdia.setMinimum(10)
		self.spinTargetdia.setMaximum(80)
		self.spinTargetdia.setSingleStep(1)
		self.spinTargetdia.setProperty("value", 40)
		self.spinTargetdia.setObjectName("spinTargetdia")
		self.labelCameralight = QtWidgets.QLabel(self.boxCameracontol)
		self.labelCameralight.setGeometry(QtCore.QRect(10, 20, 81, 81))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelCameralight.setFont(font)
		self.labelCameralight.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCameralight.setWordWrap(True)
		self.labelCameralight.setObjectName("labelCameralight")
		self.labelLinelength = QtWidgets.QLabel(self.boxCameracontol)
		self.labelLinelength.setGeometry(QtCore.QRect(10, 200, 81, 81))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelLinelength.setFont(font)
		self.labelLinelength.setAlignment(QtCore.Qt.AlignCenter)
		self.labelLinelength.setWordWrap(True)
		self.labelLinelength.setObjectName("labelLinelength")
		self.labelEdgesigma = QtWidgets.QLabel(self.boxCameracontol)
		self.labelEdgesigma.setGeometry(QtCore.QRect(10, 110, 81, 71))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelEdgesigma.setFont(font)
		self.labelEdgesigma.setAlignment(QtCore.Qt.AlignCenter)
		self.labelEdgesigma.setWordWrap(True)
		self.labelEdgesigma.setObjectName("labelEdgesigma")
		self.spinEdgesigma = QtWidgets.QDoubleSpinBox(self.boxCameracontol)
		self.spinEdgesigma.setGeometry(QtCore.QRect(100, 110, 111, 81))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.spinEdgesigma.setFont(font)
		self.spinEdgesigma.setMinimum(0.0)
		self.spinEdgesigma.setMaximum(100.0)
		self.spinEdgesigma.setSingleStep(1)
		self.spinEdgesigma.setProperty("value", 33)
		self.spinEdgesigma.setObjectName("spinEdgesigma")
		self.btnCamera = QtWidgets.QPushButton(self.boxCameracontol)
		self.btnCamera.setGeometry(QtCore.QRect(20, 500, 91, 81))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(False)
		font.setWeight(50)
		self.btnCamera.setFont(font)
		self.btnCamera.setObjectName("btnCamera")
		self.spinLinelength = QtWidgets.QSpinBox(self.boxCameracontol)
		self.spinLinelength.setGeometry(QtCore.QRect(100, 201, 111, 81))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.spinLinelength.setFont(font)
		self.spinLinelength.setMaximum(1000)
		self.spinLinelength.setSingleStep(5)
		self.spinLinelength.setProperty("value", 500)
		self.spinLinelength.setObjectName("spinLinelength")
		self.spinLinegap = QtWidgets.QSpinBox(self.boxCameracontol)
		self.spinLinegap.setGeometry(QtCore.QRect(100, 291, 111, 81))
		font = QtGui.QFont()
		font.setPointSize(22)
		self.spinLinegap.setFont(font)
		self.spinLinegap.setMaximum(1000)
		self.spinLinegap.setSingleStep(5)
		self.spinLinegap.setProperty("value", 300)
		self.spinLinegap.setObjectName("spinLinegap")
		self.labelLinegap = QtWidgets.QLabel(self.boxCameracontol)
		self.labelLinegap.setGeometry(QtCore.QRect(10, 290, 81, 81))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelLinegap.setFont(font)
		self.labelLinegap.setAlignment(QtCore.Qt.AlignCenter)
		self.labelLinegap.setWordWrap(True)
		self.labelLinegap.setObjectName("labelLinegap")
		self.labelCameraP = QtWidgets.QLabel(self.boxCameracontol)
		self.labelCameraP.setGeometry(QtCore.QRect(20, 380, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelCameraP.setFont(font)
		self.labelCameraP.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCameraP.setWordWrap(True)
		self.labelCameraP.setObjectName("labelCameraP")
		self.spinCameraP = QtWidgets.QDoubleSpinBox(self.boxCameracontol)
		self.spinCameraP.setGeometry(QtCore.QRect(100, 380, 111, 31))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.spinCameraP.setFont(font)
		self.spinCameraP.setMinimum(0.0)
		self.spinCameraP.setSingleStep(0.1)
		self.spinCameraP.setProperty("value", 2.0)
		self.spinCameraP.setObjectName("spinCameraP")
		self.labelCameraI = QtWidgets.QLabel(self.boxCameracontol)
		self.labelCameraI.setGeometry(QtCore.QRect(20, 420, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelCameraI.setFont(font)
		self.labelCameraI.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCameraI.setWordWrap(True)
		self.labelCameraI.setObjectName("labelCameraI")
		self.spinCameraI = QtWidgets.QDoubleSpinBox(self.boxCameracontol)
		self.spinCameraI.setGeometry(QtCore.QRect(100, 420, 111, 31))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.spinCameraI.setFont(font)
		self.spinCameraI.setMinimum(0.0)
		self.spinCameraI.setSingleStep(0.1)
		self.spinCameraI.setProperty("value", 0.5)
		self.spinCameraI.setObjectName("spinCameraI")
		self.spinCameraD = QtWidgets.QDoubleSpinBox(self.boxCameracontol)
		self.spinCameraD.setGeometry(QtCore.QRect(100, 460, 111, 31))
		font = QtGui.QFont()
		font.setPointSize(20)
		self.spinCameraD.setFont(font)
		self.spinCameraD.setMinimum(0.0)
		self.spinCameraD.setSingleStep(0.1)
		self.spinCameraD.setProperty("value", 1.0)
		self.spinCameraD.setObjectName("spinCameraD")
		self.labelCameraD = QtWidgets.QLabel(self.boxCameracontol)
		self.labelCameraD.setGeometry(QtCore.QRect(20, 460, 71, 31))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)
		self.labelCameraD.setFont(font)
		self.labelCameraD.setAlignment(QtCore.Qt.AlignCenter)
		self.labelCameraD.setWordWrap(True)
		self.labelCameraD.setObjectName("labelCameraD")
		self.btnCameraPID = QtWidgets.QPushButton(self.boxCameracontol)
		self.btnCameraPID.setGeometry(QtCore.QRect(120, 500, 91, 81))
		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(False)
		font.setWeight(50)
		self.btnCameraPID.setFont(font)
		self.btnCameraPID.setObjectName("btnCameraPID")
		self.textBrowser = QtWidgets.QTextBrowser(self.boxCameracontol)
		self.textBrowser.setGeometry(QtCore.QRect(20, 590, 191, 91))
		font = QtGui.QFont()
		font.setPointSize(5)
		self.textBrowser.setFont(font)
		self.textBrowser.setObjectName("textBrowser")
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
		#Reading
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
		#Camera Control
		self.spinTargetdia.valueChanged.connect(self.function_nozzledia)
		self.spinEdgesigma.valueChanged.connect(self.function_cameraedgesigma)
		self.spinLinelength.valueChanged.connect(self.function_line_length_gap)
		self.spinLinegap.valueChanged.connect(self.function_line_length_gap)
		self.spinCameraP.valueChanged.connect(self.function_cameraPIDValue)
		self.spinCameraI.valueChanged.connect(self.function_cameraPIDValue)
		self.spinCameraD.valueChanged.connect(self.function_cameraPIDValue)
		self.btnCamera.clicked.connect(self.function_cameraStart)
		self.btnCamera.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		self.btnCameraPID.clicked.connect(self.function_cameraPID)
		self.btnCameraPID.setStyleSheet("background-color: rgb(0,255,0);") #b,g,r format
		self.turn_on_selected_LED()
		
		#Update sensor display thread
		updateLabel = threading.Thread(target=self.updateTemperaturelabel)
		updateLabel.daemon = True
		updateLabel.start()
		
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
		self.btnmotorStart.setText(_translate("labelWindow", "Motor Start"))
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
		self.boxOutputfilament.setTitle(_translate("MainWindow", "Output Filament"))
		self.labelOutputDia1.setText(_translate("MainWindow", "Reading 1"))
		self.labelOutputDia2.setText(_translate("MainWindow", "Reading 2"))
		self.labelOutputDia3.setText(_translate("MainWindow", "Reading 3"))
		self.boxCameraview.setTitle(_translate("MainWindow", "Camera View"))
		self.boxCameracontol.setTitle(_translate("MainWindow", "Camera Control"))
		self.labelCameralight.setText(_translate("MainWindow", "Nozzle Dia"))
		self.labelLinelength.setText(_translate("MainWindow", "Line Length"))
		self.labelEdgesigma.setText(_translate("MainWindow", "Edge Detection Sigma"))
		self.btnCamera.setText(_translate("MainWindow", "Camera On"))
		self.labelLinegap.setText(_translate("MainWindow", "Line Gap"))
		self.labelCameraP.setText(_translate("MainWindow", "P-Term"))
		self.labelCameraI.setText(_translate("MainWindow", "I-Term"))
		self.labelCameraD.setText(_translate("MainWindow", "D-Term"))
		self.btnCameraPID.setText(_translate("MainWindow", "PID Enable"))
		self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
		"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
		"p, li { white-space: pre-wrap; }\n"
		"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:5pt; font-weight:400; font-style:normal;\">\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">NULL Data</p>\n"
		"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
		self.tabMenu.setTabText(self.tabMenu.indexOf(self.CameraTab), _translate("MainWindow", "Camera"))
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
