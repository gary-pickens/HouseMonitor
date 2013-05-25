'''
Created on May 24, 2013

@author: Gary
'''
from housemonitor.outputs.sendmail.sendmailthread import SendMailThread
from housemonitor.lib.constants import Constants
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.base import Base
from housemonitor.outputs.sendmail.sendmailstep import SendMailStep


class SendMailControl( Base ):
    '''
    SendMailControl starts the SendMail processing to send data using email.
    
    '''
    queue = None
    send_mail_threads = []
    send_mail = None
    number_of_threads = 3

    def __init__( self ):
        '''
        Constructor
        '''
        super( SendMailControl, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsZigBee

    def startSendMail( self, options ):
        '''
        Start the ZigBee processing.

        This consists of three parts:

        #. Start the Send Mail queue which used Queue, a thread safe queue for communcating
        between threads.

        #. Start the SendMailThread which talks to the mail server.  This is a slow process.

        '''
        self.queue = HMQueue( 'SendMail' )
        self.send_mail = SendMailStep( self.queue )

        for i in range( self.number_of_threads ):
            self.send_mail_threads[i] = SendMailThread( self.queue )
            self.send_tail_thread.setDaemon( True )
            self.send_mail_threads[i].start()
