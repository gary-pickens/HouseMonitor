'''
Created on Mar 6, 2013


@author: Gary

'''
from lib.common import Common
from lib.constants import Constants
from steps.abc_step import abcStep
from datetime import datetime
from datetime import timedelta


def instantuate_me(data):
    ''' This function will be called to instantiate this class. '''
    return uptime(data)


class uptime(abcStep):
    '''

    '''

    start_time = None

    def __init__(self, data):
        '''
        '''
        super(uptime, self).__init__()
        self.start_time = data[Constants.GlobalIndexs.start_time]

    @property
    def topic_name(self):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.UpTime

    @property
    def logger_name(self):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step(self, value, data={}, listeners=[]):
        """
        This function will ... .

        Args:
            value: ...
            data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

                date time received: time when value was received.
                units: units of the number
                name: name assigned to the value
                etc.
            listeners: a list of the subscribed routines to send the data to
        Returns:
            ...
        Raises:
            ...
        """
        delta = datetime.utcnow() - self.start_time
        value = str(delta).split('.')[0]
        self.logger.debug('uptime = {}'.format(value))
        return value, data, listeners
