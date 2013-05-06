'''
Created on Oct 10, 2012

@author: Gary
'''
from lib.base import Base
from xbee.zigbee import ZigBee
from lib.constants import Constants
import abc
import time


class XBeeCommunications( Base, object ):
    '''
    classdocs
    '''
    __metaclass__ = abc.ABCMeta

    serial_id = None
    connected = False
    zigbee = None

    delay = 7    # seconds
    ''' How long to wait before attempting to connect to the serial port on failure. '''

    def __init__( self ):
        super( XBeeCommunications, self ).__init__()

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputsZigBee

    @abc.abstractmethod
    def setup( self ):    # pragma: no cover
        """
        setup - a virtual function
        """
        pass

    def read( self ):
        """
        read - function read a frame of data from the XBee
        """
        packet = self.zigbee.wait_read_frame()
        return packet

    def connect( self ):
        """
        The main method for connecting with XBee radio
        """
        while True:
            try:
                self.logger.debug( "Attempting connection to XBee" )
                self.serial_id = self.setup()
                self.connected = True
            except IOError as ex:
                self.logger.exception( ex )
                time.sleep( self.delay )
            if self.connected:
                break
        self.zigbee = ZigBee( self.serial_id )
        self.logger.debug( "Successfully connected to XBee" )
