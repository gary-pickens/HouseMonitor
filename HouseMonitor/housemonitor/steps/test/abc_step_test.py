'''
Created on Dec 17, 2012

@author: Gary
'''
import unittest
from steps.oneInN import OneInN
from steps.oneInN import instantuate_me
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from lib.getdatetime import GetDateTime
from steps.abc_step import abcStep
from lib.common import Common


class testStep( abcStep ):

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return 'step'

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step( self, value, data, listeners ):
        pass


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "house_monitor_logging.conf" )

    def tearDown( self ):
        pass

    def test__topic_name( self ):
         s = testStep()
         self.assertEqual( s.topic_name, 'step' )

    def test__logger_name( self ):
        s = testStep()
        self.assertEqual( s.logger_name, Constants.LogKeys.steps )

    @patch( 'steps.test.abc_step_test.Common.send' )
    def test_getUseCount_when_count_is_zero( self, send ):
        device = 'device'
        port = 'port'
        N = testStep()

        N.counter = 0
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        N.getUseCount( 1, data, listeners )

    @patch( 'steps.test.abc_step_test.Common.send' )
    def test_getUseCount( self, send ):
        device = 'device'
        port = 'port'
        N = testStep()

        N.counter = 111
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        N.getUseCount( 1, data, listeners )
        N.send.assert_called_once_with( 0, {'device': device, 'port': port}, ['a', 'b', 'c'] )

    @patch( 'steps.test.abc_step_test.Common.send' )
    def test_getErrorCount( self, send ):
        device = 'device'
        port = 'port'
        N = testStep()

        N.errors = 10
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        N.getErrorCount( 1, data, listeners )
        N.send.assert_called_once_with( 0, {'device': device, 'port': port}, ['a', 'b', 'c'] )

    @patch( 'steps.test.abc_step_test.Common.send' )
    def test_getErrorCount_when_error_count_is_zero( self, send ):
        device = 'device'
        port = 'port'
        N = testStep()

        N.errors = 0
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        N.getErrorCount( 1, data, listeners )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
