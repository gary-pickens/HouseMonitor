'''
Created on May 13, 2013

@author: Gary
'''
from PySide.QtCore import QThread, Signal
import xmlrpclib
import winsound
import time


class MonitorThread( QThread ):
    '''
    This class is run as a thread.  It will open a xmlrpc client connection to the server on
    the beagle bone commuter.  It will then read the data from the beagle bone every read_data_interval(initially ever
    3 seconds).  It will then use MonitorData to pass the data to the main thread.
    '''
    '''
    TODO: read a lot of information from configuration files
    '''
    '''
    TODO: Use Constants file for a lot of the hard coded values
    '''
    values = None
    url = 'http://{}:{}'.format( 'beaglebone', 9002 )
    proxy = None

    connected = False

    alarm_tone = 523
    alarm_duration = 700
    alarm_sounded = False

    read_data_interval = 3000

    options = None
    monitored_data = None

    read_data = Signal()
    showMessage = Signal( str )
    garage_temperature = Signal( str )
    sunroom_temperature = Signal( str )
    door_state = Signal( str )
    finish_thread = Signal()

    model = None

    def finish_up( self ):
        # TODO: why can't I call quit directly?
        self.quit()

    def __init__( self, monitored_data ):
        '''
        Initialize the MonitorThread.
        '''
        self.monitored_data = monitored_data
        super( MonitorThread, self ).__init__()
        self.read_data_timer_id = self.startTimer( self.read_data_interval )

    def sound_alarm( self ):
        '''
        Sound the alarm when the garage door is opened.
        '''
        winsound.Beep( self.alarm_tone, self.alarm_duration )
        self.alarm_sounded = True
        print 'beep'

    def run( self ):
        self.exec_()

    def timerEvent( self, event ):    # @UnusedVariable
        '''
        This time event is started in the constructor at read_data_interval.  It's main
        task is to read the data from HouseMonitor program and send it to the main thread.
        
        :param event:
        :type event:
        '''
        while not self.connected:
            self.connect_to_house_monitor()
        try:
            self.values = self.proxy.get_current_values()
        except Exception:
            self.connected = False
        finally:
            if self.connected:
                data = self.convertToArray()
                self.monitored_data.write_data( data )
#               self.emit( SIGNAL( 'read_data()' ) )
                self.read_data.emit()

    def connect_to_house_monitor( self ):
        '''
        This method will attempt to connect to the housemonitor program running on the beaglebone
        server.  If it fails it will sleep for 2 minutes and try again.
        '''
        try:
            self.proxy = xmlrpclib.ServerProxy( self.url )
            self.connected = True
        except Exception:
            time.sleep( 120 )
            self.connected = False

    def special_handling( self, current_value, device, port ):
        '''
        This routine will inspect values that have been read form the xmlrpc server an perform
        various things with them: such as sending the values to various places(status bar, or
        the front page) in the application.
         
        :param current_value:
        :type current_value:
        :param device:
        :type device:
        :param port:
        :type port:
        '''
        if ( device == 'HouseMonitor' and port == 'uptime' ):
            self.showMessage.emit( 'HouseMonitor Up Time: ' + current_value )
        if ( device == '0x13a200409029bf' and port == 'adc-1' ):
            self.garage_temperature.emit( current_value )
        if ( device == '0x13a200409029bf' and port == 'dio-0' ):
            if current_value == 'True':
                self.door_state.emit( 'Closed' )
                self.alarm_sounded = False
            else:
                self.door_state.emit( 'Open' )
                if not self.alarm_sounded:
                    self.sound_alarm()
        if ( device == '0x13a200408cccc3' and port == 'adc-0' ):
            self.sunroom_temperature.emit( current_value )

    def convertToArray( self ):
        '''
        Convert the tree like data structure passed from beagle bone to a list of lists
        suitable for display.
        '''
        rows = []
        arrival_time = None
        current_value = None
        if self.values != None:
            for device in sorted( self.values.keys() ):
                for port in sorted( self.values[device].keys() ):
                    if 'current_value' in self.values[device][port]:
                        current_value = str( self.values[device][port]['current_value'] )
                        self.special_handling( current_value, device, port )
                    if 'at' in self.values[device][port]:
                        # TODO: Sometime this needs to be fixed in the server
                        if type( self.values[device][port]['at'] ) == dict:
                            arrival_time = str( self.values[device][port]['at']['dt'] )
                        else:
                            arrival_time = str( self.values[device][port]['at'] )
                    column = [device, port, current_value, arrival_time]
                    rows.append( column )
        return rows
