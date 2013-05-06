'''
Created on Dec 10, 2012

@author: Gary
'''
import unittest
from outputs.cosm.control import COSMControl
from outputs.cosm.outputthread import COSMOutputThread
from outputs.cosm.outputStep import COSMOutputStep
from mock import Mock, MagicMock, patch
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from lib.hmqueue import HMQueue


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_startCOSM( self ):

        cont = COSMControl()
        with patch( 'outputs.cosm.control.HMQueue', spec=HMQueue ) as que:
            with patch( 'outputs.cosm.control.COSMOutputThread', spec=COSMOutputThread ) as thread:
                with patch( 'outputs.cosm.control.COSMOutputStep', spec=COSMOutputStep ) as op:
                    options = None
                    que.return_value = 1
                    cont.startCOSM( options )
                    que.assert_called_with( 'COSM' )
                    thread.assert_called_with( 1, None, name='COSM' )
                    self.assertTrue( op.called )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
