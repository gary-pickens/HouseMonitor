'''
Created on Mar 8, 2013

@author: Gary
'''
import unittest
from housemonitor.outputs.zigbee.zigbeeoutput import ZigBeeOutput
from housemonitor.outputs.zigbee.zigbeecontrol import ZigBeeControl
from housemonitor.outputs.zigbee.zigbeeoutputstep import ZigBeeOutputStep
from housemonitor.outputs.zigbee.zigbeeoutputthread import ZigBeeOutputThread
from housemonitor.inputs.zigbeeinput.windowsxbeecommunications import WindowsXbeeCommunications
from housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications
from housemonitor.inputs.zigbeeinput.xbeecommunications import XBeeCommunications
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.constants import Constants
from mock import Mock, MagicMock, patch
from housemonitor.lib.common import Common
import logging.config
from xbee import ZigBee


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_logger_name( self ):
        out = ZigBeeOutput()
        self.assertEqual( out.logger_name, Constants.LogKeys.outputsZigBee )

#    @patch('housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications)
#    def test_setLow(self, win):
#        destination_address = 0x13a20040902a02
#        port = 'DIO-1'
#        ot = ZigBeeOutput()
#  #        ot.communication_module['nt'] = MagicMock()
#        ot.startCorrectZigbee(os_name='nt')
#        ot.setLow(destination_address, port)

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_0_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-0'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D0',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_1_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-1'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D1',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_2_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-2'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D2',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_3_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-3'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D3',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_4_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-4'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D4',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_5_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-5'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D5',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_6_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-6'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D6',
                                                    parameter='\x04',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_7_Low( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-7'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( False, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( dest_addr_long='\x00\x13\xa2\x00@\x90*\x02',
                                                    parameter='\x04',
                                                    command='D7',
                                                    frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_0_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-0'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D0',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_1_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-1'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D1',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_2_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-2'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D2',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_3_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-3'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D3',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_4_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-4'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D4',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_5_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-5'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D5',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_6_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-6'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D6',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02', frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_set_DIO_7_High( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-7'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( True, data, id=0xaa )
        ot.zigbee.remote_at.assert_called_once_with( command='D7',
                                                    parameter='\x05',
                                                    dest_addr_long='\x00\x13\xa2\x00@\x90*\x02',
                                                    frame_id='\xaa' )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_no_device( self, win ):
        data = {}
        data[Constants.DataPacket.port] = 'DIO-7'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        with self.assertRaisesRegexp( KeyError, 'The device is missing from the data block:.*' ):
            ot.sendCommand( True, data, id=0xaa )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_no_port( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        with self.assertRaisesRegexp( KeyError, "The port is missing from the data block: .*" ):
            ot.sendCommand( True, data, id=0xaa )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_invalid_device( self, win ):
        data = {}
        data[Constants.DataPacket.device] = 'xxxxxxxxxx'
        data[Constants.DataPacket.port] = 'DIO-7'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        with self.assertRaisesRegexp( ValueError, "invalid literal for int.. with base 16:.*" ):
            ot.sendCommand( True, data, id=0xaa )

    #  TODO work more on this
    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_invalid_port( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-9'
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        with self.assertRaisesRegexp( KeyError, "DIO-9" ):
            ot.sendCommand( True, data, id=0xaa )

    #  TODO work more on this
#    @patch('housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications)
#    def test_invalid_value(self, win):
#        data = {}
#        data[Constants.DataPacket.device] = '0x13a20040902a02'
#        data[Constants.DataPacket.port] = 'DIO-7'
#        ot = ZigBeeOutput()
#        ot.zigbee = MagicMock()
#        ot.zigbee.remote_at = MagicMock()
#        with self.assertRaisesRegexp(KeyError, ""):
#            ot.sendCommand('', data)

    #  TODO work more on this
    @patch( 'housemonitor.outputs.zigbee.zigbeeoutput.WindowsXbeeCommunications', spec=WindowsXbeeCommunications )
    def test_pack_and_unpack( self, win ):
        data = {}
        data[Constants.DataPacket.device] = '0x13a20040902a02'
        data[Constants.DataPacket.port] = 'DIO-7'
        value = 1
        ot = ZigBeeOutput()
        ot.zigbee = MagicMock()
        ot.zigbee.remote_at = MagicMock()
        ot.sendCommand( value, data, id=0xaa )


if __name__ == "__main__":
    #  import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
