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
    ''' The number of packets that are allowed to accumulate before they are sent to COSM '''
    packet_count = 0
    ''' The number of packets that are now saved '''

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

    def specialProcessingForGarageDoor( self, value, data ):
        ''' Special processing if the garage door.
        
        :param value: Indicates if the garage door is open or not.
        :type value: boolean
        :param data: a dictionary containing more information about the
                value. Data can be added to this as needed.  Here is a list
                of values that will be in the data dictionary:

                1 **date:** time received: time when value was received.
                2. **units:** units of the number
                3. ""name:** name assigned to the value

        '''

        ''' test if garage door '''
        # TODO: Store these values in a configuration file.
        if ( data[Constants.DataPacket.device] == '0x13a200409029bf' and data[Constants.DataPacket.port] == 'dio-0' ):

            if self.previous_value == None:
                self.previous_value = value

            if self.packet_count < self.data_items_limit and self.previous_value == value:
                self.packet_count = self.packet_count + 1
                data[Constants.DataPacket.action] = Constants.DataPacket.accumulate
            else:
                data[Constants.DataPacket.action] = Constants.DataPacket.send
                if self.previous_value == value:
                    self.packet_count = 0
                else:
                    self.packet_count = self.data_items_limit - 2

            self.previous_value = value
        else:
            data[Constants.DataPacket.action] = Constants.DataPacket.send
            self.logger.debug( 'Sending data {} packet_count {}'.format( data, self.packet_count ) )

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
        self.specialProcessingForGarageDoor( value, data )

        packet = {'data': data, 'current_value': value}
        self.queue.transmit( packet )
        self.logger.debug( "COSM Step data transmitted to COSM thread. packet_count = {}".format( data ) )
        return value, data, listeners
