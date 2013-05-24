'''
Created on Dec 17, 2012

@author: Gary
'''
import unittest
from housemonitor.lib.getdatetime import GetDateTime
import logging.config
from mock import Mock, patch
import datetime


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'lib' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_initializing_datetime( self ):
        dt = datetime.datetime( 2012, 11, 10, 9, 8, 7 )
        gdt = GetDateTime( date_time_value=dt )
        self.assertEqual( gdt.datetime(), dt )
        self.assertEqual( gdt.isoformat(), '2012-11-10T09:08:07' )

    def test_str( self ):
        gdt = GetDateTime()
        gdt.dt = datetime.datetime( 2012, 11, 10, 01, 02, 03 )
        self.assertEqual( str( gdt ), "2012/11/10 01:02:03" )

    def test_toString( self ):
        gdt = GetDateTime()
        gdt.dt = datetime.datetime( 2012, 11, 10, 01, 02, 03 )
        self.assertEqual( gdt.toString(), "2012/11/10 01:02:03" )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_utc_now']
    unittest.main()    # pragma: no cover
