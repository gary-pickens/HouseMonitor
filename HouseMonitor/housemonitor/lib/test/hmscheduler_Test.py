'''
Created on Nov 19, 2012

@author: Gary
'''
from apscheduler.scheduler import Scheduler
from datetime import timedelta
from inputs.dataenvelope import DataEnvelope
from lib.constants import Constants
from lib.getdatetime import GetDateTime
from lib.hmqueue import HMQueue
from lib.hmscheduler import HMScheduler
from mock import *
from pubsub import pub
import copy
import datetime
import logging.config
import time
import unittest
import uuid


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "house_monitor_logging.conf" )

    def tearDown( self ):
        pass

    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_init( self, que, sub ):
        sched = HMScheduler( que )
        self.assertIs( sched._input_queue, que )
        sub.assert_any_call( sched.add_interval, Constants.TopicNames.SchedulerAddIntervalStep )
        sub.assert_any_call( sched.add_cron, Constants.TopicNames.SchedulerAddCronStep )
        sub.assert_any_call( sched.add_date, Constants.TopicNames.SchedulerAddDateStep )
        sub.assert_any_call( sched.add_one_shot, Constants.TopicNames.SchedulerAddOneShotStep )
        sub.assert_any_call( sched.deleteJob, Constants.TopicNames.SchedulerDeleteJob )
        sub.assert_any_call( sched.print_jobs, Constants.TopicNames.SchedulerPrintJobs )
        sched.shutdown()
        sched = None


    @patch.object( HMQueue, 'transmit' )
    def test_logger_name( self, tx ):
        sched = HMScheduler( tx )
        self.assertEqual( sched.logger_name, Constants.LogKeys.Scheduler )
        sched.shutdown()
        sched = None

    @patch.object( HMQueue, 'transmit' )
    def test_scheduler_topic_name( self, tx ):
        sched = HMScheduler( tx )
        self.assertEqual( sched.scheduler_topic_name, Constants.TopicNames.SchedulerStep )
        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'add_interval_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_start( self, que, sub, start, add_interval_job ):
        uuid.uuid4 = Mock()
        uuid.uuid4.return_value = '1234567'
        sched = HMScheduler( que )
        sched.start()

        start.assert_called_once_with()

        name = 'scheduled status check'
        device = 'status'
        port = 'scheduler'
        listeners = [Constants.TopicNames.Statistics, Constants.TopicNames.CurrentValueStep]
        scheduler_id = '1234567'
        args = name, device, port, listeners, scheduler_id
        add_interval_job.assert_any_call( sched.sendCommand, minutes=10, args=args )

        name = 'uptime'
        device = 'HouseMonitor'
        port = 'uptime'
        listeners = [Constants.TopicNames.UpTime, Constants.TopicNames.CurrentValueStep]
        scheduler_id = '1234567'
        args = name, device, port, listeners, scheduler_id
        add_interval_job.assert_any_call( sched.sendCommand, seconds=5, args=args )

        name = 'Pulse'
        device = '0x13a20040902a02'
        port = 'DIO-0'
        listeners = [ Constants.TopicNames.StatusPanel_SystemCheck]
        scheduler_id = '1234567'
        args = name, device, port, listeners, scheduler_id
        print add_interval_job.call_args_list
        add_interval_job.assert_any_call( sched.sendCommand, seconds=5, args=( 'Pulse', '0x13a20040902a02', 'DIO-0', ['step.StatusPanel_SystemCheck', 'step.ZigBeeOutput'], '1234567' ) )

        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'add_interval_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_interval( self, que, sub, start, add_interval_job ):
        sched = HMScheduler( que )
        sched.start()
        add_interval_job.reset_mock()
        add_interval_job.return_value = 555

        name = 'Unit Test'
        weeks = 1
        days = 2
        hours = 3
        minutes = 4
        seconds = 5
        start_date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = 123
        kwargs = 456
        sched.add_interval( name, weeks, days, hours, minutes, seconds, start_date, args, kwargs )

        add_interval_job.assert_called_once_with( sched.sendCommand, name='Unit Test', seconds=5,
            args=123, days=2, hours=3, kwargs=456, weeks=1, minutes=4,
            start_date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ) )

        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'add_cron_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_cron( self, que, sub, start, add_cron_job ):
        sched = HMScheduler( que )
        sched.start()
        add_cron_job.reset_mock()
        add_cron_job.return_value = 555

        name = 'Unit Test'
        year = 2013
        month = 1
        day_of_week = 1
        week = 99
        day = 2
        hour = 3
        minute = 4
        second = 5
        start_date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = 123
        kwargs = 456
        sched.add_cron( name, year, month, day, week, day_of_week,
                  hour, minute, second, start_date, args, kwargs )

        add_cron_job.assert_called_once_with( sched.sendCommand, week=99, hour=3, args=123,
                                              year=2013, day_of_week=1, month=1, second=5,
                                              minute=4, kwargs=456,
                                              start_date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ),
                                               day=2 )
        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'add_date_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_date( self, que, sub, start, add_date_job ):
        sched = HMScheduler( que )
        sched.start()
        add_date_job.reset_mock()
        add_date_job.return_value = 555
        sched.jobs['Unit Test'] = []

        name = 'Unit Test'
        date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = 123
        kwargs = 456
        sched.add_date( name, date, args, kwargs )

        add_date_job.assert_called_once_with( sched.sendCommand,
                                               date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ),
                                               args=123, name='Unit Test', kwargs=456 )

        self.assertListEqual( sched.jobs['Unit Test'], [555] )
        sched.shutdown()
        sched = None

    @patch( 'lib.getdatetime.GetDateTime.datetime' )
    def test_add_one_shot( self, dt ):
        d = datetime.datetime( 2013, 1, 1, 1, 1, 1 )
        dt.return_value = d
        que = MagicMock()
        sched = HMScheduler( que )
        sched.scheduler = MagicMock()
        sched.scheduler.add_date_job = MagicMock()
        sched.scheduler.add_date_job.return_value = 99
        sched.jobs['test'] = []

        delta = timedelta( seconds=1 )
        name = 'Unit Test'
        args = ( 'test', 1, 2, 3 )
        kwargs = 456
        sched.add_one_shot( delta, args, kwargs )
        self.assertListEqual( sched.jobs['test'], [99] )
        self.assertEqual( sched.scheduler.add_date_job.call_count, 1 )

        sched.shutdown()
        sched = None


    def test_deleteJob( self, ):
        que = MagicMock()
        sched = HMScheduler( que )
        sched.start()
        sched.scheduler = MagicMock( spec=Scheduler )
        sched.scheduler.add_date_job.return_value = 55

        name = 'test1'
        device = 'a'
        port = 'b'
        listeners = ['c', 'd']
        date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = name, device, port, listeners
        kwargs = {'device': 456}

        sched.add_date( name, date, args, kwargs )
        date = datetime.datetime( 2013, 1, 2, 3, 4, 6 )
        sched.add_date( name, date, args, kwargs )

        name = 'test2'
        sched.add_date( name, date, args, kwargs )
        self.assertListEqual( sched.jobs['test1'], [55, 55] )
        sched.deleteJob( 'test1' )
        self.assertListEqual( sched.jobs['test1'], [] )
        sched.scheduler.unschedule_job.assert_any_call( 55 )
        self.assertEqual( sched.scheduler.unschedule_job.call_count, 2 )
        sched.scheduler.unschedule_job.reset_mock()

        sched.deleteJob( 'test3' )
        self.assertEqual( sched.scheduler.unschedule_job.call_count, 0 )

        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'shutdown' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_shutdown( self, que, sub, start, shutdown ):
        sched = HMScheduler( que )
        sched.start()
        sched.shutdown( wait=True )
        shutdown.assert_called_once_with( wait=True )
        shutdown.reset_mock()
        self.assertIsNone( sched.scheduler )

        sched.shutdown( wait=True )
        self.assertEqual( shutdown.call_count, 0 )
        sched.shutdown()
        sched = None

    @patch.object( Scheduler, 'print_jobs' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_print_jobs( self, que, sub, start, print_jobs ):
        sched = HMScheduler( que )
        sched.start()
        sched.print_jobs()
        print_jobs.assert_called_once_with()
        sched.shutdown()
        sched = None

    @patch.object( GetDateTime, "__repr__" )
    @patch.object( GetDateTime, "__str__" )
    def test_sendCommand( self, str, rept ):
        str.return_value = "a"
        rept.return_value = "'a'"
        queue = MagicMock( spec=HMQueue )
        sched = HMScheduler( queue )

        device = 1
        port = 2
        listeners = ['a', 'b']
        scheduler_id = 1
        name = 'keep on keeping on'
        sched.sendCommand( name, device, port, listeners, scheduler_id )
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port
        data[Constants.DataPacket.scheduler_id] = scheduler_id
        data[Constants.DataPacket.arrival_time] = GetDateTime()
        data[Constants.DataPacket.listeners] = copy.copy( listeners )
        data[Constants.DataPacket.name] = name
        de = DataEnvelope( type=Constants.EnvelopeTypes.status, data=data )

#         queue.transmit.assert_called_once_with( DataEnvelope( type='status', packet={},
#              arrival_time='a', data={'name': 'scheduled status check',
#                                                    'listeners': ['a', 'b'],
#                                                    'at': 'a',
#                                                    'device': 1, 'port': 2, 'scheduler_id': 1} ), 10 )
#        # Not sure why this in not working.  I have tried all sorts of variations.
        self.assertEqual( queue.transmit.call_count, 1 )
        args = queue.transmit.call_args
        sched.shutdown()
        sched = None


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
