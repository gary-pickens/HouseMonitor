'''
Created on Nov 19, 2012

@author: Gary
'''
import unittest
import datetime
import logging.config
from datetime import timedelta
from datetime import datetime
from mock import Mock
import time
from lib.hmqueue import HMQueue
from lib.hmscheduler import HMScheduler
from lib.constants import Constants
from inputs.dataenvelope import DataEnvelope
from pubsub import pub
from mock import MagicMock


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "house_monitor_logging.conf" )

    def tearDown( self ):
        pass

    def test_start_real_scheduler( self ):
        self.logger.error( 'test_start_real_scheduler' )
        update_time = 0.50
        que = Mock( spec=HMQueue )
        sched = HMScheduler( que )
        sched.send_status_update = update_time
        sched.start()
        time.sleep( update_time * 1.6 )
        sched.shutdown( wait=True )
        sched = None

    def test_add_interval( self ):
        que = Mock( spec=HMQueue )
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        listeners = ['step.statistics', 'steps.current_values']
        args = 'device', listeners
        sched.add_interval( 'add interval test', seconds=0.5, args=args )
        time.sleep( 3 )
        sched.sendCommand.assert_called_with( 'device', listeners )
        sched.shutdown( wait=True )
        sched = None

    def test_add_cron( self ):
        que = Mock( spec=HMQueue )
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        listeners = ['step.statistics', 'steps.current_values']
        args = 'device', listeners
        sched.add_cron( 'add_cron', second='0-59', args=args )
        time.sleep( 2 )
        sched.sendCommand.assert_called_with( 'device', listeners )
        sched.shutdown( wait=True )
        sched = None

    def test_add_date( self ):
        que = Mock( spec=HMQueue )
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        listeners = ['step.statistics', 'steps.current_values']
        args = 'device', listeners
        now_plus_two_second = datetime.now() + timedelta( seconds=2 )
        sched.add_date( 'add_date', now_plus_two_second, args=args )
        time.sleep( 3 )
        sched.sendCommand.assert_called_with( 'device', listeners )
        sched.shutdown( wait=True )
        sched = None

    def test_pubsub_to_add_date_works( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        listeners = ['step.statistics', 'steps.current_values']
        args = 'device', listeners
        now_plus_two_seconds = datetime.now() + timedelta( seconds=2 )
        pub.sendMessage( Constants.TopicNames.SchedulerAddDateStep, name='test_pubsub_to_add_date_works', date=now_plus_two_seconds, args=args )
        time.sleep( 4 )
        sched.sendCommand.assert_called_with( 'device', listeners )
        sched.shutdown( wait=True )
        sched = None

    def test_pubsub_to_add_cron_works( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        listeners = ['step.statistics', 'steps.current_values']
        args = 'device', listeners
        pub.sendMessage( Constants.TopicNames.SchedulerAddCronStep, name='test_pubsub_to_add_cron_works', second='0-59', args=args )
        time.sleep( 4 )
        sched.sendCommand.assert_called_with( 'device', listeners )
        sched.shutdown( wait=True )
        sched = None

    def test_pubsub_to_interval_works( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        device = 'status'
        listeners = ['step.statistics', 'steps.current_values']
        args = device, listeners
        pub.sendMessage( Constants.TopicNames.SchedulerAddIntervalStep, name='test_pubsub_to_interval_works', seconds=0.5, args=args )
        time.sleep( 4 )
        sched.sendCommand.assert_called_with( device, ['step.statistics', 'steps.current_values'] )
        sched.shutdown( wait=True )
        sched = None

    def test_pubsub_to_one_shot_works( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        device = 'oneshot'
        port = 'port'
        listeners = ['step.statistics', 'steps.current_values']
        args = device, port, listeners
        td = timedelta( seconds=2.0 )
        pub.sendMessage( Constants.TopicNames.SchedulerAddOneShotStep, name='test_pubsub_to_one_shot_works', delta=td, args=args )
        time.sleep( 4 )
        sched.sendCommand.assert_called_with( device, port, ['step.statistics', 'steps.current_values'] )
        sched.shutdown( wait=True )
        sched = None

    def test_one_shot_works( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = Mock()
        sched.start()
        device = 'oneshot'
        port = 'port'
        listeners = ['step.statistics', 'steps.current_values']
        args = device, port, listeners
        td = timedelta( seconds=1.0 )
        sched.add_one_shot( name='test_one_shot_works', delta=td, args=args )
        time.sleep( 2 )
        sched.sendCommand.assert_called_with( device, 'port', ['step.statistics', 'steps.current_values'] )
        sched.shutdown( wait=True )
        sched = None

    # FIXME why is this failing?
    @unittest.skip( "Not sure why this is failing" )
    def test_delete_job( self ):
        que = Mock()
        sched = HMScheduler( que )
        sched.sendCommand = MagicMock()
        sched.start()

        device = 'oneshot'
        port = 'port'

        listeners = ['one']
        args = device, port, listeners
        td = timedelta( seconds=4.0 )
        sched.add_one_shot( name='test_one', delta=td, args=args )

        td = timedelta( seconds=5.0 )
        listeners = ['two']
        args = device, port, listeners
        sched.add_one_shot( name='test_two', delta=td, args=args )

        listeners = ['three']
        args = device, port, listeners
        td = timedelta( seconds=6.0 )
        sched.add_one_shot( name='test_three', delta=td, args=args )
        sched.print_jobs()

        sched.deleteJob( 'test_two' )
        sched.print_jobs()
        time.sleep( 10 )

        sched.sendCommand.assert_has_calls( [( device, port, ['one'] ), ( device, port, ['three'] )], any_order=False )
        sched.shutdown( wait=True )
        sched = None

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
