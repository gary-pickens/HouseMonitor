'''
Created on Nov 14, 2012

@author: Gary
'''
import unittest
from steps.oneInN import OneInN
from steps.oneInN import instantuate_me
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch
from lib.getdatetime import GetDateTime


class Test(unittest.TestCase):

    logger = logging.getLogger('UnitTest')

    def setUp(self):
        logging.config.fileConfig("house_monitor_logging.conf")

    def tearDown(self):
        pass

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_one_device_and_port(self, config):
        N = OneInN()

        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        listeners = []
        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port
        N.step(1, data, listeners)
        self.assertEqual(N.count[device][port], 1)

        N.step(1, data, listeners)
        self.assertEqual(N.count[device][port], 2)

        N.step(1, data, listeners)
        self.assertEqual(N.count[device][port], 3)

        N = None

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_two_device_and_port(self, config):
        N = OneInN()

        listeners = []
        data = {}
        device1 = '0x13a200409029bf'
        device2 = '0x13a200408cccc3'
        port = 'adc-1'

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step(1, data, listeners)
        self.assertEqual(N.count[device1][port], 1)

        data[Constants.DataPacket.device] = device2
        data[Constants.DataPacket.port] = port
        N.step(1, data, listeners)
        self.assertEqual(N.count[device2][port], 1)

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step(1, data, listeners)
        self.assertEqual(N.count[device1][port], 2)

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.step(1, data, listeners)
        self.assertEqual(N.count[device1][port], 3)

        N = None

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_using_abc_step(self, config):
        N = OneInN()

        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        listeners = ['a', 'b', 'c']
        data = {}
        device1 = '0x13a200409029bf'
        device2 = '0x13a200408cccc3'
        port = 'adc-1'

        data[Constants.DataPacket.device] = device1
        data[Constants.DataPacket.port] = port
        N.substep(1, data, listeners)
        self.assertEqual(N.count[device1][port], 1)

        N.substep(2, data, listeners)
        self.assertEqual(N.count[device1][port], 2)

        N.substep(3, data, listeners)
        self.assertEqual(N.count[device1][port], 3)
        # TODO get this working
#        self.assertEqual(N.errors, 0)
#        self.assertEqual(N.last_error_time, None)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_no_device(self, config):
        N = OneInN()
        Common.send = Mock()
        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        listeners = ['a', 'b', 'c']
        data = {}
        port = 'adc-1'

        data[Constants.DataPacket.port] = port
        N.substep(1, data, listeners)
        self.assertEqual(N.errors, 1)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_no_port(self, config):
        N = OneInN()
        Common.send = Mock()
        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        listeners = ['a', 'b', 'c']
        data = {}
        device = '0x13a200409029bf'

        data[Constants.DataPacket.device] = device
        N.substep(1, data, listeners)
        self.assertEqual(N.errors, 1)
        self.assertEqual(N.counter, 0)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_no_device_in_count_dict(self, config):
        N = OneInN()
        Common.send = Mock()
        GetDateTime.isoformat = Mock()
        GetDateTime.isoformat.return_value = '123'
        N.config = {'0x13a200409029bf': {'adc-1': '2'}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        N.count = {}
        listeners = ['a', 'b', 'c']
        data = {}
        device = '0x13a200409029bf'
        port = 'adc-1'

        data[Constants.DataPacket.port] = port
        data[Constants.DataPacket.device] = device
        N.substep(1, data, listeners)
        self.assertEqual(N.count[device][port], 1)
        self.assertEqual(N.errors, 0)
        self.assertEqual(N.counter, 1)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_one_device_in_count_dict_that_is_not_the_same(self, config):
        device0 = 'device0'
        device1 = 'device1'
        port0 = 'port0'
        port1 = 'port1'

        N = OneInN()
        Common.send = Mock()
        GetDateTime.isoformat = Mock()
        GetDateTime.isoformat.return_value = '123'
        N.config = {device0: {port1: '2', port0: 10}, device1: {port0: '2', port1: '5'}}
        N.count = {device1: {port1: 10}}
        listeners = ['a', 'b', 'c']
        data = {}

        data[Constants.DataPacket.port] = port0
        data[Constants.DataPacket.device] = device0
        N.substep(1, data, listeners)
        self.assertEqual(N.count[device0][port0], 1)
        self.assertEqual(N.count[device1][port1], 10)
        self.assertEqual(N.errors, 0)
        self.assertEqual(N.counter, 1)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_oneInN_with_one_device_and_other_port_in_count_dict(self, config):
        N = OneInN()
        Common.send = Mock()
        GetDateTime.isoformat = Mock()
        GetDateTime.isoformat.return_value = '123'
        N.config = {'0x13a200409029bf': {'adc-1': '2', 'adc-0': 10}, '0x13a200408cccc3': {'adc-0': '2', 'adc-1': '5'}}
        N.count = {'0x13a200409029bf': {'adc-0': 10}}
        listeners = ['a', 'b', 'c']
        data = {}
        device0 = '0x13a200409029bf'
        device1 = '0x13a200408cccc3'
        port0 = 'adc-0'
        port1 = 'adc-1'

        data[Constants.DataPacket.port] = port1
        data[Constants.DataPacket.device] = device0
        N.substep(1, data, listeners)
        self.assertEqual(N.count[device0][port0], 10)
        self.assertEqual(N.count[device0][port1], 1)
        self.assertEqual(N.errors, 0)
        self.assertEqual(N.last_error_time, None)
        self.assertEqual(N.counter, 1)

    @patch('steps.oneInN.FormatConfiguration.configure')
    def test_instantuate_me(self, config):
        data = {}
        N = instantuate_me(data)
        self.assertEqual(N.counter, 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover


goodOneInNXml = '''<?xml version="1.0" encoding="UTF-8"?>
<formats>
    <item device="0x13a200409029bf" port="adc-1">2</item>
    <item device="0x13a200408cccc3" port="adc-0">5</item>
    <item device="0x13a200408cccc3" port="adc-1">20</item>
</formats>
'''
