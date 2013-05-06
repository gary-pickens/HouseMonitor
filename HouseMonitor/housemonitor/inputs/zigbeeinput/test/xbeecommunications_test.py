'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from lib.getdatetime import GetDateTime
from configuration.formatconfiguration import FormatConfiguration
from lib.getdatetime import GetDateTime

from inputs.zigbeeinput.xbeecommunications import XBeeCommunications
from xbee.zigbee import ZigBee


class myClass( XBeeCommunications ):

    def setup( self ):
        pass


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_read( self ):
        d = {'device': 'abc', 'port': 'def'}
        xbee = myClass()
        xbee.zigbee = MagicMock( spec=ZigBee )
        xbee.zigbee.wait_read_frame.return_value = d
        value = xbee.read()
        xbee.zigbee.wait_read_frame.assert_called_once_with()
        self.assertDictEqual( value, d )

    @patch( 'inputs.zigbeeinput.xbeecommunications.ZigBee' )
    def test_successful_connect( self, zigbee ):
        rv = 55
        xbee = myClass()
        xbee.delay = 0
        xbee.setup = MagicMock()
        xbee.setup.return_value = rv

        xbee.connect()
        xbee.setup.assert_called_once_with()
        zigbee.assert_called_once_with( rv )

    count = 0

    def side_effect( self ):
        if self.count == 0:
            self.count += 1
            raise IOError( "OhOh" )
        else:
            self.count += 1
            return 55

    @patch( 'inputs.zigbeeinput.xbeecommunications.ZigBee' )
    def test_fail_to_connect_first_time_then_succeed_second_time( self, zigbee ):
        rv = 55
        xbee = myClass()
        xbee.setup = MagicMock( side_effect=self.side_effect )
        xbee.setup.return_value = rv
        xbee.delay = 0

        xbee.connect()
        xbee.setup.assert_any_call()
        zigbee.assert_called_once_with( rv )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
