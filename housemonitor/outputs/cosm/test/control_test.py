'''
Created on Dec 10, 2012

@author: Gary
'''
import unittest
from housemonitor.outputs.cosm.control import COSMControl
from housemonitor.outputs.cosm.outputthread import COSMOutputThread
from housemonitor.outputs.cosm.outputStep import COSMOutputStep
from mock import Mock, MagicMock, patch
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from housemonitor.lib.hmqueue import HMQueue


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_startCOSM( self ):

        cont = COSMControl()
        with patch( 'housemonitor.outputs.cosm.control.HMQueue', spec=HMQueue ) as que:
            with patch( 'housemonitor.outputs.cosm.control.COSMOutputThread', spec=COSMOutputThread ) as thread:
                with patch( 'housemonitor.outputs.cosm.control.COSMOutputStep', spec=COSMOutputStep ) as op:
                    options = None
                    que.return_value = 1
                    cont.startCOSM( options )
                    que.assert_called_with( 'COSM' )
                    thread.assert_called_with( 1, None, name='COSM' )
                    self.assertTrue( op.called )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
