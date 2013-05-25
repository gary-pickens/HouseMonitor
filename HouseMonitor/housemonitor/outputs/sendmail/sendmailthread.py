'''
Created on May 24, 2013

@author: Gary
'''
import threading
import time
import logging
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib import constants
from housemonitor.lib.base import Base


class SendMailThread( Base, threading.Thread ):
    '''
    This class will send a message via email on when some event happens.
    '''

    output_queue = None
    done = False
    connected = False
    talking = True

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the xbee output Queue

        '''
        super( SendMailThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue

    @property
    def logger_name( self ):
        return Constants.LogKeys.outputsZigBee

    def sendMessages( self ):
        packet = self.output_queue.receive()
        data = packet['data']
        value = packet['value']
        to = data[Constants.DataPacket.toEmailAddresss]


    def run( self ):
        self.sendMessage()
