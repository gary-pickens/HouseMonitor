'''
Created on May 13, 2013

@author: Gary
'''
from PySide.QtGui import *
from PySide.QtCore import *
from SimpleXMLRPCServer import SimpleXMLRPCServer
import array
import datetime
import pprint
import xmlrpclib
from monitordata import MonitorData
# from monitormodel import MonitorModel


class MonitorThread( QThread ):
    '''
    classdocs
    '''
    values = None
    url = 'http://{}:{}'.format( 'beaglebone', 9002 )
    proxy = None

    read_data_timer_id = None
    read_data_interval = 3000

    options = None
    monitored_data = None

    read_data = Signal()
    showMessage = Signal( str )
    garage_temperature = Signal( str )
    sunroom_temperature = Signal( str )
    door_state = Signal( str )

    model = None

    def __init__( self, monitored_data ):
        '''
        Constructor
        '''
        super( MonitorThread, self ).__init__()
        self.monitored_data = monitored_data
        self.read_data_timer_id = self.startTimer( self.read_data_interval )


    def run( self ):
        self.connect_to_house_monitor()
        self.exec_()

    def timerEvent( self, event ):
        self.values = self.proxy.get_current_values()
        data = self.convertToArray()
        self.monitored_data.write_data( data )
        rows = len( data )
#        self.emit( SIGNAL( 'read_data()' ) )
        self.read_data.emit()

    def connect_to_house_monitor( self ):
        try:
            self.proxy = xmlrpclib.ServerProxy( self.url )
        except Exception:
            exit()

    def special_handling( self, current_value, device, port ):
        if ( device == 'HouseMonitor' and port == 'uptime' ):
            self.showMessage.emit( current_value )
        if ( device == '0x13a200409029bf' and port == 'adc-1' ):
            self.garage_temperature.emit( current_value )
        if ( device == '0x13a200409029bf' and port == 'dio-0' ):
            if current_value == 'True':
                self.door_state.emit( 'Closed' )
            else:
                self.door_state.emit( 'Open' )
        if ( device == '0x13a200408cccc3' and port == 'adc-0' ):
            self.sunroom_temperature.emit( current_value )

    def convertToArray( self ):
        rows = []
        arrival_time = None
        current_value = None
        for device in sorted( self.values.keys() ):
            display_device = device
            for port in sorted( self.values[device].keys() ):
                if 'current_value' in self.values[device][port]:
                    current_value = str( self.values[device][port]['current_value'] )
                    self.special_handling( current_value, device, port )
                if 'at' in self.values[device][port]:
                    if type ( self.values[device][port]['at'] ) == dict:
                        arrival_time = str( self.values[device][port]['at']['dt'] )
                    else:
                        arrival_time = str( self.values[device][port]['at'] )
                column = [device, port, current_value, arrival_time]
                rows.append( column )
        return rows

