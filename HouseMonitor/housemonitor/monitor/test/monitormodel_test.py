'''
Created on May 12, 2013

@author: Gary
'''
import unittest

import logging.config
from lib.constants import Constants
import pprint
from housemonitor.monitor.monitormodel import MonitorModel


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_convertToArray( self ):
        m = MonitorModel()
        m.convertToArray()
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
