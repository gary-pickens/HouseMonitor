'''
Created on Dec 10, 2012

@author: Gary
'''
import unittest
from outputs.cosm.queue import COSMQueue
from lib.common import Common
import logging.config
from lib.constants import Constants
from mock import Mock, MagicMock
import Queue

class Test(unittest.TestCase):

    logger = logging.getLogger('UnitTest')

    def setUp(self):
        logging.config.fileConfig("house_monitor_logging.conf")

    def tearDown(self):
        pass

    def test_transmit(self):
        que = COSMQueue()
        que._queue.put = Mock()
        data = {}
        packet = {'data': data, 'current_value': 1}
        que.transmit(packet)
        que._queue.put.assert_called_once_with(packet)

    def test_receive(self):
        que = COSMQueue()
        data = {}
        packet = {'data': data, 'current_value': 1}

        que._queue.get = Mock()
        que._queue.get.return_value = packet
        value = que.receive()
        self.assertDictEqual(value, packet)
        que._queue.get.assert_called_once()

    def test_clear_with_empty_queue(self):
        que = COSMQueue()

        que._queue.empty = Mock()
        que._queue.empty.return_value = True
        que.clear()
        que._queue.empty.assert_called_once()

    def test_clear_with_one_in_queue(self):
        que = COSMQueue()
        data = {}
        packet = {'data': data, 'current_value': 1}
        que.transmit(packet)
        que.transmit(packet)

        size = que._queue.qsize()
        que.clear()
        clear_size = que._queue.qsize()
        self.assertEqual(size, 2)
        self.assertEqual(clear_size, 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover
