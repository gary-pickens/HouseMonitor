'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, patch
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from housemonitor.lib.getdatetime import GetDateTime

from housemonitor.inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications


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
