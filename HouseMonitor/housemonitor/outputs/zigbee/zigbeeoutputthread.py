'''
Created on Oct 10, 2012

@author: Gary
'''
import threading
import time
import logging
from lib.hmqueue import HMQueue
from inputs.dataenvelope import DataEnvelope
from lib.constants import Constants
from lib import constants
from outputs.zigbee.zigbeeoutput import ZigBeeOutput
from lib.base import Base


class ZigBeeOutputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    output_queue = None
    zigbee_output = None
    done = False
    connected = False
    talking = True

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the xbee output Queue

        '''
        super( ZigBeeOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue

    @property
    def logger_name( self ):
        return Constants.LogKeys.outputsZigBee

    def zigbeeConnect( self ):
        try:
            self.zigbee_output = ZigBeeOutput()
            self.zigbee_output.startCorrectZigbee()
#            TODO: Remove the following line
#            self.zigbee_output.connect()
            self.connected = self.talking = True
        except Exception as ex:
            self.logger.error( ex )
            time.sleep( 10 )
            self.connected = self.talking = False
        return self.connected

    def processCommandToZigBee( self ):
        packet = self.output_queue.receive()
        self.logger.debug( "Received packet {}".format( packet ) )
        try:
            data = packet['data']
            value = packet['value']
            self.zigbee_output.sendCommand( value, data )
            self.talking = self.connected = True
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
