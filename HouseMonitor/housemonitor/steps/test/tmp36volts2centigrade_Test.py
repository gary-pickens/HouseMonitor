'''
Created on Nov 16, 2012

@author: Gary
'''
import unittest
from housemonitor.steps.tmp36volts2centigrade import ConvertTMP36VoltsToCentigrade
from housemonitor.steps.tmp36volts2centigrade import instantuate_me
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock
from housemonitor.lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_at_0C( self ):
        data = {}
        tmp2C = instantuate_me( data )
        listeners = []
        data = {}
        value, data, listeners = tmp2C.step( 1.0, data, listeners )
        self.assertAlmostEqual( value, 50.0, 2 )

    def test_at_50C( self ):
        tmp2C = ConvertTMP36VoltsToCentigrade()
        value = 0.0
        listeners = []
        data = {}
        value, data, listeners = tmp2C.step( value, data, listeners )
        self.assertAlmostEqual( value, -50.0, 2 )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
