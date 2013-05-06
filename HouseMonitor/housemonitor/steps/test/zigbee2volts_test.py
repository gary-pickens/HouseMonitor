'''
Created on Dec 18, 2012

@author: Gary
'''
from steps.zigbee2volts import ZigbeeCountToVolts

import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from lib.getdatetime import GetDateTime
from steps.zigbee2volts import ZigbeeCountToVolts
from steps.zigbee2volts import instantuate_me


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_convert_count_of_0_to_volts( self ):
        z = ZigbeeCountToVolts()
        data = {}
        listeners = ['a', 'b']
        data = {'device': 'a', 'port': 'b'}
        value, data, listeners = z.step( 0, data, listeners )
        self.assertAlmostEqual( value, 0, 2 )

    def test_convert_count_of_100_to_volts( self ):
        z = ZigbeeCountToVolts()
        data = {}
        listeners = ['a', 'b']
        data = {'device': 'a', 'port': 'b'}
        value, data, listeners = z.step( 100, data, listeners )
        self.assertAlmostEqual( value, 0.1171875, 2 )

    def test_topic_name( self ):
        z = ZigbeeCountToVolts()
        self.assertEqual( z.topic_name, Constants.TopicNames.ZigbeeAnalogNumberToVoltsStep )

    def test_logger_name( self ):
        z = ZigbeeCountToVolts()
        self.assertEqual( z.logger_name, Constants.LogKeys.steps )

    def test_instantuate_me( self ):
        data = {}
        z = instantuate_me( data )
        self.assertIsInstance( z, ZigbeeCountToVolts )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
