'''
Created on Dec 4, 2012

@author: Gary
'''
import unittest
from lib.base import Base
from lib.constants import Constants
from lib.common import Common
from pubsub import pub
from mock import Mock, MagicMock, patch


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getDeviceAndPort_with_good_data(self):
        data = {'device': 'abc',
                'port': 'def'}
        device, port = Common.getDeviceAndPort(data)
        self.assertEqual(device, 'abc')
        self.assertEqual(port, 'def')

    def test_getDeviceAndPort_with_missing_port(self):
        data = {'device': 'def'}
        with self.assertRaisesRegexp(KeyError, 'The port is missing from the data block:'):
            device, port = Common.getDeviceAndPort(data)

    def test_getDeviceAndPort_with_missing_device(self):
        data = {'port': 'def'}
        with self.assertRaisesRegexp(KeyError, 'The device is missing from the data block:'):
            device, port = Common.getDeviceAndPort(data)

    @patch.object(pub, 'sendMessage')
    def test_send(self, sendMessage):
        value = 1
        data = {'device': {'port': {'a': 'b'}}}
        listeners = ['a', 'b', 'c']
        Common.send(value, data, listeners)
        sendMessage.assert_called_once_with('a', value=value, data=data, listeners=['b', 'c'])

# TODO get split working
#    @patch.object(pub, 'sendMessage')
#    def test_send_with_split(self, sendMessage):
#        value = 1
#        data = {'device': {'port': {'a': 'b'}}}
#        listeners = [['x', 'y', 'z'], 'a', 'b', 'c']
#        Common.send(value, data, listeners)
#        sendMessage.assert_called_with('a', value=value, data=data, listeners=['b', 'c'])
#        sendMessage.assert_called_with(['x'], value=value, data=data, listeners=['y', 'z'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()  # pragma: no cover
