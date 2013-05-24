'''
Created on Dec 14, 2012

@author: Gary
'''
import unittest
import datetime
from housemonitor.inputs.dataenvelope import DataEnvelope
from mock import Mock, MagicMock, patch


class Test( unittest.TestCase ):

    def test_storing_data( self ):
        test = DataEnvelope()
        test.arrival_time.toString = MagicMock()
        test.arrival_time.toString.return_value = '2012/10/03 01:02:03'
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual( test.packet, {} )
        self.assertEqual( test.arrival_time.toString(), '2012/10/03 01:02:03' )
        self.assertEqual( test.data, {} )

    @patch( 'housemonitor.inputs.dataenvelope.GetDateTime.toString' )
    def test_storing_data_using_patch( self, str ):
        test = DataEnvelope()
        str.return_value = '2012/10/03 01:02:03'
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual( test.packet, {} )
        self.assertEqual( test.arrival_time.toString(), '2012/10/03 01:02:03' )
        self.assertEqual( test.data, {} )

    @patch( 'housemonitor.inputs.dataenvelope.GetDateTime.__str__' )
    def test_storing_data_using_patch_and___str__( self, s ):
        test = DataEnvelope()
        s.return_value = '2012/10/03 01:02:03'
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual( test.packet, {} )
        self.assertEqual( test.arrival_time.__str__(), '2012/10/03 01:02:03' )
        self.assertEqual( test.data, {} )

    @patch( 'housemonitor.inputs.dataenvelope.GetDateTime.__str__' )
    def test_storing_data_using_patch_and___str__1( self, s ):
        test = DataEnvelope()
        s.return_value = '2012/10/03 01:02:03'
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual( test.packet, {} )
        self.assertEqual( str( test.arrival_time ), '2012/10/03 01:02:03' )
        self.assertEqual( test.data, {} )

#    def test_store_data(self):
#
#        self.assertEqual(test.arrival_time, datetime(2012, 10, 3, 01, 02, 03))
#        self.assertEqual(test.data, {'device': 'abc', 'port': 'adc-1'})

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_storing_data']
    unittest.main()    # pragma: no cover
