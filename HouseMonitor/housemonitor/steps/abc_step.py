'''
Created on Jul 30, 2012

@author: Gary
'''
import abc
from pubsub import pub
from lib.base import Base
from datetime import datetime
from lib.common import Common
from lib.getdatetime import GetDateTime
from lib.constants import Constants
import copy


class abcStep(Base):
    '''
    This is a abstract class which is used by the step routines to convert one type of data to another.

    For example: To convert Centigrade to Fahrenheit:

    #. Create a class that has a base class of abcStep.
    #. Add a function called *step* that does the conversion.
    #. Add the other abstract methods and properties that are required:
        #.  **topic_name** The topic name to which this routine subscribes.
        #.  **logger_name** Set the logger name.

    For an example see the other files in the step directory.

    '''
    __metaclass__ = abc.ABCMeta

    whoami = None

    def __init__(self):
        '''
        Constructor
        '''
        super(abcStep, self).__init__()
        pub.subscribe(self.substep, self.topic_name)
        pub.subscribe(self.getUseCount, self.statistics_topic_name)
        pub.subscribe(self.getErrorCount, self.statistics_topic_name)
        self.whoami = self.__class__.__name__

    def getUseCount(self, value, data, listeners):
        ''' Report the number of times that step has been called.

        :param value: Not used.
        :type value: int
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

              |  1 **date:** time received: time when value was received.
              |  2. **units:** units of the number
              |  3. **name:** name assigned to the value
              |  4. etc.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: count, data, listeners
        :rtype: float, dict, listeners
        :Raises: None

        :Example:
        >>> from steps.zigbee2volts import ZigbeeCountToVolts
        >>> zig = ZigbeeCountToVolts()
        >>> zig.getUseCount(100, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (0, {'device': 'xyz', 'units': 'V', 'port': 'abc'}, ['a', 'b'])
        >>> zig.step(1, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        >>> zig.getUseCount(100, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        (1, {'device': 'xyz', 'units': 'V', 'port': 'abc'}, ['a', 'b'])
        '''
        if (self.counter != 0):
            self.logger.debug('getUseCount = {}'.format(self.counter))
            data[Constants.DataPacket.device] = 'HouseMonitor.' + self.whoami
            data[Constants.DataPacket.port] = data[Constants.DataPacket.name] = 'Count'
            data[Constants.DataPacket.arrival_time] = self.last_count_time
            Common.send(self.counter, data, copy.copy(listeners))

    def getErrorCount(self, value, data, listeners):
        ''' Report the number of errors that has occurred in this step.

        :param value: Not used.
        :type value: int
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

              |  1. **date:** time received: time when value was received.
              |  2. **units:** units of the number
              |  3. **name:** name assigned to the value
        :param listeners: a list of the subscribed routines to send the data to
        :returns: count, data, listeners
        :rtype: float, dict, listeners
        :Raises: None

        :Example:
        from steps.zigbee2volts import ZigbeeCountToVolts
        zig = ZigbeeCountToVolts()
        zig.getErrorCount(100, {'device': 'xyz', 'port': 'abc'}, ['a', 'b'])
        '''
        if (self.errors != 0):
            self.logger.debug('getErrorCount = {}'.format(self.errors))
            data[Constants.DataPacket.device] = 'HouseMonitor.' + self.whoami
            data[Constants.DataPacket.port] = data[Constants.DataPacket.name] = 'Error Count'
            data[Constants.DataPacket.arrival_time] = self.last_error_time
            Common.send(self.errors, data, copy.copy(listeners))

    @abc.abstractproperty
    def topic_name(self):  # pragma: no cover
        """ The topic name that pubsub uses to send data to this step. """
        return 'Should never see this'

    counter = 0
    ''' Contains the number of times that step has been called '''

    last_count_time = None
    ''' Contains time when step was last called. '''

    errors = 0
    ''' Contains the number of errors. '''

    last_error_time = None
    ''' Contains the time of the last error. '''

    def logger_name(self):
        """ Set the logger name. This needs to be added to house_monitoring_logging.conf """
        return 'steps'  # pragma: no cover

    @property
    def statistics_topic_name(self):
        ''' Set the name that pubsub uses to get usage information about the module. '''
        return Constants.TopicNames.Statistics

    @abc.abstractmethod
    def step(self, value, data, listeners):
        '''
        Abstract method for the procedure that does all user specific computations.

        :param value: The input value to be processesed
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

               | 1. **date:** time received: time when value was received.
               | 2. **units:** units of the number
               | 3. **name:** name assigned to the value
               | 4. **device** name of the device the data is from.
               | 5. **port** name of the port the data is from.
        :param listeners: a list of the subscribed routines to send the data to
        :returns: new_value, new_data, new_listeners
        :rtype: int, dict, listeners
        Raises:
            None
        '''
        pass  # pragma: no cover

    def substep(self, value, data, listeners):
        '''
        This function is wraps step function.  It counts usage, errors then sends the data to next function.

        :param value: The number to convert to volts.
        :type value: int, float, string, etc
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

              |  1 **date:** time received: time when value was received.
              |  2. **units:** units of the number
              |  3. **name:** name assigned to the value
              |  4. **device** name of the device the data is from.
              |  5. **port** name of the port the data is from.
        :param listeners: a list of the pubsub routines to send the data to
        :returns: value, data, listeners
        :rtype: value, dict, listeners
        :Raises: None

        '''
        # Trap any exceptions from getting to pubsub
        try:
            value, data, listeners = self.step(value, data, listeners)
            self.counter += 1
            self.last_count_time = datetime.utcnow()
            self.logger.debug('value {} listeners {}'.format(value, listeners))
            Common.send(value, data, listeners)
        except Exception as ex:
            self.logger.exception("{}: {}".format(__name__, ex))
            self.errors += 1
            self.last_error_time = datetime.utcnow()


def instantuate_me(data):  # pragma: no cover
    return None
