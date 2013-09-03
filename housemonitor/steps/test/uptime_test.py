'''
Created on Mar 6, 2013

@author: Gary
'''
import unittest
from housemonitor.steps.uptime import uptime
from housemonitor.steps.uptime import instantuate_me
from housemonitor.lib.constants import Constants
from datetime import datetime
import time


class Test( unittest.TestCase ):

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

#     def test_uptime( self ):
#         data = {}
#         value = None
#         listeners = []
#         data[Constants.GlobalIndexs.start_time] = datetime.utcnow()
#         uptime = instantuate_me( data )
# #         time.sleep(2.2)
# #         v, d, l = uptime.step(value, data, listeners)
# #         self.assertEqual(v, "0:00:02")

    def test_topic_name( self ):
        data = {}
        value = None
        listeners = []
        data = {Constants.GlobalIndexs.start_time: datetime.utcnow()}
        uptime = instantuate_me( data )
        self.assertEqual( uptime.topic_name, Constants.TopicNames.UpTime )

    def test_logger_name( self ):
        data = {}
        value = None
        listeners = []
        data = {Constants.GlobalIndexs.start_time: datetime.utcnow()}
        uptime = instantuate_me( data )
        self.assertEqual( uptime.logger_name, Constants.LogKeys.steps )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
