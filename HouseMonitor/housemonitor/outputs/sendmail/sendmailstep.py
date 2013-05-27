'''
Created on May 24, 2013

@author: Gary
'''
from housemonitor.lib.constants import Constants
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.base import Base
from pubsub import pub

class SendMailStep( Base ):
    '''
    This object will take messages from pubsub and send them to the email thread.

    '''
    queue = None
    ''' A Queue for communicating between threads. '''

    def __init__( self, queue ):
        '''
        Initialize COSMOutputStep.

        :param queue: an object which communicates between threads
        :type queue: COSMQueue
        '''
        super( SendMailStep, self ).__init__()
        self.queue = queue
        pub.subscribe( self.sendEMailMessage, Constants.TopicNames.SendMailMessage )
        self.logger.debug( "SendMailStep started" )

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.SendMail

    def sendEMailMessage( self, **kargs ):
        """
        This function receives data that will be sent to COSM and forwards it to the COSM output processing
        thread.

        This function will compare the value with the previous value and if they are different send the data to
        the next listener else don't send the data along.

        :param **kargs: a dictionary containing where the email is coming from and the message to send.
        :type map: containing the mailing list name('list') and the message('msg')
        
        """
        self.queue.transmit( **kargs )
        self.logger.debug( "SendMailStep data transmitted to SendMail thread" )

