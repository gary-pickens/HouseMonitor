'''
Created on Mar 8, 2013

@author: Gary
'''
import unittest
from housemonitor.outputs.zigbee.zigbeeoutputthread import ZigBeeOutputThread
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
        queue = HMQueue()
        thread = ZigBeeOutputThread( queue, 1 )
        self.assertEqual( thread.logger_name, Constants.LogKeys.outputsZigBee )

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutputthread.time.sleep' )
    @patch( 'housemonitor.outputs.zigbee.zigbeeoutputthread.ZigBeeOutput' )
    def test_ZigBeeOutput_throws_exception( self, zo, t ):
        queue = HMQueue()
        thread = ZigBeeOutputThread( queue , 1 )
        zo.side_effect = KeyError( 'boom' )
        thread.zigbeeConnect()
        self.assertFalse( thread.connected )
        self.assertFalse( thread.talking )

#    @patch('outputs.zigbee.zigbeeoutputthread.ZigBeeOutput.connect')
#    @patch('outputs.zigbee.zigbeeoutputthread.time.sleep')
#    @patch('outputs.zigbee.zigbeeoutputthread.ZigBeeOutput.startCorrectZigbee')
#    def test_startCorrectZigbee_throws_exception(self, zo, t, co):
#        queue = HMQueue()
#        thread = ZigBeeOutputThread(queue)
#        co.side_effect = KeyError('boom')
#        thread.zigbeeConnect()
#        zo.assert_called_once_with()
#        self.assertFalse(thread.connected)
#        self.assertFalse(thread.talking)

    @patch( 'housemonitor.outputs.zigbee.zigbeeoutputthread.HMQueue.receive' )
    def test_processCommandToZigBee( self, qr ):
        packet = {}
        queue = HMQueue()
        value = 555
        data = {}
        packet['value'] = value
        packet['data'] = data
        packet['id'] = 0xab
        thread = ZigBeeOutputThread( queue, 1 )
        qr.return_value = packet
        thread.zigbee_output = MagicMock()
        thread.zigbee_output.sendCommand = MagicMock()
        thread.connected = True
        thread.talking = True
        thread.done = False
        thread.processCommandToZigBee()
        thread.zigbee_output.sendCommand.assert_called_once_with( **packet )
        self.assertTrue( thread.connected )
        self.assertTrue( thread.talking )
        thread.done = False

    def test_processCommandToZigBee_with_IOError_in_SendCommand( self ):
        queue = HMQueue()
        packet = 555
        thread = ZigBeeOutputThread( queue, 1 )
        thread.output_queue = MagicMock()
        thread.output_queue.receive = MagicMock()
        thread.connected = True
        thread.talking = True
        thread.done = False
        thread.zigbee_output = MagicMock()
        thread.zigbee_output.sendCommand = MagicMock( side_effect=IOError() )
        thread.processCommandToZigBee()
        self.assertFalse( thread.connected )
        self.assertFalse( thread.talking )
        self.assertFalse( thread.done )

    def test_processCconnectAndProcessZigBeeCommands( self ):
        queue = HMQueue()
        packet = 555
        thread = ZigBeeOutputThread( queue, 1 )
        thread.connected = False
        thread.talking = True
        thread.done = False
        thread.zigbeeConnect = MagicMock( return_value=True )
        thread.processCommandToZigBee = MagicMock( side_effect=KeyboardInterrupt )
        thread.connectAndProcessZigBeeCommands()
        thread.zigbeeConnect.assert_called_once_with()
        thread.zigbeeConnect.assert_called_once_with()
        self.assertTrue( thread.connected )
        self.assertTrue( thread.talking )
        self.assertFalse( thread.done )

    def test_run( self ):
        queue = HMQueue()
        packet = 555
        thread = ZigBeeOutputThread( queue, 1 )
        thread.connectAndProcessZigBeeCommands = MagicMock()
        thread.run()
        thread.connectAndProcessZigBeeCommands.assert_called_once_with()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
