'''
Created on Oct 10, 2012

@author: Gary
'''
import os
import Adafruit_BBIO.UART as UART
from serial import Serial
from xbeecommunications import XBeeCommunications
from housemonitor.configuration.xmlconfiguration import XmlConfiguration
from housemonitor.lib.constants import Constants


class BeagleboneBlackXbeeCommunications( XBeeCommunications, XmlConfiguration, object ):
    """
    Connect to the XBee on the beagle bone computer
    """

    def __init__( self ):
        super( BeagleboneBlackXbeeCommunications, self ).__init__()


    def setup( self ):
        """
        setup - sets up the serial line on the beaglebone board
        """
        serial_port = None

        UART.setup( self.config[Constants.XbeeConfiguration.xbee_beaglebone_black_uart] )

        port = self.config[Constants.XbeeConfiguration.xbee_beaglebone_port]
        baudrate = int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_baudrate] )
        timeout = int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_timeout] )

        serial_port = Serial( port, baudrate, timeout=timeout )
        return serial_port

    def close( self ):
        # UART.cleanup() This will cause kernal to crash
        Serial.close()

    @property
    def configuration_topic_name( self ):
        return __name__

    @property
    def configuration_file_name( self ):
        return __name__
