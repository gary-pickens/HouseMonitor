'''
Created on Dec 18, 2012

@author: Gary
'''
import unittest
from housemonitor.configuration.sendmailconfiguration import SendMailConfiguration
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

    @patch.object( SendMailConfiguration, 'configure' )
    def test_configuration_topic_name( self, configure ):
        x = SendMailConfiguration()
        self.assertEqual( x.configuration_file_name, "housemonitor.configuration.sendmailconfiguration" )

    @patch.object( SendMailConfiguration, 'configure' )
    def test_logger_name( self, configure ):
        x = SendMailConfiguration()
        self.assertEqual( x.logger_name, Constants.LogKeys.SendMail )

    @patch.object( SendMailConfiguration, 'configure' )
    def test_process_configuration( self, configure ):
        fc = SendMailConfiguration()
        et = fromstring( xml )
        fc.process_configuration( et )
        self.assertEqual( fc.smtp_host, 'abc' )
        self.assertEqual( fc.smtp_port, 465 )
        self.assertEqual( fc.require_login, True )
        self.assertEqual( fc.from_address, 'abc@def.com' )
        self.assertEqual( fc.password, 'Not My Password' )
        self.assertListEqual( fc['Garage Door Opening'], ['com', 'org'] )
        self.assertListEqual( fc['Garage Door Closing'], ['gary_pickens@yahoo.com'] )
        self.assertListEqual( fc['Garage Door Open > 15 minutes'], ['gary_pickens@yahoo.com', 'gwpickens@hotmail.com'] )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()


xml = '''<?xml version="1.0" encoding="UTF-8"?>
<email>
    <smtp_host>abc</smtp_host>
    <smtp_port>465</smtp_port>
    <require_login>True</require_login>
    <from_address>abc@def.com</from_address>
    <password>Not My Password</password>
    <list name="Garage Door Opening">
        com,
        org
    </list>
    <list name="Garage Door Closing">
        gary_pickens@yahoo.com
    </list>
    <list name="Garage Door Open > 15 minutes">
        gary_pickens@yahoo.com,
        gwpickens@hotmail.com
    </list>
</email>
'''
