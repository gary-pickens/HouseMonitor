'''
Created on Apr 12, 2013

@author: Gary
'''
import unittest
import datetime
from lib.common import Common
import logging.config
from lib.constants import Constants
import pprint
from mock import Mock, patch, MagicMock
from lib.getdatetime import GetDateTime
from inputs import dataenvelope
from inputs.computermonitor.computermonitor import MonitorComputer


class Test( unittest.TestCase ):


    def setUp( self ):
        pass


    def tearDown( self ):
        pass


    def test_logger_name( self ):
        queue = MagicMock()
        cmp = MonitorComputer( queue )
        self.assertEqual( cmp.logger_name, Constants.LogKeys.ComputerMonitor )

    def test_extractData( self ):
        queue = MagicMock()
        cmp = MonitorComputer( queue )

        counts = cmp.extractData( data )
        self.assertIsNotNone( counts )
        self.assertEqual( counts['tx'], '1188940' )
        self.assertEqual( counts['rx'], '1427150' )



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
