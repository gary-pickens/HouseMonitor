'''
Created on Oct 10, 2012

@author: Gary
'''
import threading
import os

from housemonitor.inputs.zigbeeinput.beagleboneblackxbeecommunications import BeagleboneBlackXbeeCommunications
from windowsxbeecommunications import WindowsXbeeCommunications
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib.base import Base


class UnsupportedSystemError( Exception ):
    pass


class XBeeInputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    input_queue = None
    zigbee = None
    exit_flag = False

    communication_module = {'posix': BeagleboneBlackXbeeCommunications,
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
        while True:
            packet = self.zigbee.read()
            env = DataEnvelope( type='xbee', packet=packet )
            self.input_queue.transmit( env, Constants.Queue.mid_priority )
            if ( self.exit_flag ):
                break
