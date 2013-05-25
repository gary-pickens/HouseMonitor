'''
Created on May 24, 2013

@author: Gary
'''
from housemonitor.steps.abc_step import abcStep
from housemonitor.lib.constants import Constants
from housemonitor.lib.hmqueue import HMQueue

class SendMailStep( object ):
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
        self.logger.debug( "SendMailStep started" )

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.SendMailMessage

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.SendMail

    def step( self, value, data={}, listeners=[] ):
        """
        This function receives data that will be sent to COSM and forwards it to the COSM output processing
        thread.

        This function will compare the value with the previous value and if they are different send the data to
        the next listener else don't send the data along.

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        :raises: ValueError, KeyError
        
        """
        packet = {'data': data, 'value': value}
        self.queue.transmit( packet, self.queue.three_quarters_priority )
        self.logger.debug( "SendMailStep data transmitted to SendMail thread" )
        return value, data, listeners

