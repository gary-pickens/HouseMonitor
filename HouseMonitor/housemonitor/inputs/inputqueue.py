'''
Created on Sep 20, 2012

@author: Gary
'''
import Queue

from lib.base import Base
from lib.constants import Constants


# TODO: Remove this file and use hmqueue
class InputQueue(Base, object):
    '''
    classdocs
    '''
    INPUT_QUEUE_SIZE = 100
    _inputQueue = None

    def __init__(self):
        '''
        Constructor
        '''
        self._inputqueue = Queue.PriorityQueue(self.INPUT_QUEUE_SIZE)
        super(InputQueue, self).__init__()

    @property
    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.inputs

    def transmit(self, packet, priority=Constants.Queue.default_priority):
        '''
        Add packet to input queue.

        This is the input queue that all incoming messages will go though.  messages
        are added on the input side and then processed on the out going side.

        args:
            packet: a data packet with the data to be processed
        returns:
            none
        exceptions:
            none
        side effects:
            may block if gueue is full
        '''
        self._inputqueue.put((priority, packet))
        self.logger.debug("put packet on inputQueue {}".format(packet))

    def receive(self):
        '''
        remove packet from input queue.

        This routine will remove a packet from the input queue for processing.

        args:
            None
        returns
            packet
        exceptions
            None
        side effect
            Will block if no packets are availiable
        '''
        priority, packet = self._inputqueue.get()
        self.logger.debug("get packet off inputQueue {}".format(packet))
        return packet
