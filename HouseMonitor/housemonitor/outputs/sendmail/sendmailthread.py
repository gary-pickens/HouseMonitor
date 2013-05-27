'''
Created on May 24, 2013

@author: Gary
'''
import threading
import time
import logging
import smtplib
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib import constants
from housemonitor.lib.base import Base
from housemonitor.configuration.sendmailconfiguration import SendMailConfiguration


class SendMailThread( SendMailConfiguration, threading.Thread ):
    '''
    This class will send a message via email on when some event happens.
    '''

    output_queue = None
    done = False
    connected = False
    talking = True

    smtp_host = 'smtp.mail.yahoo.com'
    smtp_port = 465
    require_login = True
    from_address = 'gary_pickens@yahoo.com'
    password = '6a9k3Td8Xb'
    to_address = ['gary_pickens@yahoo.com', 'garypickens@gmail.com']
    debug_level = 0

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the xbee output Queue

        '''
        super( SendMailThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue

    @property
    def logger_name( self ):
        return Constants.LogKeys.SendMail


    def sendSMTPMessage( self, msg ):
        server = None
        try:
            server = smtplib.SMTP_SSL( self.smtp_host, self.smtp_port )
            server.set_debuglevel( self.debug_level )
            if self.require_login:
                server.login( self.from_address, self.password )
            server.sendmail( self.from_address, self.to_address, msg )
        except Exception as ex:
            self.logger.exception( 'Exception raised in {} '.format( ex ) )
        finally:
            if server != None:
                server.quit()
            server = None

    def sendMessage( self ):
        packet = self.output_queue.receive()

        data = packet['data']

        if Constants.DataPacket.email_list_name in data:
            email_list_name = data[Constants.DataPacket.email_list_name]
        else:
            raise KeyError( 'No email list name' )

        if Constants.DataPacket.email_message in data:
            email_message = data[Constants.DataPacket.email_message]
        else:
            raise KeyError( 'No email message' )

        msg = ( "From: {}\r\nTo: {}\r\n\r\n{}".format( self.from_address, ", ".join( self.to_address ), email_message ) )

        self.sendSMTPMessage( msg )



    def run( self ):
        self.sendMessage()
