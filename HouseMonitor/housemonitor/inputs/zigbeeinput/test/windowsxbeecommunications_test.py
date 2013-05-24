'''
Created on Dec 18, 2012

@author: Gary
'''
from housemonitor.inputs.zigbeeinput.windowsxbeecommunications import WindowsXbeeCommunications
import unittest
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, patch
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from housemonitor.lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.XmlConfiguration.configure' )
    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.Serial' )
    def test_setup( self, serial, cfg ):
        port = 'COM2'
        baud = 9600
        value = 0xaa
        win = WindowsXbeeCommunications()
        win.config = {Constants.XbeeConfiguration.xbee_windows_port: port,
                      Constants.XbeeConfiguration.xbee_windows_baud: baud}
        serial.return_value = value
        return_value = win.setup()
        serial.assert_called_once_with( port, baud )
        self.assertEqual( return_value, value )

    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.XmlConfiguration.configure' )
    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.Serial.close' )
    def test_close( self, close, cfg ):
        win = WindowsXbeeCommunications()
        win.close()
        close.assert_called_once_with()

    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.XmlConfiguration.configure' )
    def test_configuration_topic_name( self, cfg ):
        win = WindowsXbeeCommunications()
        self.assertEqual( win.configuration_topic_name, 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications' )

    @patch( 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications.XmlConfiguration.configure' )
    def test_configuration_file_name( self, cfg ):
        win = WindowsXbeeCommunications()
        self.assertEqual( win.configuration_file_name, 'housemonitor.inputs.zigbeeinput.windowsxbeecommunications' )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
