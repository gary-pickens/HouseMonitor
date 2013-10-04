'''
Created on Oct 10, 2012

@author: Gary
'''
import threading
import time
import logging
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib import constants
from housemonitor.outputs.zigbee.zigbeeoutput import ZigBeeOutput
from housemonitor.lib.base import Base


class ZigBeeOutputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    output_queue = None
    zigbee_output = None
    done = False
    connected = False
    talking = True

    def __init__( self, queue, in_test_mode ):
        '''
        Constructor
        args:
            queue is the xbee output Queue

        '''
        super( ZigBeeOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue
        self.in_test_mode = in_test_mode

    @property
    def logger_name( self ):
        return Constants.LogKeys.outputsZigBee

    def zigbeeConnect( self ):
        try:
            self.zigbee_output = ZigBeeOutput( self.in_test_mode )
            self.zigbee_output.startCorrectZigbee()
            self.connected = self.talking = True
            self.logger.debug( 'Connect to ZibBee' )
        except Exception as ex:
            self.logger.error( ex )
            time.sleep( 10 )
            self.connected = self.talking = False
        return self.connected

    def processCommandToZigBee( self ):
        packet = self.output_queue.receive()
        self.logger.debug( "Thread Output ZigBee Received packet for sending to XBee" )
        try:
            data = packet['data']
            value = packet['value']
            id = packet['id']
            self.zigbee_output.sendCommand( value, data, id )
            self.talking = self.connected = True
            self.logger.debug( 'command sent to zigbee: value = {} data = {} id = {}'.format( value, data, id ) )
        except IOError as er:
            self.logger.exception( er )
            self.connected = self.talking = False
        return self.talking

    def connectAndProcessZigBeeCommands( self ):
        try:
            while not self.done:
                while not self.connected:
                    self.connected = self.zigbeeConnect()
                    self.logger.debug( "Successfully connected to the zigbee".format( self.connected ) )
                while self.talking:
                    self.talking = self.processCommandToZigBee()
        except KeyboardInterrupt as ki:
            self.logger.exception( ki )

    def run( self ):
        self.connectAndProcessZigBeeCommands()
