'''
Created on Oct 10, 2012

@author: Gary
'''
import threading
import os

from inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications
from windowsxbeecommunications import WindowsXbeeCommunications
from inputs.dataenvelope import DataEnvelope
from lib.constants import Constants
from lib.base import Base


class UnsupportedSystemError( Exception ):
    pass


class XBeeInputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    input_queue = None
    zigbee = None
    exit_flag = False

    communication_module = {'posix': BeagleboneXbeeCommunications,
                            'nt': WindowsXbeeCommunications}

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputsZigBee

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the InputQueue

        '''
        super( XBeeInputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.input_queue = queue

    def startCorrectZigbee( self, os_name=os.name ):
        if ( os_name in self.communication_module ):
            self.logger.debug( 'connect to zigbee on {}'.format( os_name ) )
            self.zigbee = self.communication_module[os_name]()
        else:
            raise UnsupportedSystemError( "System {} not supported".format( os_name ) )

    def run( self ):
        self.startCorrectZigbee()
        self.zigbee.connect()
        self.logger.warn( 'Successfully connect to Zigbee' )
        while True:
            self.logger.warn( 'waiting for data from Zigbee' )
            packet = self.zigbee.read()
            self.logger.info( 'read data from Zigbee' )
            env = DataEnvelope( type='xbee', packet=packet )
            self.logger.warn( 'read data {}'.format( packet ) )
            self.input_queue.transmit( env, Constants.Queue.mid_priority )
            if ( self.exit_flag ):
                break
