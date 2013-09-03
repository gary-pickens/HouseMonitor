'''
Created on Dec 18, 2012

@author: Gary
'''
from housemonitor.inputs.zigbeeinput.beagleboneblackxbeecommunications import BeagleboneBlackXbeeCommunications
import unittest
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from housemonitor.lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):

#    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
#        logging.config.fileConfig( "unittest_logging.conf" )
        pass

    def tearDown( self ):
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
