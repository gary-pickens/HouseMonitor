'''
Created on Dec 18, 2012

@author: Gary
'''
from steps.formatvalue import FormatValue

import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from lib.getdatetime import GetDateTime
from steps.formatvalue import FormatValue
from steps.formatvalue import instantuate_me


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_step( self, config ):
        listeners = ['a', 'b', 'c']

        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        fv = FormatValue()
        fv.config = {'0x13a200409029bf': {'adc-1': '{:.2f}'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}

        value, data, listeners = fv.step( 1.1111111, data, listeners )
        self.assertEqual( value, '1.11' )

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_step_with_value_error( self, config ):
        listeners = ['a', 'b', 'c']

        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        fv = FormatValue()
        fv.config = {'0x13a200409029bf': {'adc-1': '{:.2a}'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}

        with self.assertRaisesRegexp( ValueError, 'The format is incompatable with the input data type {:.2a}: device 0x13a200409029bf port adc-1 file steps.formatvalue: error message Unknown format code .a. for object of type .float.' ):
            value, data, listeners = fv.step( 1.1111111, data, listeners )

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_topic_name( self, config ):
        fv = FormatValue()
        self.assertEqual( fv.topic_name, Constants.TopicNames.FormatValueStep )

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_logger_name( self, config ):
        fv = FormatValue()
        self.assertEqual( fv.logger_name, Constants.LogKeys.steps )

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_configuration_file_name( self, config ):
        fv = FormatValue()
        self.assertEqual( fv.configuration_file_name, 'steps.formatvalue' )

    @patch( 'steps.formatvalue.FormatConfiguration.configure' )
    def test_instantuate_me( self, config ):
        data = {}
        N = instantuate_me( data )
        self.assertEqual( N.counter, 0 )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
