'''
Created on Oct 2, 2012

@author: Gary

'''
import threading

from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.base import Base
from send import COSMSend
from housemonitor.lib.constants import Constants


class COSMOutputThread( Base, threading.Thread ):
    '''
    This thread will remove the data off the cosm queue and send it to the COSM web site.
    '''

    forever = True

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.outputsCOSM

    _queue = None
    ''' The HMQueue object.  Used to receive data. '''

    _cosm_send = None
    ''' Object that sends data to COSM. '''

    def __init__( self, queue, options, send=None, name=None ):
        '''
        Constructor
        args:
        :param queue: Queue for sending data between threads
        :type HMQueue:
        :param options: options from the command line
        :type dict:
        :param send: optional argument used for test
        :type COSMSend:
        :returns: None
        :raises: None

        '''
        self._queue = queue
        if ( send == None ):
            self._cosm_send = COSMSend( options )
        else:
            self._cosm_send = send
        super( COSMOutputThread, self ).__init__()

        threading.Thread.__init__( self )


    def process( self ):
        '''
        This function does the following:

        #. Wait on data from the queue.
        #. Remove data from previous send.
        #. Unpack data from received packet
        #. send data to COSM_send

        '''
        packet = self._queue.receive()
        data = packet[Constants.Cosm.packet.data]
        data[Constants.Cosm.packet.current_value] = packet[Constants.Cosm.packet.current_value]
        self._cosm_send.output( data )

    def run( self ):
        '''
        The COSM thread will loop forever calling process.

        '''
        while self.forever:
            self.process()
