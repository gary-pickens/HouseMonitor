'''
Created on Oct 2, 2012

@author: Gary

'''
import Queue
from lib.base import Base
from lib.constants import Constants


class COSMQueue(Base):
    '''
    A class for communicating between the main thread and the
    COSM thread.
    '''
    QUEUE_SIZE = 100
    ''' The size of the Queue. '''

    _queue = None
    ''' A Tread safe queue used to communicate data between threads. '''

    def __init__(self):
        '''
        Constructor
        '''
        if (COSMQueue._queue == None):
            COSMQueue._queue = Queue.Queue(self.QUEUE_SIZE)
        super(COSMQueue, self).__init__()

    @property
    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsCOSM

    def transmit(self, packet):
        '''
        Add packet to input queue.

        This is the cosm queue that all outgoing messages will go though.  messages
        are added on the processing side and then passed to the thread where the
        data will be sent to COSM.


        :param packet: a data packet with the data to be processed
        :returns: none
        :exceptions: none

        :Example:
        >>> from outputs.cosm.queue import COSMQueue
        >>> cosm = COSMQueue()
        >>> cosm.transmit({'a':  'b'})
        >>> cosm.receive()
        {'a': 'b'}

        .. warning:: This my block if gueue is full.  The attribute QUEUE_SIZE contains the number of items that can be put on the queue.

        '''
        COSMQueue._queue.put(packet)
        self.logger.debug("put packet on cosmQueue: packet = {}".format(packet))

    def receive(self):
        '''
        remove packet from input queue.

        This routine will remove a packet from the COSM queue where it will be sent to COSM.

        :returns packet: The same packet the was transmitted by the transmit function.
        :rtype:  Same as the data that was sent by the transmit function
        :exceptions: None
        .. warning:: Will block if no packets are availiable

        :Example:
        >>> from outputs.cosm.queue import COSMQueue
        >>> cosm = COSMQueue()
        >>> cosm.transmit({'a':  'b'})
        >>> cosm.receive()
        {'a': 'b'}

        '''
        packet = COSMQueue._queue.get()
        self.logger.debug("get packet off cosm Queue: packet = {}".format(packet))
        return packet

    def clear(self):
        '''
        Clear the queue

        This routine is mainly used for unit test

        :Example:
        >>> from outputs.cosm.queue import COSMQueue
        >>> cosm = COSMQueue()
        >>> cosm.clean()

        .. warning::  All the data in the queue will be lost
        '''
        try:
            while (self._queue.get(False)):
                pass
        except Queue.Empty:
            return

if __name__ == "__main__":
    import doctest
    doctest.testmod()  # pragma: no cover
