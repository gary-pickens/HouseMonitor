'''
Created on Nov 15, 2012


@author: Gary

'''
from housemonitor.lib.constants import Constants
from abc_step import abcStep
from housemonitor.lib.common import Common
from copy import copy


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return onBooleanChange()


class onBooleanChange( abcStep ):
    '''
    This module will receive the current value and if it is different than the previous value pass it on.

    '''
    current_value = {}
    ''' A dictionary that contains the last value read. '''

    def __init__( self ):
        '''
        Constructor
        '''
        super( onBooleanChange, self ).__init__()
        self.current_value = {}

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.onBooleanChangeStep

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step( self, value, data={}, listeners=[] ):
        """
        This function will compare the value with the previous value and if they are different send the data to
        the next listener else don't send the data along.

        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param data: a dictionary containing more information about the value. 
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: float, dict, listeners
        :Raises: ValueError, KeyError

        """

        device, port = Common.getDeviceAndPort( data )

        new_entry = Common.generateDevicePortTree( value, device, port, self.current_value )

        if ( ( value == self.current_value[device][port] ) and not new_entry ):
            listeners = []
            self.logger.debug( 'No change detected: steps discontinued: device = {} port = {} volue = {} previous value = {}'.format( device, port, value, self.current_value[device][port] ) )
        else:
            self.logger.debug( 'Change detected: continue stepping device = {} port = {} volue = {} previous value = {}'.format( device, port, value, self.current_value[device][port] ) )

        self.current_value[device][port] = value
        return value, data, listeners
