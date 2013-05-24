'''
Created on May 5 2013

@author: Gary
'''
from apscheduler.scheduler import Scheduler
from datetime import timedelta
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib.getdatetime import GetDateTime
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.hmscheduler import HMScheduler
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
    sched = None

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        if self.sched != None:
            self.sched.shutdown()
        sched = None


    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_init( self, que, sub ):
        self.sched = HMScheduler( que )
        self.assertIs( self.sched._input_queue, que )
        sub.assert_any_call( self.sched.add_interval, Constants.TopicNames.SchedulerAddIntervalStep )
        sub.assert_any_call( self.sched.add_cron, Constants.TopicNames.SchedulerAddCronStep )
        sub.assert_any_call( self.sched.add_date, Constants.TopicNames.SchedulerAddDateStep )
        sub.assert_any_call( self.sched.add_one_shot, Constants.TopicNames.SchedulerAddOneShotStep )
        sub.assert_any_call( self.sched.deleteJob, Constants.TopicNames.SchedulerDeleteJob )
        sub.assert_any_call( self.sched.print_jobs, Constants.TopicNames.SchedulerPrintJobs )
        self.sched.shutdown()
        self.sched = None


    @patch.object( HMQueue, 'transmit' )
    def test_logger_name( self, tx ):
        self.sched = HMScheduler( tx )
        self.assertEqual( self.sched.logger_name, Constants.LogKeys.Scheduler )
        self.sched.shutdown()
        self.sched = None

    @patch.object( HMQueue, 'transmit' )
    def test_scheduler_topic_name( self, tx ):
        self.sched = HMScheduler( tx )
        self.assertEqual( self.sched.scheduler_topic_name, Constants.TopicNames.SchedulerStep )
        self.sched.shutdown()
        self.sched = None

    @patch.object( Scheduler, 'add_interval_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_start( self, que, sub, start, add_interval_job ):
        try:
            uuid.uuid4 = Mock()
            uuid.uuid4.return_value = '1234567'
            self.sched = HMScheduler( que )
            self.sched.start()

            start.assert_called_once_with()

            name = 'scheduled status check'
            device = 'status'
            port = 'scheduler'
            listeners = [Constants.TopicNames.Statistics, Constants.TopicNames.CurrentValueStep]
            scheduler_id = '1234567'
            args = name, device, port, listeners, scheduler_id
            add_interval_job.assert_any_call( self.sched.sendCommand, minutes=10, args=args )

            name = 'uptime'
            device = 'HouseMonitor'
            port = 'uptime'
            listeners = [Constants.TopicNames.UpTime, Constants.TopicNames.CurrentValueStep]
            scheduler_id = '1234567'
            args = name, device, port, listeners, scheduler_id
            add_interval_job.assert_any_call( self.sched.sendCommand, seconds=5, args=args )

            name = 'Pulse'
            device = '0x13a20040902a02'
            port = 'DIO-0'
            listeners = [ Constants.TopicNames.StatusPanel_SystemCheck]
            scheduler_id = '1234567'
            args = name, device, port, listeners, scheduler_id
            print add_interval_job.call_args_list
            add_interval_job.assert_any_call( self.sched.sendCommand, seconds=5, args=( 'Pulse', '0x13a20040902a02', 'DIO-0', ['step.StatusPanel_SystemCheck', 'step.ZigBeeOutput'], '1234567' ) )
        finally:
            self.sched.shutdown()
            self.sched = None

    @patch.object( Scheduler, 'add_interval_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_interval( self, que, sub, start, add_interval_job ):
        self.sched = HMScheduler( que )
        self.sched.start()
        add_interval_job.reset_mock()
        add_interval_job.return_value = 555

        name = 'Unit Test'
        weeks = 1
        days = 2
        hours = 3
#         minutes = 4
#         seconds = 5
#         start_date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
#         args = ( name )
#         kwargs = 456
#         self.sched.add_interval( weeks, days, hours, minutes, seconds, start_date, args, kwargs )
#
#         add_interval_job.assert_called_once_with( self.sched.sendCommand, seconds=5,
#             args=name, days=2, hours=3, kwargs=456, weeks=1, minutes=4,
#             start_date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ) )

        self.sched.shutdown()
        self.sched = None

    @patch.object( Scheduler, 'add_cron_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_cron( self, que, sub, start, add_cron_job ):
        self.sched = HMScheduler( que )
        self.sched.start()
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
        args = ( name )
        kwargs = 456
        self.sched.add_cron( year, month, day, week, day_of_week,
                  hour, minute, second, start_date, args, kwargs )

        add_cron_job.assert_called_once_with( self.sched.sendCommand, week=99, hour=3, args=args,
                                              year=2013, day_of_week=1, month=1, second=5,
                                              minute=4, kwargs=456,
                                              start_date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ),
                                               day=2 )
        self.sched.shutdown()
        self.sched = None

    @patch.object( Scheduler, 'add_date_job' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_add_date( self, que, sub, start, add_date_job ):
        self.sched = HMScheduler( que )
        self.sched.start()
        add_date_job.reset_mock()
        add_date_job.return_value = 555
        self.sched.jobs['Unit Test'] = []

        name = 'Unit Test'
        device = 'device'
        port = 'port'
        listeners = []
        scheduler_id = str( uuid.uuid4() )
        date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = ( name, device, port, listeners, scheduler_id )
#         kwargs = {}
#         self.sched.add_date( date, args, kwargs )
#
#         add_date_job.assert_called_once_with( self.sched.sendCommand,
#                                                date=datetime.datetime( 2013, 1, 2, 3, 4, 5 ),
#                                                *args, **kwargs )
#
#         self.assertListEqual( self.sched.jobs[name], [555, 555] )
        self.sched.shutdown()
        self.sched = None

    @patch( 'housemonitor.lib.getdatetime.GetDateTime.datetime' )
    def test_add_one_shot( self, dt ):
        d = datetime.datetime( 2013, 1, 1, 1, 1, 1 )
        dt.return_value = d
        que = MagicMock()
        self.sched = HMScheduler( que )
        self.sched.scheduler = MagicMock()
        self.sched.scheduler.add_date_job = MagicMock()
        self.sched.scheduler.add_date_job.return_value = 99
        self.sched.jobs['test'] = []

        delta = timedelta( seconds=1 )
        name = 'Unit Test'
        args = ( 'test', 1, 2, 3 )
        kwargs = 456
        self.sched.add_one_shot( delta, args, kwargs )
        self.assertListEqual( self.sched.jobs['test'], [99] )
        self.assertEqual( self.sched.scheduler.add_date_job.call_count, 1 )

        self.sched.shutdown()
        self.sched = None


    def test_deleteJob( self, ):
        que = MagicMock()
        self.sched = HMScheduler( que )
        self.sched.start()
        self.sched.scheduler = MagicMock( spec=Scheduler )
        self.sched.scheduler.add_date_job.return_value = 55

        name = 'test1'
        device = 'a'
        port = 'b'
        listeners = ['c', 'd']
        date = datetime.datetime( 2013, 1, 2, 3, 4, 5 )
        args = name, device, port, listeners
        kwargs = {}
        self.sched.jobs['test1'] = []

        self.sched.add_date( date, args, **kwargs )
        date = datetime.datetime( 2013, 1, 2, 3, 4, 6 )
        self.sched.add_date( date, args )

        name = 'test2'
        args = name, device, port, listeners
        self.sched.add_date( date, args )
        self.assertListEqual( self.sched.jobs['test1'], [55, 55] )
        self.sched.deleteJob( 'test1' )
        self.assertListEqual( self.sched.jobs['test1'], [] )
        self.sched.scheduler.unschedule_job.assert_any_call( 55 )
        self.assertEqual( self.sched.scheduler.unschedule_job.call_count, 2 )
        self.sched.scheduler.unschedule_job.reset_mock()

        self.sched.deleteJob( 'test3' )
        self.assertEqual( self.sched.scheduler.unschedule_job.call_count, 0 )

        self.sched.shutdown()
        self.sched = None

    @patch.object( Scheduler, 'shutdown' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_shutdown( self, que, sub, start, shutdown ):
        self.sched = HMScheduler( que )
        self.sched.start()
        self.sched.shutdown( wait=True )
        shutdown.assert_called_once_with( wait=True )
        shutdown.reset_mock()
        self.assertIsNone( self.sched.scheduler )

        self.sched.shutdown( wait=True )
        self.assertEqual( shutdown.call_count, 0 )
        self.sched.shutdown()
        self.sched = None

    @patch.object( Scheduler, 'print_jobs' )
    @patch.object( Scheduler, 'start' )
    @patch.object( pub, 'subscribe' )
    @patch.object( HMQueue, 'transmit' )
    def test_print_jobs( self, que, sub, start, print_jobs ):
        self.sched = HMScheduler( que )
        self.sched.start()
        self.sched.print_jobs()
        print_jobs.assert_called_once_with()
        self.sched.shutdown()
        self.sched = None

    @patch.object( GetDateTime, "__repr__" )
    @patch.object( GetDateTime, "__str__" )
    def test_sendCommand( self, str, rept ):
        str.return_value = "a"
        rept.return_value = "'a'"
        queue = MagicMock( spec=HMQueue )
        self.sched = HMScheduler( queue )

        device = 1
        port = 2
        listeners = ['a', 'b']
        scheduler_id = 1
        name = 'keep on keeping on'
        self.sched.sendCommand( name, device, port, listeners, scheduler_id )
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
        self.sched.shutdown()
        self.sched = None


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
