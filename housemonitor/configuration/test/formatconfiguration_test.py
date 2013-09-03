'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
from housemonitor.configuration.formatconfiguration import FormatConfiguration
import datetime
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from housemonitor.lib.getdatetime import GetDateTime
from xml.etree.ElementTree import ElementTree, fromstring


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch.object( FormatConfiguration, 'configure' )
    def test_configuration_topic_name( self, configure ):
        x = FormatConfiguration()
        self.assertEqual( x.configuration_file_name, "housemonitor.configuration.formatconfiguration" )

    @patch.object( FormatConfiguration, 'configure' )
    def test_logger_name( self, configure ):
        x = FormatConfiguration()
        self.assertEqual( x.logger_name, Constants.LogKeys.configuration )

    @patch.object( FormatConfiguration, 'configure' )
    def test_process_configuration( self, configure ):
        exformat = {'0x13a200408cccc3': {'adc-0': '{:3.1f}', 'adc-1': '{:3.1f}'},
                    '0x13a200409029bf': {'adc-1': '{:3.1f}'}}
        fc = FormatConfiguration()
        et = fromstring( xml )
        config = fc.process_configuration( et )
        self.assertDictEqual( config, exformat )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


xml = '''<?xml version="1.0" encoding="UTF-8"?>
<formats>
    <item device="0x13a200409029bf" port="adc-1">{:3.1f}</item>
    <item device="0x13a200408cccc3" port="adc-0">{:3.1f}</item>
    <item device="0x13a200408cccc3" port="adc-1">{:3.1f}</item>
</formats>

'''
