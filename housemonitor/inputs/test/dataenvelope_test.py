'''
Created on Dec 14, 2012

@author: Gary
'''
import unittest
import datetime
from housemonitor.inputs.dataenvelope import DataEnvelope
from mock import Mock, MagicMock, patch
from housemonitor.lib.constants import Constants


class Test( unittest.TestCase ):

    def test_with_at(self):
        test = DataEnvelope(at='2012/10/03 01:02:03')
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual(test[Constants.DataPacket.arrival_time], '2012/10/03 01:02:03')

    def test_with_computer_type(self):
        test = DataEnvelope(Constants.EnvelopeTypes.COMPUTER)
        self.assertEqual(test.type, 'computer')

    def test_with_invalid_type(self):
        with self.assertRaisesRegexp(KeyError, 'Invalid type error: type = ABC'):
            test = DataEnvelope('ABC')
            self.assertEqual(test.type, 'ABC')

#    def test_store_data(self):
#
#        self.assertEqual(test.arrival_time, datetime(2012, 10, 3, 01, 02, 03))
#        self.assertEqual(test.data, {'device': 'abc', 'port': 'adc-1'})

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_storing_data']
    unittest.main()    # pragma: no cover
