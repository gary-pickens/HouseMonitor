'''
Created on Oct 10, 2012

@author: Gary
'''
import os
from serial import Serial
from xbeecommunications import XBeeCommunications
from housemonitor.configuration.xmlconfiguration import XmlConfiguration
from housemonitor.lib.constants import Constants


class BeagleboneXbeeCommunications( XBeeCommunications, XmlConfiguration, object ):
    """
    Connect to the XBee on the beagle bone computer
    """
    path = '/sys/kernel/debug/omap_mux/'

    def __init__( self ):
        super( BeagleboneXbeeCommunications, self ).__init__()

    def write_uart_configuration_setup( self, fname, mode ):
        filename = os.path.join( self.path, fname )
        with open( filename, "wb" ) as f:
            f.write( "%X" % mode )

    def setup( self ):
        """
        setup - sets up the serial line on the beaglebone board
        """
        serial_port = None

        uart1_pin_mux = \
        [
             ( self.config[Constants.XbeeConfiguration.xbee_beaglebone_rx_mux],
              int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_receive_enable] ) ),
             ( self.config[Constants.XbeeConfiguration.xbee_beaglebone_tx_mux],
              int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_transmit_enable] ) )
        ]

        for ( fname, mode ) in uart1_pin_mux:
            self.write_uart_configuration_setup( fname, mode )

        port = self.config[Constants.XbeeConfiguration.xbee_beaglebone_port]
        baudrate = int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_baudrate] )
        timeout = int( self.config[Constants.XbeeConfiguration.xbee_beaglebone_timeout] )

        serial_port = Serial( port, baudrate, timeout=timeout )
        return serial_port

    def close( self ):
        Serial.close()

    @property
    def configuration_topic_name( self ):
        return __name__

    @property
    def configuration_file_name( self ):
        return __name__
