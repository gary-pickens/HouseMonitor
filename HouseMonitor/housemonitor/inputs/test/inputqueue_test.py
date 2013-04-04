'''
Created on Dec 18, 2012

@author: Gary
'''
from inputs.inputqueue import InputQueue

import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch
from lib.getdatetime import GetDateTime


class Test(unittest.TestCase):
    logger = logging.getLogger('UnitTest')

    def setUp(self):
        logging.config.fileConfig("house_monitor_logging.conf")

    def tearDown(self):
        pass

    def test_transmit_and_receive(self):
        iq = InputQueue()
        packet = {'device': {'port': {'a': 'b'}}}
        iq.transmit(packet)
        new_packet = iq.receive()
        self.assertDictEqual(packet, new_packet)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover
