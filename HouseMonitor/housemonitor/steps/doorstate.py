'''
Created on Aug 6, 2012

@author: Gary
'''
from abc_step import abcStep
from lib.constants import Constants
from lib.common import Common
from copy import copy
from datetime import datetime, timedelta
import time


def instantuate_me( data ):
    return ConvertGarageDoorState()


class ConvertGarageDoorState( abcStep ):
    '''
    Convert the boolean value returned by the XBee for the state of the
    garage door to open or closed.
    '''

    @property
    def topic_name( self ):
        """ The topic name to which this routine subscribes."""
        return Constants.TopicNames.GarageDoorStateStep

    @property
    def logger_name( self ):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.steps

    smuggen_before = timedelta( milliseconds=1000 )

    def step( self, value, data={}, listeners=[] ):
        """
        Convert the boolean garage door state from 0 and 1 to open and
        closed

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the value.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        :raises:  ValueError, KeyError

        """
        state = ''
        self.send_old_values( value, data, listeners )

        if ( value == False ):
            state = "open"
            value = "0"
        elif( value == True ):
            state = "closed"
            value = "1"
        else:
            value = -1
            state = 'invalid'
            self.logger.warn( "invalid state %d", value )
        data[Constants.DataPacket.units] = state
        self.logger.info( "new door state is {} {} {}".format( value, data[Constants.DataPacket.units], listeners ) )
        return value, data, listeners

    def send_old_values( self, value, data, listeners ):
        new_data = copy( data )
        new_listeners = copy( listeners )
        if ( value == False ):
            new_data[Constants.DataPacket.units] = "closed"
            new_data[Constants.DataPacket.arrival_time] = new_data[Constants.DataPacket.arrival_time] - self.smuggen_before
            new_value = "1"
        elif( value == True ):
            new_data[Constants.DataPacket.units] = "open"
            new_data[Constants.DataPacket.arrival_time] = new_data[Constants.DataPacket.arrival_time] - self.smuggen_before
            new_value = "0"
        else:
            new_value = -1
            new_data[Constants.DataPacket.units] = 'invalid'
            self.logger.warn( "invalid state %d", value )
        self.logger.info( "prior door state was {} {} {}".format( new_value, new_data[Constants.DataPacket.units], listeners ) )
        try:
            Common.send( new_value, new_data, new_listeners )
        except Exception as ex:
            self.logger.exception( 'Common.send error {}'.format( ex ) )
