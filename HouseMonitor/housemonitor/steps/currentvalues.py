'''
Created on Nov 7, 2012

@author: Gary

'''
import copy
from lib.base import Base
from lib.constants import Constants
from lib.currentvalues import CurrentValues
from abc_step import abcStep
import pprint
from lib.common import Common


def instantuate_me(data):
    ''' This function will be called to instantiate this class. '''
    return CurrentValues(data)


class CurrentValues(abcStep):
    '''
    Store the current values using the lib.currentvalues object.  This stores the
    data in a thread safe structure.

    '''

    current_values = None
    ''' A reference to lib.currentvalues object. '''

    def __init__(self, data):
        '''
        '''
        super(CurrentValues, self).__init__()
        if 'current values' in data:
            self.current_values = data['current values']

    @property
    def topic_name(self):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.CurrentValueStep

    @property
    def logger_name(self):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step(self, value, data={}, listeners=[]):
        """
        Store the current value.

        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

               | 1. **date:** time received: time when value was received.
               | 2. **units:** units of the number
               | 3. **name:** name assigned to the value
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: value, dict, listeners
        :Raises: ValueError, KeyError
        """
        device, port = Common.getDeviceAndPort(data)

        current_data = self.current_values.buildDataBlock(value, data)
        self.current_values.store(value, device, port, current_data)
        self.logger.debug("currentvalue table {} {} {}".format(device, port, value))
#        pprint.pprint(self.current_values.get())
        return value, data, listeners
