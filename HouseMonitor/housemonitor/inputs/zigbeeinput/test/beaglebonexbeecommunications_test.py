'''
Created on Dec 18, 2012

@author: Gary
'''
from housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications
import unittest
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from housemonitor.lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.XmlConfiguration.configure' )
    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.Serial' )
    def test_setup( self, serial, cfg ):
        port = 'COM2'
        baud = 9600
        value = 0xaa
        bb = BeagleboneXbeeCommunications()
        bb.write_uart_configuration_setup = Mock()
        bb.config = {Constants.XbeeConfiguration.xbee_beaglebone_port: port,
                      Constants.XbeeConfiguration.xbee_beaglebone_baudrate: baud,
                      Constants.XbeeConfiguration.xbee_beaglebone_mux_mode: 'mux_mode',
                      Constants.XbeeConfiguration.xbee_beaglebone_receive_enable: '0',
                      Constants.XbeeConfiguration.xbee_beaglebone_rx_mux: 'rx_mode',
                      Constants.XbeeConfiguration.xbee_beaglebone_timeout: '10',
                      Constants.XbeeConfiguration.xbee_beaglebone_transmit_enable: '1',
                      Constants.XbeeConfiguration.xbee_beaglebone_tx_mux: 'tx_mux'
                      }
        serial.return_value = value
        return_value = bb.setup()
        bb.write_uart_configuration_setup.assert_any_call( 'tx_mux', 1 )
        self.assertEqual( bb.write_uart_configuration_setup.call_count, 2 )
        serial.assert_called_once_with( port, baud, timeout=10 )
        self.assertEqual( value, return_value )

    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.XmlConfiguration.configure' )
    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.Serial.close' )
    def test_close( self, close, cfg ):
        bb = BeagleboneXbeeCommunications()
        bb.close()
        close.assert_called_once_with()

    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.XmlConfiguration.configure' )
    def test_configuration_topic_name( self, cfg ):
        bb = BeagleboneXbeeCommunications()
        self.assertEqual( bb.configuration_topic_name, 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications' )

    @patch( 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications.XmlConfiguration.configure' )
    def test_configuration_file_name( self, cfg ):
        bb = BeagleboneXbeeCommunications()
        self.assertEqual( bb.configuration_file_name, 'housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications' )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
