'''
Created on Nov 14, 2012

@author: Gary
'''
import unittest
from housemonitor.steps.oneInN import OneInN
from housemonitor.steps.oneInN import instantuate_me
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

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_oneInN_with_one_device_and_port( self, configuration ):
        N = OneInN()

        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        listeners = []
        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device][port], 1 )

        N.step( 1, data, listeners )
        self.assertEqual( N.count[device][port], 2 )

        N.step( 1, data, listeners )
        self.assertEqual( N.count[device][port], 3 )

        N = None

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_oneInN_with_two_device_and_port( self, configuration ):
        N = OneInN()

        listeners = []
        data = {}
        device1 = '0x13a200409029bf'
        device2 = '0x13a200408cccc3'
        port = 'adc-1'

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device1][port], 1 )

        data[Constants.DataPacket.device] = device2
        data[Constants.DataPacket.port] = port
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device2][port], 1 )

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device1][port], 2 )

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device1][port], 3 )

        N = None

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_oneInN_with_no_device_in_count_dict( self, configuration ):
        N = OneInN()
        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        N.count = {}
        listeners = ['a', 'b', 'c']
        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'

        data[Constants.DataPacket.port] = port
        data[Constants.DataPacket.device] = device
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device][port], 1 )

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_oneInN_with_one_device_in_count_dict_that_is_not_the_same( self, configuration ):
        device0 = 'device0'
        device1 = 'device1'
        port0 = 'port0'
        port1 = 'port1'

        N = OneInN()
        N.config = {device0: {port1: '2', port0: 10}, device1: {port0: '2', port1: '5'}}
        N.count = {device1: {port1: 10}}
        listeners = ['a', 'b', 'c']
        data = {}

        data[Constants.DataPacket.port] = port0
        data[Constants.DataPacket.device] = device0
        N.step( 1, data, listeners )
        self.assertEqual( N.count[device0][port0], 1 )
        self.assertEqual( N.count[device1][port1], 10 )

    @patch( 'housemonitor.steps.oneInN.Common.send' )
    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_oneInN_with_one_device_and_other_port_in_count_dict( self, send, configuration ):
        N = OneInN()
        GetDateTime.isoformat = Mock()
        GetDateTime.isoformat.return_value = '123'
        N.config = {'0x13a200409029bf': {'adc-1': '2', 'adc-0': 10}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        N.count = {'0x13a200409029bf': {'adc-0': 10}}
        listeners = ['a', 'b', 'c']
        data = {}
        device0 = '0x13a200409029bf'
        device1 = '0x13a200408cccc3'
        port0 = 'adc-0'
        port1 = 'adc-1'

        data[Constants.DataPacket.port] = port1
        data[Constants.DataPacket.device] = device0
        N.substep( 1, data, listeners )
        self.assertEqual( N.count[device0][port0], 10 )
        self.assertEqual( N.count[device0][port1], 1 )
        self.assertEqual( N.errors, 0 )
        self.assertEqual( N.last_error_time, None )
        self.assertEqual( N.counter, 1 )
#         self.assertEqual(N.last_count_time, '123')

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_instantuate_me( self, config ):
        data = {}
        N = instantuate_me( data )
        self.assertIsInstance( N, OneInN )

    @patch( 'housemonitor.configuration.formatconfiguration.FormatConfiguration.configure' )
    def test_configuration_file_name( self, config ):
        oin = OneInN()
        self.assertEqual( oin.configuration_file_name(), 'housemonitor.steps.oneInN' )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover


goodOneInNXml = '''<?xml version="1.0" encoding="UTF-8"?>
<formats>
    <item device="0x13a200409029bf" port="adc-1">2</item>
    <item device="0x13a200408cccc3" port="adc-0">5</item>
    <item device="0x13a200408cccc3" port="adc-1">20</item>
</formats>
'''
