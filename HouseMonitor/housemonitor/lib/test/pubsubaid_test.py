'''
Created on Apr 28, 2013

@author: Gary
'''
from housemonitor.lib.constants import Constants
from housemonitor.lib.pubsubaid import PubSubAid
from mock import *
from pubsub import pub
import unittest
import logging.config


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pub.setTopicUnspecifiedFatal( False )

    @patch.object( pub, 'subscribe' )
    def test_init( self, sub ):
        pubsubaid = PubSubAid()
        sub.assert_any_call( pubsubaid.step, Constants.TopicNames.Step )
        sub.assert_any_call( pubsubaid.outputs, Constants.TopicNames.Outputs )
        sub.assert_any_call( pubsubaid.all_topics, Constants.TopicNames.ALL_TOPICS )
        pubsubaid = None

    def test_outputs( self ):
        pubsubaid = PubSubAid()
        pubsubaid.outputs()
        pubsubaid = None

    def test_all_topics( self ):
        pubsubaid = PubSubAid()
        pubsubaid.all_topics()
        pubsubaid = None

    def test_step( self ):
        pubsubaid = PubSubAid()
        pubsubaid.step()
        pubsubaid = None

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
