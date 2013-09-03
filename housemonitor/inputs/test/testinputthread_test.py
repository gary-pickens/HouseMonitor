'''
Created on Dec 10, 2012

@author: Gary
'''
import unittest
from housemonitor.inputs.testinputthead import SendGarageDoorData, TestInputThread
from housemonitor.inputs.dataenvelope import DataEnvelope
from mock import Mock, MagicMock, patch
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from housemonitor.lib.hmqueue import HMQueue
import datetime
import time


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_SendGarageDoorData_send( self ):
        queue = MagicMock()
        cs = SendGarageDoorData( queue )
        cs.send()
        self.assertTrue( queue.transmit.called )
        queue.transmit.reset_mock()
        cs.send()
        self.assertTrue( queue.transmit.called )

    def test_SendGarageDoorData_send_with_high_temperature( self ):
        queue = MagicMock()
        cs = SendGarageDoorData( queue )
        cs._current_temperature = 901
        cs.send()
        self.assertLess( cs._current_temperature, cs._high_temperature )

    def test_logger_name( self ):
        queue = MagicMock()
        th = TestInputThread( queue )
        self.assertEqual( th.logger_name, Constants.LogKeys.inputs )

    @patch( 'housemonitor.inputs.testinputthead.SendGarageDoorData.send' )
    def test_TestInputThread( self, sg ):
        queue = MagicMock()
        th = TestInputThread( queue )
        time.sleep = Mock( side_effect=KeyboardInterrupt )
        th.run()
        sg.assert_called_once_with()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
