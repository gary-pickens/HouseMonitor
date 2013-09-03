'''
Created on Apr 12, 2013

@author: Gary
'''
from housemonitor.inputs import dataenvelope
from housemonitor.inputs.computermonitor.computermonitor import ComputerMonitor
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.common import Common
from housemonitor.lib.constants import Constants
from housemonitor.lib.getdatetime import GetDateTime
from mock import *
from datetime import datetime
import logging.config
import pprint
import unittest
import copy


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )


    def tearDown( self ):
        pass

#     def test_thread( self ):
#         queue = MagicMock()
#         cmp = ComputerMonitor( queue )
#         cmp.forever = False
#         cmp.start()

    def test_logger_name( self ):
        queue = MagicMock()
        cmp = ComputerMonitor( queue )
        self.assertEqual( cmp.logger_name, Constants.LogKeys.ComputerMonitor )

    def test_extractData( self ):
        queue = MagicMock()
        cmp = ComputerMonitor( queue )

        counts = cmp.extractData( data )
        self.assertIsNotNone( counts )
        self.assertEqual( counts['tx'], '1188940' )
        self.assertEqual( counts['rx'], '1427150' )

    def test_send( self ):
        queue = MagicMock()
        dt = GetDateTime( year=2000, month=1, day=2, hour=3, minute=4, second=5 )
        key = 'tx'
        value = 12345

        listeners = [Constants.TopicNames.CurrentValueStep]
        data = {Constants.DataPacket.device: 'OMAP UART1',
                Constants.DataPacket.port: key,
                Constants.DataPacket.arrival_time: dt,
                Constants.DataPacket.current_value: value,
                Constants.DataPacket.listeners: copy.copy( listeners )}

        env = DataEnvelope( type=Constants.EnvelopeTypes.status, data=data, arrival_time=dt )

        cm = ComputerMonitor( queue )
        cm.send( dt, key, value )


    def test_process_data( self ):
        queue = MagicMock()
        dt = GetDateTime( year=2013, month=1, day=2, hour=3, minute=4, second=5 )
        packet = None
        data = {Constants.DataPacket.device: 'OMAP UART1',
                Constants.DataPacket.port: '1188940',
                Constants.DataPacket.current_value: 1,
                Constants.DataPacket.arrival_time: GetDateTime( dt )}
        envelope = DataEnvelope( type='Computer', data=data, arrival_time=dt )

        file_contents = {'tx': '1188940', 'rx': '1427150'}

        cmp = ComputerMonitor( queue )
        cmp.process_data( file_contents, dt )

        self.assertEqual( cmp.start_count['tx'], 1188940 )
        self.assertEqual( cmp.start_count['rx'], 1427150 )
        self.assertEqual( cmp.previous_count['tx'], 1188940 )
        self.assertEqual( cmp.previous_count['rx'], 1427150 )

        queue.reset_mock()
        dt = GetDateTime( datetime( 2013, 1, 2, 3, 4, 10 ) )


#         file_contents = {'tx': '1188960', 'rx': '1427170'}
#         cmp.process_data( file_contents, dt )
#         self.assertEqual( queue.transmit.call_count, 4 )
#         calls = queue.transmit.call_args_list
# #        print calls
#         self.assertEqual( cmp.start_count['tx'], 1188940 )
#         self.assertEqual( cmp.start_count['rx'], 1427150 )
#         self.assertEqual( cmp.previous_count['tx'], 20 )
#         self.assertEqual( cmp.previous_count['rx'], 20 )
#
#         # I'm not sure that this works. I've spent hours trying to get it to work.
#         self.assertNotIn( call( priority=10, packet=DataEnvelope( type='status', packet=None, arrival_time='2013/01/02 03:04:10', data={'device': 'OMAP UART1', 'current_value': 20, 'port': 'rx', 'at': '2013/01/02 03:04:10'} ) ), calls )
#         self.assertNotIn( call( priority=10, packet=DataEnvelope( type='status', packet=None, arrival_time='2013/01/02 03:04:10', data={'device': 'OMAP UART1', 'current_value': 4.0, 'port': 'rx rate', 'at': '2013/01/02 03:04:10'} ) ), calls )
#         self.assertNotIn( call( priority=10, packet=DataEnvelope( type='status', packet=None, arrival_time='2013/01/02 03:04:10', data={'device': 'OMAP UART1', 'current_value': 20, 'port': 'tx', 'at': '2013/01/02 03:04:10'} ) ), calls )
#         self.assertNotIn( call( priority=10, packet=DataEnvelope( type='status', packet=None, arrival_time='2013/01/02 03:04:10', data={'device': 'OMAP UART1', 'current_value': 4.0, 'port': 'tx rate', 'at': '2013/01/02 03:04:10'} ) ), calls )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_logger_name']
    unittest.main()

data = '''
serinfo:1.0 driver revision:
0: uart:OMAP UART0 mmio:0x44E09000 irq:72 tx:85 rx:0 CTS|DSR
1: uart:OMAP UART1 mmio:0x48022000 irq:73 tx:1188940 rx:1427150 RTS|CTS|DTR|DSR|CD|RI
2: uart:OMAP UART2 mmio:0x48024000 irq:74 tx:0 rx:0 CTS|DSR
3: uart:OMAP UART3 mmio:0x481A6000 irq:44 tx:0 rx:0 CTS|DSR
4: uart:OMAP UART4 mmio:0x481A8000 irq:45 tx:0 rx:0 CTS|DSR
5: uart:OMAP UART5 mmio:0x481AA000 irq:46 tx:0 rx:0 CTS|DSR
'''
data1 = '''
serinfo:1.0 driver revision:
0: uart:OMAP UART0 mmio:0x44E09000 irq:72 tx:85 rx:0 CTS|DSR
1: uart:OMAP UART1 mmio:0x48022000 irq:73 tx:1188940 rx:1427150 RTS|CTS|DTR|DSR|CD|RI
2: uart:OMAP UART2 mmio:0x48024000 irq:74 tx:0 rx:0 CTS|DSR
3: uart:OMAP UART3 mmio:0x481A6000 irq:44 tx:0 rx:0 CTS|DSR
4: uart:OMAP UART4 mmio:0x481A8000 irq:45 tx:0 rx:0 CTS|DSR
5: uart:OMAP UART5 mmio:0x481AA000 irq:46 tx:0 rx:0 CTS|DSR
'''
