'''
Created on Mar 8, 2013

@author: Gary
'''
import unittest
from outputs.zigbee.zigbeecontrol import ZigBeeControl
from outputs.zigbee.zigbeeoutputstep import ZigBeeOutputStep
from outputs.zigbee.zigbeeoutputthread import ZigBeeOutputThread
from lib.hmqueue import HMQueue
from lib.constants import Constants
from mock import Mock, MagicMock, patch
from lib.common import Common
import logging.config


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_logger_name( self ):
        queue = HMQueue()
        zig = ZigBeeOutputStep( queue )
        self.assertEqual( Constants.LogKeys.outputsZigBee, zig.logger_name )

    def test_topic_name( self ):
        queue = HMQueue()
        zig = ZigBeeOutputStep( queue )
        self.assertEqual( Constants.TopicNames.ZigBeeOutput, zig.topic_name )

    def test_step( self ):
        value = 5
        data = {Constants.DataPacket.device: 'data',
                Constants.DataPacket.port: 'port',
                Constants.DataPacket.arrival_time: 'arrival_time'}
        listeners = ['a', 'b', 'c']
        package = {'data': data, 'value': value}
        queue = MagicMock( spec=HMQueue )
        zig = ZigBeeOutputStep( queue )
        v, d, l = zig.step( value, data, listeners )
        queue.transmit.assert_called_once_with( package, queue.three_quarters_priority )
        self.assertEqual( value, v )
        self.assertEqual( data, d )
        self.assertEqual( listeners, l )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
