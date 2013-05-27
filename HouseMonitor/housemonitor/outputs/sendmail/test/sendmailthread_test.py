'''
Created on May 24, 2013

@author: Gary
'''
import unittest
from housemonitor.outputs.sendmail.sendmailthread import SendMailThread
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.constants import Constants
from mock import Mock, MagicMock, patch
from housemonitor.lib.common import Common
import logging.config


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_logger_name( self ):
        queue = HMQueue()
        thread = SendMailThread( queue )
        self.assertEqual( thread.logger_name, Constants.LogKeys.SendMail )

    @patch.object( HMQueue, 'receive' )
    def test_sendMessage_with_missing_email_list_name( self, receive ):
        packet = {}
        data = {Constants.DataPacket.email_list_name: 'Garage Door Opening',
                   Constants.DataPacket.email_message: 'test'}
        data = {
                   Constants.DataPacket.email_message: 'test'}

        packet['data'] = data

        q = HMQueue()
        sm = SendMailThread( q )
        receive.return_value = packet

        with self.assertRaisesRegexp( KeyError, 'No email list name.' ):
            sm.sendMessage()

    @patch.object( HMQueue, 'receive' )
    def test_sendMessage_with_missing_email_message( self, receive ):
        packet = {}
        data = {Constants.DataPacket.email_list_name: 'Garage Door Opening',
                   Constants.DataPacket.email_message: 'test'}
        data = {Constants.DataPacket.email_list_name: 'Garage Door Opening'}

        packet['data'] = data

        q = HMQueue()
        sm = SendMailThread( q )
        receive.return_value = packet

        with self.assertRaisesRegexp( KeyError, 'No email message.' ):
            sm.sendMessage()

    @patch.object( SendMailThread, 'sendSMTPMessage' )
    @patch.object( HMQueue, 'receive' )
    def test_sendMessage( self, receive, sendSMTPMessage ):
        packet = {}
        data = {Constants.DataPacket.email_list_name: 'Garage Door Opening',
                   Constants.DataPacket.email_message: 'test'}

        packet['data'] = data

        q = HMQueue()
        sm = SendMailThread( q )
        receive.return_value = packet

        sm.sendMessage()
        sendSMTPMessage.assert_called_once_with( 'From: gary_pickens@yahoo.com\r\nTo: gary_pickens@yahoo.com, garypickens@gmail.com\r\n\r\ntest' )

    @patch( 'housemonitor.outputs.sendmail.sendmailthread.smtplib', autospec=True )
    @patch.object( HMQueue, 'receive' )
    def test_sendSMTPMessage( self, receive, smtp ):
        q = HMQueue()
        sm = SendMailThread( q )

        msg = 'test test test'
        sm.smtp_host = 'host'
        sm.smtp_port = 123
        sm.debug_level = 10
        sm.from_address = from_address = 'gary'
        sm.to_address = to = 'not gary'
        sm.password = password = 'NotPassword'
        sm.sendSMTPMessage( msg )
        print smtp.mock_calls
        smtp.SMTP_SSL.assert_called_once_with( sm.smtp_host, sm.smtp_port )
        smtp.SMTP_SSL().set_debuglevel.assert_called_once_with( 10 )
        smtp.SMTP_SSL().login.assert_called_once_with( from_address, password )
        smtp.SMTP_SSL().sendmail.assert_called_once_with( from_address, to, msg )
        smtp.SMTP_SSL().quit.assert_called_once_with()


    @patch( 'housemonitor.outputs.sendmail.sendmailthread.smtplib', autospec=True )
    @patch.object( HMQueue, 'receive' )
    def test_sendSMTPMessage_with_login_not_required( self, receive, smtp ):
        q = HMQueue()
        sm = SendMailThread( q )

        msg = 'test test test'
        sm.smtp_host = 'host'
        sm.smtp_port = 123
        sm.debug_level = 10
        sm.require_login = False
        sm.from_address = from_address = 'gary'
        sm.to_address = to = 'not gary'
        sm.password = password = 'NotPassword'
        sm.sendSMTPMessage( msg )
        print smtp.mock_calls
        smtp.SMTP_SSL.assert_called_once_with( sm.smtp_host, sm.smtp_port )
        smtp.SMTP_SSL().set_debuglevel.assert_called_once_with( 10 )
        self.assertFalse( smtp.SMTP_SSL().login.called )
        smtp.SMTP_SSL().sendmail.assert_called_once_with( from_address, to, msg )
        smtp.SMTP_SSL().quit.assert_called_once_with()

    @patch( 'housemonitor.outputs.sendmail.sendmailthread.smtplib', autospec=True )
    @patch.object( HMQueue, 'receive' )
    def test_sendSMTPMessage_exception( self, receive, smtp ):
        q = HMQueue()
        sm = SendMailThread( q )

        msg = 'test test test'
        sm.smtp_host = 'host'
        sm.smtp_port = 123
        sm.debug_level = 10
        sm.require_login = False
        sm.from_address = from_address = 'gary'
        sm.to_address = to = 'not gary'
        sm.password = password = 'NotPassword'
        smtp.SMTP_SSL().set_debuglevel.side_effect = Exception( 'Boom' )
        sm.sendSMTPMessage( msg )

        self.assertFalse( smtp.SMTP_SSL().login.called )
        self.assertFalse( smtp.SMTP_SSL().sendmail.called )
        smtp.SMTP_SSL().quit.assert_called_once_with()
        print smtp.mock_calls


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test']
    unittest.main()
