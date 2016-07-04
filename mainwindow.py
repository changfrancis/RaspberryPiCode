# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon Jul  4 11:03:21 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_labelWindow(object):
    def setupUi(self, labelWindow):
        labelWindow.setObjectName("labelWindow")
        labelWindow.resize(480, 800)
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
        self.tabMenu.setGeometry(QtCore.QRect(0, 0, 481, 740))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabMenu.sizePolicy().hasHeightForWidth())
        self.tabMenu.setSizePolicy(sizePolicy)
        self.tabMenu.setObjectName("tabMenu")
        self.ControlTab = QtWidgets.QWidget()
        self.ControlTab.setObjectName("ControlTab")
        self.btnEstop = QtWidgets.QPushButton(self.ControlTab)
        self.btnEstop.setGeometry(QtCore.QRect(340, 470, 121, 221))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btnEstop.setFont(font)
        self.btnEstop.setDefault(True)
        self.btnEstop.setObjectName("btnEstop")
        self.boxSetTarget = QtWidgets.QGroupBox(self.ControlTab)
        self.boxSetTarget.setGeometry(QtCore.QRect(0, 0, 321, 700))
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
        self.lcdcoldblock.setProperty("value", 25.1)
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
        self.lcdAircon.setProperty("value", 25.1)
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
        self.lcdHotend.setProperty("value", 25.1)
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
        self.scrollHotend.setMinimum(251)
        self.scrollHotend.setMaximum(1500)
        self.scrollHotend.setPageStep(1)
        self.scrollHotend.setSliderPosition(251)
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
        self.scrollColdblock.setSliderPosition(251)
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
        self.scrollAircon.setSliderPosition(251)
        self.scrollAircon.setOrientation(QtCore.Qt.Vertical)
        self.scrollAircon.setInvertedAppearance(False)
        self.scrollAircon.setInvertedControls(True)
        self.scrollAircon.setObjectName("scrollAircon")
        self.scrollFilament = QtWidgets.QScrollBar(self.boxSetTarget)
        self.scrollFilament.setGeometry(QtCore.QRect(220, 20, 40, 100))
        self.scrollFilament.setAutoFillBackground(False)
        self.scrollFilament.setMinimum(160)
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
        self.btnRetract = QtWidgets.QPushButton(self.boxSetTarget)
        self.btnRetract.setGeometry(QtCore.QRect(170, 570, 140, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btnRetract.setFont(font)
        self.btnRetract.setObjectName("btnRetract")
        self.btnExtrude = QtWidgets.QPushButton(self.boxSetTarget)
        self.btnExtrude.setGeometry(QtCore.QRect(10, 570, 140, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.btnExtrude.setFont(font)
        self.btnExtrude.setAutoDefault(False)
        self.btnExtrude.setDefault(False)
        self.btnExtrude.setFlat(False)
        self.btnExtrude.setObjectName("btnExtrude")
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
        self.DebugTab = QtWidgets.QWidget()
        self.DebugTab.setObjectName("DebugTab")
        self.tabMenu.addTab(self.DebugTab, "")
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
        self.btnRetract.setText(_translate("labelWindow", "Retract"))
        self.btnExtrude.setText(_translate("labelWindow", "Extrude"))
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
        self.tabMenu.setTabText(self.tabMenu.indexOf(self.DebugTab), _translate("labelWindow", "Debug"))
        self.menuFile.setTitle(_translate("labelWindow", "File"))
        self.actionExit.setText(_translate("labelWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    labelWindow = QtWidgets.QMainWindow()
    ui = Ui_labelWindow()
    ui.setupUi(labelWindow)
    labelWindow.show()
    sys.exit(app.exec_())

