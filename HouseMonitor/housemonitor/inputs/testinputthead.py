'''
Created on Jun 21, 2012

@author: Gary
'''
import threading
import time
from struct import *

from lib.constants import Constants
from lib.base import Base
from lib.getdatetime import GetDateTime
from inputs.dataenvelope import DataEnvelope


class SendGarageDoorData():
    '''
    Send fake XBee messages though the system and see how it performs.
    '''
    _i = 0
    _starting_temperature = 400
    _low_temperature = 400
    _high_temperature = 900
    _temperature_step_value = 10
    _current_temperature = _starting_temperature

    _door = False

    _packets_sent = 0

    _time_stamp = None

    _print_message_count = 1  # how many message

    _input_queue = None

    def __init__(self, input_queue):
        self._time_stamp = GetDateTime()
        self._input_queue = input_queue

    def send(self):
        '''
        send fake xbee messages that are modeled after the garage door XBee
        '''
        packet = {}

        if (self._current_temperature > self._high_temperature):
            self._current_temperature = self._low_temperature

        self._current_temperature = self._current_temperature + self._temperature_step_value
        self._door = not self._door

        self._i += 1
        if ((self._i % 2) == 0):
            packet['source_addr_long'] = pack('!Q', 0x13a200409029bf)
            packet[Constants.XBee.samples] = [{
                                                Constants.XBee.adc_1: self._current_temperature,
                                                Constants.XBee.dio_0: self._door
                                                }]
        else:
            packet['source_addr_long'] = pack('!Q', 0x13a200408cccc3)
            packet[Constants.XBee.samples] = [{
                                               Constants.XBee.adc_1: self._current_temperature,
                                               Constants.XBee.adc_0: self._current_temperature + 200
                                               }]

        packet['source_addr'] = pack('!H', 0xf9f2)

        envelope = DataEnvelope(packet=packet)

        self._input_queue.transmit(envelope)

        # print a message every _print_message_count times
#        if ((self._packets_sent % self._print_message_count) == 0):
#            delta = GetDateTime() - self._time_stamp
#            print "{} {}".format(delta, self._packets_sent)
#            self._time_stamp = GetDateTime()
        self._packets_sent = self._packets_sent + 1


class TestInputThread(Base, threading.Thread):
    '''
    Send fake messages though the system and see how it performs.
    '''
    _input_queue = None
    _sleep_time = 1  # seconds

    def __init__(self, queue):
        '''
        Constructor
        args:
            queue is the InputQueue

        '''
        super(TestInputThread, self).__init__()
        threading.Thread.__init__(self)
        self._input_queue = queue

    @property
    def logger_name(self):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return Constants.LogKeys.inputs

    def run(self):
        try:
            garage_door_data = SendGarageDoorData(self._input_queue)
            while True:
                garage_door_data.send()
                time.sleep(self._sleep_time)
        except KeyboardInterrupt as ki:
            self.logger.warn("test input thread exiting")
