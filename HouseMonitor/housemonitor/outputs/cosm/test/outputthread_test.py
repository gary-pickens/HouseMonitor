'''
Created on Mar 8, 2013

@author: Gary
'''
import unittest
from housemonitor.outputs.cosm.outputthread import COSMOutputThread
from housemonitor.configuration.xmlconfiguration import XmlConfiguration
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.outputs.cosm.send import COSMSend
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

    @patch.object( XmlConfiguration, 'configure' )
    def test_logger_name( self , config ):
        queue = HMQueue( 'COSM' )
        options = 'a'
        thread = COSMOutputThread( options, queue )
        self.assertEqual( thread.logger_name, Constants.LogKeys.outputsCOSM )

    @patch( 'housemonitor.outputs.cosm.outputthread.COSMSend' )
    def test_init( self, send ):
        options = 'a'
        queue = 'q'
        thread = COSMOutputThread( queue, options )
        send.assert_called_once_with( options )
        self.assertEqual( thread._queue, 'q' )

    @patch( 'housemonitor.outputs.cosm.outputthread.COSMSend' )
    def test_init_with_send( self, send ):
        options = 'a'
        queue = 'q'
        thread = COSMOutputThread( queue, options, send='s' )
        self.assertEqual( thread._cosm_send, 's' )
        self.assertEqual( thread._queue, 'q' )

    @patch( 'housemonitor.outputs.cosm.outputthread.COSMSend' )
    def test_run( self, send ):
        options = 'a'
        data = {}
        queue = MagicMock()
        packet = {Constants.Cosm.packet.current_value: 1,
                  Constants.Cosm.packet.data: data}
        thread = COSMOutputThread( queue, options )
        thread._queue.receive = MagicMock( return_value=packet )
        thread._cosm_send.empty_datastream_list = MagicMock()
        thread._cosm_send.output = MagicMock()
        thread.process()
        thread._queue.receive.assert_called_once_with()
#        thread._cosm_send.empty_datastream_list.assert_called_once_with()
        thread._cosm_send.output.assert_called_once_with( data )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
