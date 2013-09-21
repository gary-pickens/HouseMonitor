'''
Created on Jun 21,
        2012

@author: Gary
'''
import threading
import time
from struct import *

from housemonitor.lib.constants import Constants
from housemonitor.lib.base import Base
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.inputs.dataenvelope import DataEnvelope
import os
import sys

class TestInputThread( Base, threading.Thread ):
    '''
    Send fake messages though the system and see how it performs.
    '''
    __input_queue = None
    __sleep_time = 1  # seconds

    def __init__( self, queue ):
        '''
        Constructor
        args:
            queue is the InputQueue

        '''
        super( TestInputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.__input_queue = queue

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.inputs

    def run( self ):
        garage_door_data = SendGarageDoorData( self.__input_queue )
        while True:
            try:
                garage_door_data.send()
            except KeyboardInterrupt as ki:
                self.logger.warn( "test input thread exiting" )


class SendGarageDoorData():
    '''
    Send fake XBee messages though the system and see how it performs.
    '''
    __input_queue = None

    def __init__( self, input_queue ):
        self.__input_queue = input_queue

    def send( self ):
        '''
        send fake xbee messages that are modeled after the garage door XBee
        '''
        for packet in self.msgs:
            envelope = DataEnvelope( packet=packet )
            self.__input_queue.transmit( envelope )
            time.sleep( 20 )

    msgs = [
        {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf', 'source_addr': '\xf9\xf2', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-1': 669, 'dio-0': True}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D1', 'id': 'remote_at_response'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D2', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8c\xcc\xc3', 'source_addr': '\x11\xba', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 659, 'adc-1': 541}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf', 'source_addr': '\xf9\xf2', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-1': 668, 'dio-0': True}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D2', 'id': 'remote_at_response'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D1', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'source_addr': '\xe4\xe8', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-0': True, 'dio-1': False, 'dio-6': False, 'dio-4': True, 'dio-5': False}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 671}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90(g', 'source_addr': '6\x01', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 662}], 'options': 'A'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf', 'source_addr': '\xf9\xf2', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-1': 666, 'dio-0': True}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D2', 'id': 'remote_at_response'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D1', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90(g', 'source_addr': '6\x01', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 662}], 'options': 'A'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8c\xcc\xc3', 'source_addr': '\x11\xba', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-0': 658, 'adc-1': 534}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf', 'source_addr': '\xf9\xf2', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-1': 666, 'dio-0': True}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D2', 'id': 'remote_at_response'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D1', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'source_addr': '\xe4\xe8', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-0': True, 'dio-1': False, 'dio-6': False, 'dio-4': True, 'dio-5': False}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x90)\xbf', 'source_addr': '\xf9\xf2', 'id': 'rx_io_data_long_addr', 'samples': [{'adc-1': 667, 'dio-0': True}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D2', 'id': 'remote_at_response'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D1', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'source_addr_long': '\x00\x13\xa2\x00@\x8b\xafE', 'source_addr': '\x07\x0f', 'id': 'rx_io_data_long_addr', 'samples': [{'dio-2': False, 'dio-3': False, 'dio-1': False, 'adc-0': 672}], 'options': '\x01'},
        {'status': '\x00', 'source_addr': '\xe4\xe8', 'source_addr_long': '\x00\x13\xa2\x00@\x90*\x02', 'frame_id': '\xaa', 'command': 'D0', 'id': 'remote_at_response'},
    ]
