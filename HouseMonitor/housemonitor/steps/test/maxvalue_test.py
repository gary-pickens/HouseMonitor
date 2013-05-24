'''
Created on Mar 2, 2013

@author: Gary
'''
import unittest
from housemonitor.steps.maxvalue import MaxValue
from housemonitor.steps.maxvalue import instantuate_me
from housemonitor.lib.common import Common
import logging.config
from housemonitor.lib.constants import Constants
import pprint
from mock import Mock, MagicMock, patch


class Test(unittest.TestCase):

    data = {}
    steps = []
    device = 'device'
    port = 'port'

    def setUp(self):
        self.data[self.device] = self.device
        self.data[self.port] = self.port
        self.steps = ['a', 'b']

    def tearDown(self):
        self.data = None
        self.steps = None

    def test_initalize_dictionary_with_value_of_10(self):

        max = MaxValue()
        value = 10
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], value)

    def test_initalize_dictionary_with_added_port_to_value_of_11(self):

        max = MaxValue()
        value = 10
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], value)

        max = MaxValue()
        value = 11
        self.data['port'] = 'port1'
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], 10)
        self.assertEqual(max.max_value[self.device]['port1'], value)

    def test_set_max_value_to_20(self):

        max = MaxValue()
        value = 10
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], value)

        value = 20
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], value)

    def test_leave_max_value_at_10(self):

        max = MaxValue()
        value = 10
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], value)

        value = 5
        return_value, data, steps = max.step(value, self.data, self.steps)
        self.assertDictEqual(data, self.data)
        self.assertListEqual(steps, self.steps)
        self.assertEqual(return_value, value)
        self.assertEqual(max.max_value[self.device][self.port], 10)

    def test_topic_name(self):
        max = MaxValue()
        self.assertEqual(max.topic_name, Constants.TopicNames.MaxValue)

    def test_logger_name(self):
        max = MaxValue()
        self.assertEqual(max.logger_name, Constants.LogKeys.steps)

    def test_instantuate_me(self):
        max = instantuate_me(self.data)
        self.assertIsInstance(max, MaxValue)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
