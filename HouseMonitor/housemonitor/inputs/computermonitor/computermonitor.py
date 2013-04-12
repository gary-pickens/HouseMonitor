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


class ComputerMonitor( Base, object ):
    '''
    classdocs
    '''
    input_queue = None
    files = {'serial': {'file':'/proc/tty/driver/OMAP-SERIAL',
                        'regexp': re.compile( '''^.*OMAP UART1.*   # The device
                                            tx:(?P<tx>\d*)\s*   # number of char transmitted
                                            rx:(?P<rx>\d*)      # the number of chars received
                                            .*$''',
                                            flags=re.MULTILINE | re.VERBOSE )}}

    @property
    def logger_name( self ):
        return Constants.LogKeys.ComputerMonitor

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the InputQueue

        '''
        super( ComputerMonitor, self ).__init__()
        threading.Thread.__init__( self )
        self.input_queue = queue


    def extractData( self, file_contents ):
        m = self.files[0].match( file_contents )
        return m.groupdict()


    def readFile( self, filename ):
        with open( filename, 'r' ) as f:
            results = line = f.readline( 80 )
            while line:
                line = f.readline( 80 )
                results += line
            dt = GetDateTime()
        return results, dt

    def run( self ):
        while True:
            for key in self.files:
                file_contents, datetime = self.readFile( self.files[key]['filename'] )
                data = self.extractData( key, file_contents )
                for key in data:

#                     env = DataEnvelope( type='xbee', packet=packet )
#                     self.logger.debug( 'read data {}'.format( packet ) )
#                     self.input_queue.transmit( env, Constants.Queue.mid_priority )
#                     if ( self.exit_flag ):
#                             break
