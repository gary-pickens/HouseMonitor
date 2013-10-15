'''
Created on Dec 14, 2012

@author: Gary
'''
import unittest
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants


class Test( unittest.TestCase ):

    def test_with_at( self ):
        test = DataEnvelope( type=Constants.EnvelopeTypes.XBEE, at='2012/10/03 01:02:03' )
        self.assertEqual( test.type, 'xbee' )
        self.assertEqual( test[Constants.DataPacket.arrival_time], '2012/10/03 01:02:03' )

    def test_with_computer_type( self ):
        test = DataEnvelope( Constants.EnvelopeTypes.COMPUTER )
        self.assertEqual( test.type, 'computer' )

    def test_repr( self ):
        test = DataEnvelope( Constants.EnvelopeTypes.XBEE, at='2012/10/03 01:02:03' )
        self.assertEqual( test.__repr__(), "DataEnvelope(xbee,  {'at': '2012/10/03 01:02:03'})" )

    def test_with_invalid_type( self ):
        with self.assertRaisesRegexp( KeyError, 'Invalid type error: type = ABC' ):
            test = DataEnvelope( 'ABC' )
            self.assertEqual( test.type, 'ABC' )

    def test_with_dict( self ):
        data = {'a': 'b', 'c': 'd'}
        test = DataEnvelope( Constants.EnvelopeTypes.COMPUTER, **data )
        self.assertEqual( test.type, 'computer' )
        self.assertEqual( test['a'], 'b' )
        self.assertEqual( test['c'], 'd' )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_storing_data']
    unittest.main()  # pragma: no cover
