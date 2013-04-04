'''
Created on Oct 16, 2012

@author: Gary

'''
from lib.constants import Constants
from configuration.formatconfiguration import FormatConfiguration
from lib.base import Base
from abc_step import abcStep
from lib.common import Common
import pprint


class FormatValue(abcStep):
    '''
    Format values as specified in the format configuration file.

    For more on python formatting see the following web page:

    `Format Specification Mini-Language <http://sphinx-doc.org/rest.html>`_.

    The format of the formatting configuration file is:

    ::

        <?xml version="1.0" encoding="UTF-8"?>
        <formats>
            <item device="0x13a200409029bf" port="adc-1">{:3.1f}</item>
            <item device="0x13a200408cccc3" port="adc-0">{:3.1f}</item>
            <item device="0x13a200408cccc3" port="adc-1">{:3.1f}</item>
        </formats>

    '''

    def __init__(self):
        '''
        Construct FormatValue object and read the configuration file formatvalue.xml
        '''
        super(FormatValue, self).__init__()
        format = FormatConfiguration()
        self.config = format.configure('formatvalue.xml')

    @property
    def topic_name(self):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.FormatValueStep

    @property
    def configuration_file_name(self):
        ''' The topic name to which this routine subscribes.'''
        return __name__

    ''' Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name(self):
        ''' Set the logger level. '''
        return Constants.LogKeys.steps

    def step(self, value, data={}, listeners=[]):
        """
        This function will format value as specified in the format stored in formatvalue.xml.

        :param value: The value to format.
        :type value: boolean, string, int or float
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

               | 1. **date:** time received: time when value was received.
               | 2. **units:** units of the number
               | 3. **name:** name assigned to the value
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: float, dict, listeners
        :Raises: ValueError, KeyError

        """
        device, port = Common.getDeviceAndPort(data)
        format_specification = self.config[device][port]
        try:
            new_value = format_specification.format(value)
            self.logger.debug("FormatValue received {} sent out {}".format(value, new_value))
        except ValueError as ve:
            error = "The format is incompatable with the input data type {}: device {} port {} file {}: error message {}".\
                    format(format_specification, device, port, self.configuration_file_name, ve)
            raise ValueError(error)
        return new_value, data, listeners


def instantuate_me(data):
    ''' This function will be called to instantiate this class. '''
    return FormatValue()
