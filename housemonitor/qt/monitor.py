# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HouseMonitor3.ui'
#
# Created: Mon Oct 14 12:47:07 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status_view = QtGui.QTabWidget(self.centralwidget)
        self.status_view.setObjectName("status_view")
        self.general_tab = QtGui.QWidget()
        self.general_tab.setObjectName("general_tab")
        self.layoutWidget = QtGui.QWidget(self.general_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 50, 311, 158))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.garage_door_label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.garage_door_label.setFont(font)
        self.garage_door_label.setObjectName("garage_door_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.garage_door_label)
        self.door_state = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.door_state.setFont(font)
        self.door_state.setFrameShape(QtGui.QFrame.Box)
        self.door_state.setText("")
        self.door_state.setObjectName("door_state")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.door_state)
        self.garage_temperature_label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.garage_temperature_label.setFont(font)
        self.garage_temperature_label.setObjectName("garage_temperature_label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.garage_temperature_label)
        self.garage_temperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.garage_temperature.setFont(font)
        self.garage_temperature.setFrameShape(QtGui.QFrame.Box)
        self.garage_temperature.setText("")
        self.garage_temperature.setObjectName("garage_temperature")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.garage_temperature)
        self.sunroom_temerature_label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sunroom_temerature_label.setFont(font)
        self.sunroom_temerature_label.setObjectName("sunroom_temerature_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.sunroom_temerature_label)
        self.sunroom_temperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.sunroom_temperature.setFont(font)
        self.sunroom_temperature.setFrameShape(QtGui.QFrame.Box)
        self.sunroom_temperature.setText("")
        self.sunroom_temperature.setObjectName("sunroom_temperature")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.sunroom_temperature)
        self.KitchenTemperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.KitchenTemperature.setFont(font)
        self.KitchenTemperature.setObjectName("KitchenTemperature")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.KitchenTemperature)
        self.outdoor_temperature_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outdoor_temperature_2.setFont(font)
        self.outdoor_temperature_2.setObjectName("outdoor_temperature_2")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.outdoor_temperature_2)
        self.power_controller_1_temperature_2 = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.power_controller_1_temperature_2.setFont(font)
        self.power_controller_1_temperature_2.setObjectName("power_controller_1_temperature_2")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.power_controller_1_temperature_2)
        self.kitchen_temperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.kitchen_temperature.setFont(font)
        self.kitchen_temperature.setFrameShape(QtGui.QFrame.Box)
        self.kitchen_temperature.setText("")
        self.kitchen_temperature.setObjectName("kitchen_temperature")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.kitchen_temperature)
        self.outdoor_temperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outdoor_temperature.setFont(font)
        self.outdoor_temperature.setFrameShape(QtGui.QFrame.Box)
        self.outdoor_temperature.setText("")
        self.outdoor_temperature.setObjectName("outdoor_temperature")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.outdoor_temperature)
        self.power_controller_1_temperature = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.power_controller_1_temperature.setFont(font)
        self.power_controller_1_temperature.setFrameShape(QtGui.QFrame.Box)
        self.power_controller_1_temperature.setText("")
        self.power_controller_1_temperature.setObjectName("power_controller_1_temperature")
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.power_controller_1_temperature)
        self.gridLayoutWidget = QtGui.QWidget(self.general_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 260, 311, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.GarysLightLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.GarysLightLabel.setObjectName("GarysLightLabel")
        self.gridLayout.addWidget(self.GarysLightLabel, 1, 0, 1, 1)
        self.GarysBedLightOn = QtGui.QPushButton(self.gridLayoutWidget)
        self.GarysBedLightOn.setObjectName("GarysBedLightOn")
        self.gridLayout.addWidget(self.GarysBedLightOn, 1, 1, 1, 1)
        self.GarysBedLightOff = QtGui.QPushButton(self.gridLayoutWidget)
        self.GarysBedLightOff.setObjectName("GarysBedLightOff")
        self.gridLayout.addWidget(self.GarysBedLightOff, 1, 2, 1, 1)
        self.MarilynsLightLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.MarilynsLightLabel.setObjectName("MarilynsLightLabel")
        self.gridLayout.addWidget(self.MarilynsLightLabel, 0, 0, 1, 1)
        self.MarilynsBedLightOn = QtGui.QPushButton(self.gridLayoutWidget)
        self.MarilynsBedLightOn.setObjectName("MarilynsBedLightOn")
        self.gridLayout.addWidget(self.MarilynsBedLightOn, 0, 1, 1, 1)
        self.MarilynsBedLightOff = QtGui.QPushButton(self.gridLayoutWidget)
        self.MarilynsBedLightOff.setObjectName("MarilynsBedLightOff")
        self.gridLayout.addWidget(self.MarilynsBedLightOff, 0, 2, 1, 1)
        self.status_view.addTab(self.general_tab, "")
        self.status_tab = QtGui.QWidget()
        self.status_tab.setObjectName("status_tab")
        self.status_table_view = QtGui.QTableView(self.status_tab)
        self.status_table_view.setGeometry(QtCore.QRect(0, 0, 781, 521))
        self.status_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.status_table_view.setAlternatingRowColors(True)
        self.status_table_view.setWordWrap(False)
        self.status_table_view.setObjectName("status_table_view")
        self.status_table_view.horizontalHeader().setDefaultSectionSize(120)
        self.status_table_view.horizontalHeader().setStretchLastSection(True)
        self.status_view.addTab(self.status_tab, "")
        self.house_monitor_tab = QtGui.QWidget()
        self.house_monitor_tab.setObjectName("house_monitor_tab")
        self.house_monitor_table_view = QtGui.QTableView(self.house_monitor_tab)
        self.house_monitor_table_view.setGeometry(QtCore.QRect(0, 0, 801, 531))
        self.house_monitor_table_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.house_monitor_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.house_monitor_table_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.house_monitor_table_view.setTabKeyNavigation(False)
        self.house_monitor_table_view.setProperty("showDropIndicator", False)
        self.house_monitor_table_view.setDragDropOverwriteMode(False)
        self.house_monitor_table_view.setAlternatingRowColors(True)
        self.house_monitor_table_view.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.house_monitor_table_view.setWordWrap(False)
        self.house_monitor_table_view.setObjectName("house_monitor_table_view")
        self.house_monitor_table_view.horizontalHeader().setVisible(False)
        self.house_monitor_table_view.horizontalHeader().setCascadingSectionResizes(True)
        self.house_monitor_table_view.horizontalHeader().setDefaultSectionSize(200)
        self.house_monitor_table_view.verticalHeader().setVisible(False)
        self.status_view.addTab(self.house_monitor_tab, "")
        self.computer_tab = QtGui.QWidget()
        self.computer_tab.setObjectName("computer_tab")
        self.computer_table_view = QtGui.QTableView(self.computer_tab)
        self.computer_table_view.setGeometry(QtCore.QRect(0, 0, 801, 531))
        self.computer_table_view.setAlternatingRowColors(True)
        self.computer_table_view.setWordWrap(False)
        self.computer_table_view.setCornerButtonEnabled(False)
        self.computer_table_view.setObjectName("computer_table_view")
        self.computer_table_view.horizontalHeader().setStretchLastSection(True)
        self.status_view.addTab(self.computer_tab, "")
        self.all = QtGui.QWidget()
        self.all.setObjectName("all")
        self.all_table_view = QtGui.QTableView(self.all)
        self.all_table_view.setGeometry(QtCore.QRect(0, 0, 781, 521))
        self.all_table_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.all_table_view.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.all_table_view.setTabKeyNavigation(False)
        self.all_table_view.setProperty("showDropIndicator", False)
        self.all_table_view.setDragDropOverwriteMode(False)
        self.all_table_view.setAlternatingRowColors(True)
        self.all_table_view.setWordWrap(False)
        self.all_table_view.setObjectName("all_table_view")
        self.all_table_view.horizontalHeader().setStretchLastSection(True)
        self.status_view.addTab(self.all, "")
        self.horizontalLayout.addWidget(self.status_view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGeneral = QtGui.QAction(MainWindow)
        self.actionGeneral.setObjectName("actionGeneral")
        self.actionStatus = QtGui.QAction(MainWindow)
        self.actionStatus.setObjectName("actionStatus")
        self.actionProgram_Status = QtGui.QAction(MainWindow)
        self.actionProgram_Status.setObjectName("actionProgram_Status")
        self.actionComputer_Status = QtGui.QAction(MainWindow)
        self.actionComputer_Status.setObjectName("actionComputer_Status")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionConfiguration = QtGui.QAction(MainWindow)
        self.actionConfiguration.setObjectName("actionConfiguration")
        self.menuFile.addAction(self.actionConfiguration)
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionGeneral)
        self.menuView.addAction(self.actionStatus)
        self.menuView.addAction(self.actionProgram_Status)
        self.menuView.addAction(self.actionComputer_Status)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.status_view.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "House Monitor", None, QtGui.QApplication.UnicodeUTF8))
        self.garage_door_label.setText(QtGui.QApplication.translate("MainWindow", "Garage Door", None, QtGui.QApplication.UnicodeUTF8))
        self.garage_temperature_label.setText(QtGui.QApplication.translate("MainWindow", "Garage Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.sunroom_temerature_label.setText(QtGui.QApplication.translate("MainWindow", "Sunroom Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.KitchenTemperature.setText(QtGui.QApplication.translate("MainWindow", "Kitchen Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.outdoor_temperature_2.setText(QtGui.QApplication.translate("MainWindow", "Outdoor Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.power_controller_1_temperature_2.setText(QtGui.QApplication.translate("MainWindow", "Power Controller 1 Temperature", None, QtGui.QApplication.UnicodeUTF8))
        self.GarysLightLabel.setText(QtGui.QApplication.translate("MainWindow", "Gary\'s Bed Light", None, QtGui.QApplication.UnicodeUTF8))
        self.GarysBedLightOn.setText(QtGui.QApplication.translate("MainWindow", "On", None, QtGui.QApplication.UnicodeUTF8))
        self.GarysBedLightOff.setText(QtGui.QApplication.translate("MainWindow", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.MarilynsLightLabel.setText(QtGui.QApplication.translate("MainWindow", "Marilyn\'s Bed Light", None, QtGui.QApplication.UnicodeUTF8))
        self.MarilynsBedLightOn.setText(QtGui.QApplication.translate("MainWindow", "On", None, QtGui.QApplication.UnicodeUTF8))
        self.MarilynsBedLightOff.setText(QtGui.QApplication.translate("MainWindow", "Off", None, QtGui.QApplication.UnicodeUTF8))
        self.status_view.setTabText(self.status_view.indexOf(self.general_tab), QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.status_view.setTabText(self.status_view.indexOf(self.status_tab), QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.status_view.setTabText(self.status_view.indexOf(self.house_monitor_tab), QtGui.QApplication.translate("MainWindow", "House Monitor", None, QtGui.QApplication.UnicodeUTF8))
        self.status_view.setTabText(self.status_view.indexOf(self.computer_tab), QtGui.QApplication.translate("MainWindow", "Computer", None, QtGui.QApplication.UnicodeUTF8))
        self.status_view.setTabText(self.status_view.indexOf(self.all), QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("MainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGeneral.setText(QtGui.QApplication.translate("MainWindow", "General ", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStatus.setText(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProgram_Status.setText(QtGui.QApplication.translate("MainWindow", "Program Status", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputer_Status.setText(QtGui.QApplication.translate("MainWindow", "Computer Status", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfiguration.setText(QtGui.QApplication.translate("MainWindow", "Configuration", None, QtGui.QApplication.UnicodeUTF8))

