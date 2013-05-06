'''
Created on Dec 17, 2012

@author: Gary
'''
import unittest
from steps.centigrade2fahrenheit import ConvertCentigradeToFahrenheit
from steps.centigrade2fahrenheit import instantuate_me
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock
from lib.getdatetime import GetDateTime


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_boiling_point( self ):
        data = {}
        c2f = instantuate_me( data )
        listeners = []
        value, data, listeners = c2f.step( 100.0, data, listeners )
        self.assertAlmostEqual( value, 212.0, 2 )

    def test_freezing_point( self ):
        data = {}
        c2f = instantuate_me( data )
        listeners = []
        value, data, listeners = c2f.step( 0.0, data, listeners )
        self.assertAlmostEqual( value, 32.0, 2 )

    def test_logger_name( self ):
        data = {}
        c2f = instantuate_me( data )
        self.assertEqual( c2f.logger_name, Constants.LogKeys.steps )

    def test_topic_name( self ):
        data = {}
        c2f = ConvertCentigradeToFahrenheit()
        self.assertEqual( c2f.topic_name, Constants.TopicNames.Centigrade2FahrenheitStep )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
