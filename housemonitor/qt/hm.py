#!/usr/bin/python2.7
from PySide.QtCore import *
from PySide.QtGui import *
from PySide import *
import sys
import monitor
from monitorthread import MonitorThread
from monitordata import MonitorData


class HMStandardItemModel( QStandardItemModel ):

    monitor_data = None
    values = None
    previous_values = None
    get_data = Signal()

    def __init__( self, rows, columns, monitor_data ):
        super( HMStandardItemModel, self ).__init__( rows, columns )
        self.monitor_data = monitor_data

    @QtCore.Slot()
    def read_data( self ):
        self.previous_values = self.values
        self.values = self.monitor_data.retreive_data()
        for rows in range( 0, len( self.values ) ):
            for columns in range( 0, 4 ):
                if ( self.previous_values == None ):
                    item = QStandardItem( self.values[rows][columns] )
                    self.setItem( rows, columns, item )
                elif ( len( self.previous_values ) >= rows and
                        self.previous_values[rows][columns] != self.values[rows][columns] ):
                    item = QStandardItem( self.values[rows][columns] )
                    self.setItem( rows, columns, item )


class MainWindow( QMainWindow, monitor.Ui_MainWindow ):

    md = None
    model = None
    mt = None
    thread_exit_signal = Signal()

    @QtCore.Slot()
    def button_clicked( self ):
        print "Bang!"

    def stop_program( self ):
        self.mt.finish_thread.emit()
        self.mt.wait( 1000 )
        self.close()


    def __init__( self, parent=None ):
        super( MainWindow, self ).__init__()

        md = MonitorData()
        self.model = HMStandardItemModel ( 0, 4, md )
        self.mt = MonitorThread( md )
# Old style signal
#        self.connect( self.mt, SIGNAL( 'read_data()' ), self.model.read_data )
# New style signal
        self.mt.read_data.connect( self.model.read_data )

        self.mt.start()
        self.setupUi( self )

        self.mt.showMessage.connect( self.statusbar.showMessage )
        self.mt.garage_temperature.connect( self.garage_temperature.setText )
        self.mt.sunroom_temperature.connect( self.sunroom_temperature.setText )
        self.mt.door_state.connect( self.door_state.setText )
        self.mt.kitchen_temperature.connect( self.kitchen_temperature.setText )
        self.mt.outdoor_temperature.connect( self.outdoor_temperature.setText )
        self.mt.power_controller_1_temperature.connect( self.power_controller_1_temperature.setText )

        self.status_proxy_model = QSortFilterProxyModel()
        self.computer_proxy_model = QSortFilterProxyModel()
        self.HouseMonitor_proxy_model = QSortFilterProxyModel()
        self.all_table_view.setModel( self.model )

        self.status_proxy_model.setSourceModel( self.model )
        self.computer_proxy_model.setSourceModel( self.model )
        self.HouseMonitor_proxy_model.setSourceModel( self.model )

        self.status_proxy_model.setFilterRegExp( QRegExp( "^0x.*$", Qt.CaseSensitive, QRegExp.RegExp ) )
        self.status_proxy_model.setFilterKeyColumn( 0 )
        self.status_proxy_model.sort( 0, Qt.DescendingOrder )
        self.status_proxy_model.setDynamicSortFilter( True )

        self.HouseMonitor_proxy_model.setFilterRegExp( QRegExp( "^HouseMonitor\\..*$", Qt.CaseSensitive, QRegExp.RegExp ) )
        self.HouseMonitor_proxy_model.setFilterKeyColumn( 0 )
        self.HouseMonitor_proxy_model.sort( 0, Qt.DescendingOrder )
        self.HouseMonitor_proxy_model.setDynamicSortFilter( True )

        self.computer_proxy_model.setFilterRegExp( QRegExp( "^OMAP.*$", Qt.CaseSensitive, QRegExp.RegExp ) )
        self.computer_proxy_model.setFilterKeyColumn( 0 )
        self.computer_proxy_model.sort( 0, Qt.DescendingOrder )
        self.computer_proxy_model.setDynamicSortFilter( True )

        self.status_table_view.setModel( self.status_proxy_model )
        self.house_monitor_table_view.setModel( self.HouseMonitor_proxy_model )
        self.computer_table_view.setModel( self.computer_proxy_model )


        self.all_table_view.horizontalHeader().setResizeMode( 0, QHeaderView.ResizeToContents )
        self.status_table_view.horizontalHeader().setResizeMode( 0, QHeaderView.ResizeToContents )
        self.house_monitor_table_view.horizontalHeader().setResizeMode( 0, QHeaderView.ResizeToContents )
        self.computer_table_view.horizontalHeader().setResizeMode( 0, QHeaderView.ResizeToContents )

        self.model.setHorizontalHeaderItem( 0, QStandardItem( 'Device' ) )
        self.model.setHorizontalHeaderItem( 1, QStandardItem( 'Port' ) )
        self.model.setHorizontalHeaderItem( 2, QStandardItem( 'Value' ) )
        self.model.setHorizontalHeaderItem( 3, QStandardItem( 'Time' ) )

        # Turn on and off devices
        self.GarysBedLightOn.clicked.connect( self.mt.turnGarysLightOn )
        self.GarysBedLightOff.clicked.connect( self.mt.turnGarysLightOff )

        self.MarilynsBedLightOn.clicked.connect( self.mt.turnMarilynsLightOn )
        self.MarilynsBedLightOff.clicked.connect( self.mt.turnMarilynsLightOff )

        self.actionExit.triggered.connect( self.stop_program )
        self.mt.finish_thread.connect( self.mt.finish_up )

app = QApplication( sys.argv )
form = MainWindow()


form.show()
app.exec_()

