'''
Created on 3/8/2013

@author: Gary

'''
import Queue
from lib.base import Base
from lib.constants import Constants


class HMQueue( Base ):
    '''
    '''
    QUEUE_SIZE = 100
    ''' The size of the Queue. '''

    ''' Priority levels for the priority queue '''
    high_priority = 0
    three_quarters_priority = 2
    mid_priority = 4
    one_quarter_priority = 3
    low_priority = 8

    _queue = None
    ''' A Tread safe queue used to communicate data between threads. '''

    def __init__( self ):
        '''
        Constructor
        '''
        if ( self._queue == None ):
            self._queue = Queue.PriorityQueue( self.QUEUE_SIZE )
        super( HMQueue, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.lib

    def transmit( self, packet, priority=mid_priority ):
        '''
        Add packet to input queue.

        This is the cosm queue that all outgoing messages will go though.  messages
        are added on the processing side and then passed to the thread where the
        data will be sent to COSM.


        :param packet: a data packet with the data to be processed
        :returns: none
        :exceptions: none

        >>> from lib.queue import HMQueue
        >>> cosm = HMQueue()
        >>> cosm.transmit({'a':  'b'})
        >>> cosm.receive()
        {'a': 'b'}

        .. warning:: This my block if gueue is full.  The attribute QUEUE_SIZE contains the number of items that can be put on the queue.

        '''
        self._queue.put( ( priority, packet ) )
        self.logger.debug( "put packet on HMQueue: packet = {}".format( packet ) )

    def receive( self ):
        '''
        Remove packet from input queue.

        This routine will remove a packet from the COSM queue where it will be sent to COSM.

        :returns packet: The same packet the was transmitted by the transmit function.
        :rtype:  Same as the data that was sent by the transmit function
        :exceptions: None

        .. warning:: Will block if no packets are available

        >>> from lib.queue import HMQueue
        >>> cosm = HMQueue()
        >>> cosm.transmit({'a':  'b'})
        >>> cosm.receive()
        {'a': 'b'}

        '''
        priority, packet = self._queue.get()
        self.logger.debug( "get packet off cosm Queue: packet = {}".format( packet ) )
        return packet

    def clear( self ):
        '''
        Clear the queue

        This routine is mainly used for unit test

        >>> from lib.queue import HMQueue
        >>> cosm = HMQueue()
        >>> cosm.clean()

        .. warning::  All the data in the queue will be lost
        '''
        try:
            while ( self._queue.get( False ) ):
                pass
        except Queue.Empty:
            return

if __name__ == "__main__":
    import doctest
    doctest.testmod()    # pragma: no cover
