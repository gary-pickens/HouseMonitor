'''
Created on Apr 12, 2013

@author: Gary
'''
import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from lib.getdatetime import GetDateTime
from inputs.computermonitor import ComputerMonitor


class Test( unittest.TestCase ):


    def setUp( self ):
        pass


    def tearDown( self ):
        pass


    def test_logger_name( self ):
        queue = MagicMock()
        cmp = ComputerMonitor( queue )
        self.assertEqual( cmp.logger_name, Constants.LogKeys.ComputerMonitor )



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_logger_name']
    unittest.main()
