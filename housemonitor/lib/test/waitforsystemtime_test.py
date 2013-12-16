'''
Created on Dec 8, 2013

@author: gary
'''
import unittest
from housemonitor.lib.waitforsystemtime import WaitForSystemTime
from mock import patch, Mock
from datetime import datetime
from time import sleep


class Test( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    def test_validSystemTime( self ):
        vst = WaitForSystemTime()
        assert( vst.validSystemTime() )

    def test_not_validSystemTime( self ):
        sleep = Mock()
        vst = WaitForSystemTime( sleep=sleep )
        assert( not vst.validSystemTime( datetime( 2000, 1, 1, 0, 0, 0 ) ) )

    def test_waitForSystemTime( self ):
        vst = WaitForSystemTime()
        vst.validSystemTime = Mock( side_effect=[False, True] )
        vst.wait()
        assert vst.validSystemTime.call_count == 2


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
