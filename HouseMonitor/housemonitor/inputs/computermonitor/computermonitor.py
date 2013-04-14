'''
Created on Apr 11, 2013

@author: Gary
'''
import threading
import os
import re

from inputs.dataenvelope import DataEnvelope
from lib.constants import Constants
from lib.base import Base
from lib.getdatetime import GetDateTime
from datetime import timedelta


class MonitorComputer( Base, threading.Thread ):
    '''
    classdocs
    '''
    input_queue = None
    MAX_LINE_LENGTH = 120
    forever = True
    previous_time = GetDateTime()
    previous_tx = 0
    previous_rcv = 0

    files = {'serial': {'file':'/proc/tty/driver/OMAP-SERIAL',
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
        super( MonitorComputer, self ).__init__()
        threading.Thread.__init__( self )
        self.input_queue = queue


    def extractData( self, file_contents ):
        m = self.files['serial']['regexp'].search( file_contents )
        if m == None:
            self.logger.debug( "Failed regex" )
            return None
        else:
            return m.groupdict()


    def readFile( self, filename ):
        with open( filename, 'r' ) as f:
            results = line = f.readline( self.MAX_LINE_LENGTH )
            while line:
                line = f.readline( self.MAX_LINE_LENGTH )
                results += line
            dt = GetDateTime()
        return results, dt

    def run( self ):
        while True:
            for key in self.files:
                file_contents, datetime = self.readFile( self.files[key]['filename'] )
                data = self.extractData( key, file_contents )
                for key, value in data.iteritems():
                    packet = {}
                    packet[Constants.DataPacket.device] = 'OMAP UART1'
                    packet[Constants.DataPacket.port] = key
                    packet[Constants.DataPacket.arrival_time] = datetime
                    packet[Constants.DataPacket.current_value] = value
                    env = DataEnvelope( type='Computer', packet=packet )
                    self.logger.debug( 'read data {}'.format( packet ) )
                    self.input_queue.transmit( env, Constants.Queue.low_priority )

                    delta = datetime - self.previous_time
                    rate = int( value ) / delta.seconds()

                    packet[Constants.DataPacket.device] = 'OMAP UART1'
                    packet[Constants.DataPacket.port] = key + " rate"
                    packet[Constants.DataPacket.arrival_time] = datetime
                    packet[Constants.DataPacket.current_value] = rate
                    env = DataEnvelope( type='Computer', packet=packet )
                    self.logger.debug( 'read data {}'.format( packet ) )
                    self.input_queue.transmit( env, Constants.Queue.low_priority )

            self.previous_time = datetime
            if ( self.forever == False ):
                break
