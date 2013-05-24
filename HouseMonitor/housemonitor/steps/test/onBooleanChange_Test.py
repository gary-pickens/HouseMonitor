'''
Created on Nov 15, 2012

@author: Gary
'''
import unittest
from housemonitor.steps.onbooleanchange import onBooleanChange
from housemonitor.steps.onbooleanchange import instantuate_me
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from housemonitor.lib.getdatetime import GetDateTime
import time


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'housemonitor.steps.onbooleanchange.Common.send' )
    def test_onBooleanChange_with_one_device_and_port( self, send ):
        device = 'device'
        port = 'port'
        Change = onBooleanChange()

        Change.config = {device: {port: False}}
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        Change.substep( True, data, listeners )
        self.assertEqual( Change.current_value[device][port], True )
        send.assert_called_once_with( True, {'device': device, 'port': port}, listeners )
        send.reset_mock()

        listeners = ['a', 'b', 'c']
        Change.substep( True, data, listeners )
        self.assertEqual( Change.current_value[device][port], True )
        send.assert_called_once_with( True, {'device': device, 'port': port}, [] )
        send.reset_mock()

        listeners = ['a', 'b', 'c']
        Change.substep( False, data, listeners )
        self.assertEqual( Change.current_value[device][port], False )
        send.assert_called_once_with( False, {'device': device, 'port': port}, ['a', 'b', 'c'] )
        send.reset_mock()

    def test_onBooleanChange_with_two_device_and_port( self ):
        N = onBooleanChange()

        listeners = ['a', 'b', 'c']
        data = {}
        device1 = 'device1'
        device2 = 'device2'
        port = 'port'

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.substep( True, data, listeners )
        self.assertEqual( N.current_value[device1][port], True )

        data[Constants.DataPacket.device] = device2
        data[Constants.DataPacket.port] = port
        N.substep( False, data, listeners )
        self.assertEqual( N.current_value[device2][port], False )
        self.assertEqual( N.current_value[device1][port], True )

    def test_onBooleanChange_with_one_device_and_two_ports( self ):
        N = onBooleanChange()

        listeners = ['a', 'b', 'c']
        data = {}
        device1 = 'device1'
        port1 = 'port1'
        port2 = 'port2'

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port1
        N.substep( True, data, listeners )
        self.assertEqual( N.current_value[device1][port1], True )

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port2
        N.substep( False, data, listeners )
        self.assertEqual( N.current_value[device1][port1], True )
        self.assertEqual( N.current_value[device1][port2], False )

    def test_onBooleanChange_if_no_device_in_data( self ):
        N = onBooleanChange()
        port = 'port'
        data = {}
        listeners = []
        data[Constants.DataPacket.port] = port
        with self.assertRaisesRegexp( KeyError, "The device is missing from the data block: 'device'" ):
            N.step( True, data, listeners )

    def test_onBooleanChange_if_no_port_in_data( self ):
        N = onBooleanChange()
        device = 'device'
        data = {}
        listeners = []
        data[Constants.DataPacket.device] = device
        with self.assertRaisesRegexp( KeyError, "The port is missing from the data block: 'port'" ):
            N.step( True, data, listeners )

    def test_instantuate_me( self ):
        data = {}
        N = instantuate_me( data )
        self.assertEqual( N.counter, 0 )

    def test_onBooleanChange_continues_after_new_entry_is_made( self ):
        device = 'device'
        port = 'port'
        N = onBooleanChange()

        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port

        listeners = ['a', 'b', 'c']
        returned_value, returned_data, returned_listeners = N.step( True, data, listeners )
        self.assertListEqual( listeners, returned_listeners )

        listeners = ['a', 'b', 'c']
        returned_value, returned_data, returned_listeners = N.step( True, data, listeners )
        self.assertListEqual( [], returned_listeners )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
