'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch
from lib.getdatetime import GetDateTime
from configuration.formatconfiguration import FormatConfiguration
from lib.getdatetime import GetDateTime

from inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def testName( self ):
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
