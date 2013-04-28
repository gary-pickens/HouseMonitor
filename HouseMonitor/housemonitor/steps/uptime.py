'''
Created on Mar 6, 2013


@author: Gary

'''
from datetime import datetime, timedelta
from lib.common import Common
from lib.constants import Constants
from pubsub import pub
from steps.abc_step import abcStep


def instantuate_me( data ):
    ''' This function will be called to instantiate this class. '''
    return uptime( data )


class uptime( abcStep ):
    '''

    '''

    start_time = None
    update_interval = 4

    def __init__( self, data ):
        '''
        '''
        super( uptime, self ).__init__()
        self.start_time = data[Constants.GlobalIndexs.start_time]
        pub.subscribe( self.schedulerRegistration, Constants.TopicNames.RegistrationScheduler )

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.UpTime

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def schedulerRegistration( self ):
        name = Constants.SchedulerName.Uptime_update
        device = 'HouseMonitor'
        port = 'uptime'
        listeners = [Constants.TopicNames.UpTime, Constants.TopicNames.CurrentValueStep]
        args = name, device, port, listeners
        pub.sendMessage( Constants.TopicNames.SchedulerAddIntervalStep, name=name, seconds=self.update_interval, args=args )
        self.logger.debug( 'Succcessfully scheduled uptime update' )

    def step( self, value, data={}, listeners=[] ):
        """
        This function will ... .

        :param value: Not used
        :type value: Boolean
        :param data: a dictionary containing more information about the value. 
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: Boolean, dict, listeners

        """
        delta = datetime.utcnow() - self.start_time
        value = str( delta ).split( '.' )[0]
        self.logger.debug( 'uptime = {}'.format( value ) )
        return value, data, listeners
