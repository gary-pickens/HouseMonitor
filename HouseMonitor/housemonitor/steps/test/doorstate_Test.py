'''
Created on Sep 4, 2012

@author: Gary
'''
import unittest
from housemonitor.steps.doorstate import ConvertGarageDoorState
from housemonitor.steps.doorstate import instantuate_me
from datetime import datetime


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass

    def test_DoorOpen(self):
        data = {}
        data['device'] = 'device'
        data['port'] = 'port'
        data['at'] = datetime(2013, 1, 2, 3, 4, 5)
        listeners = ['a', 'b']
        door = ConvertGarageDoorState()
        results, new_data, new_listeners = door.step(True, data, listeners)
        self.assertEqual(results, '1')
        self.assertEqual(new_data['units'], 'closed')

    def test_DoorClosed(self):
        data = {}
        data['device'] = 'device'
        data['port'] = 'port'
        data['at'] = datetime(2013, 1, 2, 3, 4, 5)
        listeners = ['a', 'b']
        door = ConvertGarageDoorState()
        results, new_data, new_listeners = door.step(False, data, listeners)
        self.assertEqual(results, '0')
        self.assertEqual(new_data['units'], 'open')

    def test_DoorOther(self):
        data = {}
        data['device'] = 'device'
        data['port'] = 'port'
        listeners = ['a', 'b']
        door = ConvertGarageDoorState()
        results, new_data, new_listeners = door.step('ste', data, listeners)
        self.assertEqual(results, -1)
        self.assertEqual(new_data['units'], 'invalid')

    def test_instantuate_me(self):
        data = {}
        N = instantuate_me(data)
        self.assertIsInstance(N, ConvertGarageDoorState)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover
