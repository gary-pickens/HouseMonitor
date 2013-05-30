'''
Created on Dec 10, 2012

@author: Gary
'''
import unittest
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.outputs.cosm.outputStep import COSMOutputStep
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'housemonitor.outputs.cosm.control.HMQueue', spec=HMQueue )
    def test_step( self, que ):
        value = 5252
        data = {'device': 'device', 'port': 'port'}
        listeners = ['a', 'b']
        cs = COSMOutputStep( que )
        new_value, new_data, new_listeners = cs.step( value, data, listeners )
        que.transmit.assert_called_once_with( {'current_value': value, 'data': data} )
        self.assertEqual( new_value, value )
        self.assertEqual( new_data, data )
        self.assertEqual( new_listeners, listeners )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
