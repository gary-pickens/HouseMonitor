'''
Created on 2012-11-06

@author: Gary

'''
from steps.abc_step import abcStep
from lib.constants import Constants
from lib.hmqueue import HMQueue


class ZigBeeOutputStep(abcStep):
    '''
    This object should be started with with the COSM thread and hang around forever.

    '''
    queue = None
    ''' A Queue for communicating between threads. '''

    def __init__(self, queue):
        '''
        Initialize COSMOutputStep.

        :param queue: an object which communicates between threads
        :type queue: COSMQueue
        '''
        super(ZigBeeOutputStep, self).__init__()
        self.queue = queue
        self.logger.debug("ZigBeeOutputStep started")

    @property
    def topic_name(self):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.ZigBeeOutput

    @property
    def logger_name(self):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsZigBee

    def step(self, value, data={}, listeners=[]):
        """
        This function receives data that will be sent to COSM and forwards it to the COSM output processing
        thread.

        This function will compare the value with the previous value and if they are different send the data to
        the next listener else don't send the data along.

        :param value: The number to add to the list of numbers.
        :type value: boolean, int or float
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

                1 **date:** time received: time when value was received.
                2. **units:** units of the number
                3. ""name:** name assigned to the value
        :param listeners: a list of the subscribed routines to send the data to
        :returns: value, data, listeners
        :rtype: float, dict, listeners
        :Raises: ValueError, KeyError
        """
        packet = {'data': data, 'value': value}
        self.queue.transmit(packet, self.queue.three_quarters_priority)
        self.logger.debug("ZigBee Step data transmitted to ZigBee thread = {}".format(packet))
        return value, data, listeners
