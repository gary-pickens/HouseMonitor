'''
Created on Apr 11, 2013

@author: Gary
'''
from datetime import timedelta
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants
from housemonitor.lib.getdatetime import GetDateTime
import copy
import os
import re
import threading
import time



class ComputerMonitor( Base, threading.Thread ):
    '''
    classdocs
    '''
    input_queue = None
    forever = True
    previous_time = {}
    previous_count = {}
    start_count = {}
    time_between_reads = 300.0

    files = {'serial': {'file':'/proc/tty/driver/OMAP-SERIAL',
                        'device': 'OMAP-SERIAL',
                        'port': 'OMAP UART1',
                         'regexp': re.compile( '''^.*OMAP\sUART1.*     # Select correct device
                                                  tx:(?P<tx>\d*)\s*   # Get number of char xmited
                                                  rx:(?P<rx>\d*)      # the number of chars received
                                                 .*$''', flags=re.MULTILINE | re.VERBOSE )}}

    @property
    def logger_name( self ):
        return Constants.LogKeys.ComputerMonitor

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the InputQueue

        '''
        try:
            super( ComputerMonitor, self ).__init__()
            threading.Thread.__init__( self )
            self.input_queue = queue
        except Exception as ex:
            self.logger.exception( ex )

    def extractData( self, file_contents ):
        m = self.files['serial']['regexp'].search( file_contents )
        if m == None:
            self.logger.debug( "Failed regex" )
            return None
        else:
            return m.groupdict()

    def readFile( self, filename ):
        ''' Read the number of bytes transmitted and received. '''

        try:
            with open( filename, 'r' ) as f:
                results = f.read()
                dt = GetDateTime()
                return results, dt
        except Exception as ex:
            self.logger.exception( ex )
            raise

    def send( self, dt, key, value ):
        listeners = [Constants.TopicNames.CurrentValueStep]
        data = {Constants.DataPacket.device: 'OMAP UART1',
                Constants.DataPacket.port: key,
                Constants.DataPacket.arrival_time: dt,
                Constants.DataPacket.current_value: value,
                Constants.DataPacket.listeners: copy.copy( listeners )}

        env = DataEnvelope( type=Constants.EnvelopeTypes.status, data=data, arrival_time=dt )
        self.input_queue.transmit( packet=env, priority=Constants.Queue.low_priority )

    def process_data( self, file_contents, dt ):
        for key, value in file_contents.iteritems():
            value = int( value )
            if key not in self.start_count:
                self.start_count[key] = value
                self.previous_count[key] = value
                self.previous_time[key] = dt
            else:
                # Send the number of bytes send since program stated
                count = value - self.start_count[key]
                self.send( dt, key, count )

                # Send the number of bytes per second
                delta = dt.datetime() - self.previous_time[key].datetime()
                rate = int( ( count - self.previous_count[key] ) / delta.total_seconds() )
                what = key + " rate"
                if ( rate > 0 ):
                    self.send( dt, what, rate )

                self.previous_count[key] = count
                self.previous_time[key] = dt


    def run( self ):
        while True:
            try:
                extracted_data, extraction_time = self.readFile( self.files['serial']['file'] )
                data = self.extractData( extracted_data )
                self.process_data( data, extraction_time )
            except Exception as ex:
                self.logger.exception( ex )
            if ( self.forever == False ):
                break
            time.sleep( self.time_between_reads )
