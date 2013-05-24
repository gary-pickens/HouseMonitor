'''
Created on Jan 17, 2013


@author: Gary

'''
from housemonitor.lib.common import Common
from housemonitor.lib.constants import Constants
from abc_step import abcStep


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return MaxValue()


class MaxValue( abcStep ):
    '''

    '''

    max_value = {}

    def __init__( self ):
        '''
        '''
        super( MaxValue, self ).__init__()

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.MaxValue

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        This function will record the max value.

        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param data: a dictionary containing more information about the value. 
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: float, dict, listeners
        :raises: ValueError, KeyError
        
        """
        device, port = Common.getDeviceAndPort( data )
        Common.generateDevicePortTree( value, device, port, self.max_value )

        if value > self.max_value[device][port]:
            self.max_value[device][port] = value

        return value, data, listeners
