'''
Created on 2012-11-06

@author: Gary

'''
from housemonitor.steps.abc_step import abcStep
from housemonitor.lib.constants import Constants


class COSMOutputStep( abcStep ):
    '''
    This object should be started with with the COSM thread and hang around forever.

    '''
    queue = None
    ''' A Queue for communicating between threads. '''

    previous_value = None
    ''' Contains the previous value '''

    data_items_limit = 10

    def __init__( self, queue ):
        '''
        Initialize COSMOutputStep.

        :param queue: an object which communicates between threads
        :type queue: HMQueue
        '''
        super( COSMOutputStep, self ).__init__()
        self.queue = queue

    @property
    def topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.COSM

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsCOSM

    def step( self, value, data={}, listeners=[] ):
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
        if self.previous_value == None:
            self.previous_value = value
        if ( data[Constants.DataPacket.device] == '0x13a200409029bf' and
                data[Constants.DataPacket.port] == 'dio-0' and
                self.packet_count < self.data_items_limit ):
            if self.previous_value == value:
                self.packet_count = self.packet_count + 1
                data[Constants.DataPacket.action] = Constants.DataPacket.accumulate
                self.logger.info( 'Accumulating data {} count {}'.format( data, self.packet_count ) )
            else:
                data[Constants.DataPacket.action] = Constants.DataPacket.send
                self.packet_count = 0
            self.previous_value = value
        else:
            data[Constants.DataPacket.action] = Constants.DataPacket.send
            self.packet_count = 0
            self.logger.info( 'Sending data {}'.format( data ) )

        packet = {'data': data, 'current_value': value}
        self.queue.transmit( packet )
        self.logger.debug( "COSM Step data transmitted to COSM thread = {}".format( packet ) )
        return value, data, listeners
