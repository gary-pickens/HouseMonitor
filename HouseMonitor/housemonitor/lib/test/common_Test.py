'''
Created on Dec 4, 2012

@author: Gary
'''
import unittest
from lib.base import Base
from lib.constants import Constants
from lib.common import Common
from pubsub import pub
from mock import *
from pprint import pprint


class Test( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_getDeviceAndPort_with_good_data( self ):
        data = {'device': 'abc',
                'port': 'def'}
        device, port = Common.getDeviceAndPort( data )
        self.assertEqual( device, 'abc' )
        self.assertEqual( port, 'def' )

    def test_getDeviceAndPort_with_missing_port( self ):
        data = {'device': 'def'}
        with self.assertRaisesRegexp( KeyError, 'The port is missing from the data block:' ):
            device, port = Common.getDeviceAndPort( data )

    def test_getDeviceAndPort_with_missing_device( self ):
        data = {'port': 'def'}
        with self.assertRaisesRegexp( KeyError, 'The device is missing from the data block:' ):
            device, port = Common.getDeviceAndPort( data )

    @patch.object( pub, 'sendMessage' )
    def test_send( self, sendMessage ):
        value = 1
        data = {'device': {'port': {'a': 'b'}}}
        listeners = ['a', 'b', 'c']
        Common.send( value, data, listeners )
        sendMessage.assert_called_once_with( 'a', value=value, data=data, listeners=['b', 'c'] )

    @patch.object( pub, 'sendMessage' )
    def test_send_with_split( self, sendMessage ):
        value = 1
        data = {'device': {'port': {'a': 'b'}}}
        listeners = [['x', 'y', 'z'], 'a', 'b', 'c']
        Common.send( value, data, listeners )
        expected_call_list = [call( 'x', listeners=['y', 'z'], data={'device': {'port': {'a': 'b'}}}, value=1 ),
                             call( 'a', listeners=['b', 'c'], data={'device': {'port': {'a': 'b'}}}, value=1 )]
        self.assertEqual( sendMessage.mock_calls, expected_call_list )

    def test_generateDevicePortTree( self ):
        values = {}
        value = ( 'a', 'b' )
        devices = ( 'device1', 'device2' )
        ports = ( 'port1', 'port2' )
        expected_values = {devices[0]: {ports[0]: value[0]}}

        added = Common.generateDevicePortTree( value[0], devices[0], ports[0], values )
        self.assertDictEqual( expected_values, values )
        self.assertTrue( added )

        # Check if no new entry was added
        added = Common.generateDevicePortTree( value[0], devices[0], ports[0], values )
        self.assertDictEqual( expected_values, values )
        self.assertFalse( added )

        # Check port
        expected_values = {devices[0]: {ports[0]: value[0], ports[1]: value[1]}}
        added = Common.generateDevicePortTree( value[1], devices[0], ports[1], values )
        self.assertDictEqual( expected_values, values )
        self.assertTrue( added )



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
