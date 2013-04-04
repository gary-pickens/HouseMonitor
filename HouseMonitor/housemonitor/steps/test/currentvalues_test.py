'''
Created on Dec 17, 2012

@author: Gary
'''
import unittest
from steps.currentvalues import CurrentValues
from steps.currentvalues import instantuate_me
from lib.currentvalues import CurrentValues as CV
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

    def test_with_real_data(self):
        lcv = CV()
        d = {'current values': lcv}
        cv = CurrentValues(d)
        listeners = []
        data = {'device': '0x13a200409029bf',
                'port': 'adc-1'
        }
        value, data, listeners = cv.step(1, data, listeners)
        self.assertAlmostEqual(value, 1, 2)
        test_value = lcv.get_current_value('0x13a200409029bf', 'adc-1')
        self.assertEqual(test_value['current_value'], 1)

    def test_with_invalid_device_data(self):
        lcv = CV()
        d = {'current values': lcv}
        cv = CurrentValues(d)
        listeners = []
        data = {'device': '0x13a200409029be',
                'port': 'adc-1'
        }

        value, data, listeners = cv.step(1, data, listeners)
        self.assertAlmostEqual(value, 1, 2)
        test_value = lcv.get_current_value('0x13a200409029be', 'adc-1')
        self.assertEqual(test_value['current_value'], 1)

    def test_with_invalid_port_data(self):
        lcv = CV()
        d = {'current values': lcv}
        cv = CurrentValues(d)
        listeners = []
        data = {'device': '0x13a200409029bf',
                'port': 'adc-2'
        }

        value, data, listeners = cv.step(1, data, listeners)
        self.assertAlmostEqual(value, 1, 2)
        test_value = lcv.get_current_value('0x13a200409029be', 'adc-1')
        self.assertEqual(test_value['current_value'], 1)

    def test_logger_name(self):
        data = {}
        cv = instantuate_me(data)
        self.assertEqual(cv.logger_name, Constants.LogKeys.steps)

    def test_topic_name(self):
        data = {}
        cv = CurrentValues(data)
        self.assertEqual(cv.topic_name, Constants.TopicNames.CurrentValueStep)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover
