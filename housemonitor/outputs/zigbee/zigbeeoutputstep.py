'''
Created on 2012-11-06

@author: Gary

'''
from housemonitor.steps.abc_step import abcStep
from housemonitor.lib.constants import Constants
from housemonitor.lib.hmqueue import HMQueue
import random


class ZigBeeOutputStep( abcStep ):
    '''
    This object should be started with with the COSM thread and hang around forever.

    '''
    queue = None
    ''' A Queue for communicating between threads. '''

    def __init__( self, queue ):
        '''
        Initialize COSMOutputStep.

        :param queue: an object which communicates between threads
        :type queue: COSMQueue
        '''
        super( ZigBeeOutputStep, self ).__init__()
        self.queue = queue
        self.logger.debug( "ZigBeeOutputStep started" )

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.ZigBeeOutput

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsZigBee

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
        data[Constants.DataPacket.ID] = int( random.random() * 255.0 )
        data[Constants.DataPacket.value] = value
        data[Constants.DataPacket.listeners] = listeners
        self.queue.transmit( data, self.queue.THREE_QUARTERS_PRIORITY )
        self.logger.debug( "ZigBee Step data transmitted to ZigBee thread: value = {} data = {}".format( value, data ) )
        return value, data, listeners
