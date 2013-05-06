'''
Created on Mar 13, 2013

@author: Gary
'''
import unittest
import datetime
import logging.config
from datetime import timedelta
from datetime import datetime
import Queue
from mock import Mock
import time
from lib.hmqueue import HMQueue
from lib.constants import Constants
from inputs.dataenvelope import DataEnvelope
from pubsub import pub
from mock import MagicMock, Mock, patch


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_logger_name( self ):
        que = HMQueue()
        self.assertEqual( que.logger_name, Constants.LogKeys.lib )

    def test_receive( self ):
        packet = {'a': 'b'}
        value = 11
        que = HMQueue()
        priority = que.mid_priority
        que._queue.get = Mock( return_value=( priority, value ) )
        ret = que.receive()
        que._queue.get.assert_called_once_with()
        self.assertEqual( value, ret )

    def test_clear( self ):
        que = HMQueue()
        que._queue.get = Mock( side_effect=Queue.Empty )
        que.clear()
        que._queue.get.assert_called_once_with( False )

    def test_transmit( self ):
        packet = {'a': 'b'}
        value = 11
        que = HMQueue()
        que._queue.put = Mock()
        que.transmit( packet )
        que._queue.put.assert_called_once_with( ( que.mid_priority, packet ) )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
