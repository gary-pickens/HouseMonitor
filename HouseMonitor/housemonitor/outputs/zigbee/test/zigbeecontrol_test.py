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
        logging.config.fileConfig( "house_monitor_logging.conf" )

    def tearDown( self ):
        pass

    def test_logger_name( self ):
        zig = ZigBeeControl()
        self.assertEqual( Constants.LogKeys.outputsZigBee, zig.logger_name )

    @patch( 'outputs.zigbee.zigbeecontrol.HMQueue', spec=HMQueue )
    @patch( 'outputs.zigbee.zigbeecontrol.ZigBeeOutputThread', spec=ZigBeeOutputThread )
    @patch( 'outputs.zigbee.zigbeecontrol.ZigBeeOutputStep', spec=ZigBeeOutputStep )
    def test_start_zigbee( self, step, thread, queue ):
        # setup
        options = 1
        cont = ZigBeeControl()
        queue.return_value = 1

        # run
        cont.startZigBee( options )

        # test
        queue.assert_called_with( 'ZigBeeInput' )
        thread.assert_called_with( 1 )
        step.assert_called_with( 1 )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
