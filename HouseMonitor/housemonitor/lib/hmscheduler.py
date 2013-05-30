'''
Created on 2012-05-04

@author: Gary

'''
from apscheduler.jobstores.shelve_store import ShelveJobStore
from apscheduler.scheduler import Scheduler
from housemonitor.configuration.formatconfiguration import FormatConfiguration
from datetime import date, datetime, time, timedelta
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants
from housemonitor.lib.getdatetime import GetDateTime
from collections import defaultdict
from pubsub import pub
import copy
import pprint
import uuid



class HMScheduler( Base ):
    '''
    The HMSceduler is used to periodically to send messages to HouseMonitor.  The commands can anything including:

    # Report status
    # Turn on and off devices.

    You control the scheduler by sending messages to the scheduler using pubsub.
    '''

    ''' The queue that is used to send messages to the rest of the system. '''
    _input_queue = None

    ''' The scheduler object '''
    scheduler = None

    ''' A dictionary of the current jobs that are running '''
    jobs = defaultdict( list )

    previous_datetime = datetime.utcnow()

    def __init__( self, queue ):
        '''
        Initialize the MHScheduler.

        # Store the queue into _input_queue
        # Associate **add_interval** with Constants.TopicNames.SchedulerAddIntervalStep
        # Associate **add_cron** with Constants.TopicNames.SchedulerAddCronStep
        # Associate **add_date** with Constants.TopicNames.SchedulerAddDateStep
        # Associate **add_one_shot with Constants.TopicNames.SchedulerAddOneShotStepSchedulerAddOneShotStep
        # Associate **delete_job** with Constants.TopicNames.SchedulerDeleteJob
        '''
        super( HMScheduler, self ).__init__()
        self._input_queue = queue
        pub.subscribe( self.add_interval, Constants.TopicNames.SchedulerAddIntervalStep )
        pub.subscribe( self.add_cron, Constants.TopicNames.SchedulerAddCronStep )
        pub.subscribe( self.add_date, Constants.TopicNames.SchedulerAddDateStep )
        pub.subscribe( self.add_one_shot, Constants.TopicNames.SchedulerAddOneShotStep )
        pub.subscribe( self.deleteJob, Constants.TopicNames.SchedulerDeleteJob )
        pub.subscribe( self.print_jobs, Constants.TopicNames.SchedulerPrintJobs )

    @property
    def scheduler_topic_name( self ):
        ''' The topic name to which this routine subscribes.'''
        return Constants.TopicNames.SchedulerStep

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.Scheduler

    def start( self ):
        '''
        Start the Scheduler.

        For more information on the parameter see:

        .. seealso:: http://packages.python.org/APScheduler/#starting-the-scheduler

        '''
        self.logger.debug( 'Scheduler starting' )
        self.scheduler = Scheduler()
#        self.logger.debug( 'Setting jobstore to HouseMonitor.db' )
#        self.scheduler.add_jobstore(ShelveJobStore('HouseMonitor.db'), 'shelve')
        self.scheduler.start()

        name = 'scheduled status check'
        device = 'status'
        port = 'scheduler'
        listeners = [Constants.TopicNames.Statistics, Constants.TopicNames.CurrentValueStep]
        scheduler_id = str( uuid.uuid4() )
        args = name, device, port, listeners, scheduler_id
        self.scheduler.add_interval_job( self.sendCommand, minutes=10, args=args )

        name = 'uptime'
        device = 'HouseMonitor'
        port = 'uptime'
        listeners = [Constants.TopicNames.UpTime, Constants.TopicNames.CurrentValueStep]
        scheduler_id = str( uuid.uuid4() )
        args = name, device, port, listeners, scheduler_id
        self.scheduler.add_interval_job( self.sendCommand, seconds=5, args=args )

        name = 'Pulse'
        device = '0x13a20040902a02'
        port = 'DIO-0'
        listeners = [ Constants.TopicNames.StatusPanel_SystemCheck, Constants.TopicNames.ZigBeeOutput]
        scheduler_id = str( uuid.uuid4() )
        args = name, device, port, listeners, scheduler_id
        self.scheduler.add_interval_job( self.sendCommand, seconds=5, args=args )

    def add_interval( self, weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, args=None, kwargs=None ):
        '''
        Schedule an interval at which sendCommand will be called.

        For more information on the parameter see:

            .. seealso:: http://packages.python.org/APScheduler/intervalschedule.html

        :param name: the name of the job to start. This will be used to identify the job if there is a need to delete it latter.
        :type name: str
        :param weeks: the number of weeks between calls.
        :type weeks: int
        :param days: the number of days between calls.
        :type days: int
        :param hours: the number of hours between calls.
        :type hours: int
        :param minutes: the number of minutes between calls.
        :type minutes: int
        :param seconds: the number of seconds between calls.
        :type seconds: int
        :param start_date: the time and date to start the interval.
        :type start_date: datetime
        :param args: the args to pass to sendCommand
        :param kwargs: the kwargs to pass to sendCommand
        :raises: None

        '''
        name = args[0]
        self.logger.debug( 'interval ({}) add {} {} {} {} {} {} {}'.format( name, weeks, days, hours, hours, minutes, seconds, start_date ) )
        token = self.scheduler.add_interval_job( self.sendCommand, weeks=weeks,
                        days=days, hours=hours, minutes=minutes, seconds=seconds,
                        start_date=start_date, args=args, kwargs=kwargs, name=name )
        self.jobs[name].append( token )

    def add_cron( self, year=None, month=None, day=None, week=None, day_of_week=None,
                  hour=None, minute=None, second=None, start_date=None, args=None, kwargs=None ):
        '''
        Schedule a cron command to call sendCommand.

        For more information on the parameter see:

            .. seealso:: http://packages.python.org/APScheduler/cronschedule.html

        :param name: the name of the cron job to start. This will be used to identify the job if there is a need to delete it latter.
        :type weeks: str
        :param weeks: the number of weeks between calls.
        :type weeks: int
        :param days: the number of days between calls.
        :type days: int
        :param hours: the number of hours between calls.
        :type hours: int
        :param minutes: the number of minutes between calls.
        :type minutes: int
        :param seconds: the number of seconds between calls.
        :type seconds: int
        :param start_date: the time and date to start the interval.
        :type start_date: datetime
        :param args: the args to pass to sendCommand
        :param kwargs: the kwargs to pass to sendCommand
        :raises: None

        '''
        name = args[0]
        self.logger.debug( 'set cron({}) at {}/{}/{} {}:{}:{} {} {} {}'.format( name, year, month,
                                day, hour, minute, second, week, day_of_week, start_date ) )
        token = self.scheduler.add_cron_job( self.sendCommand, year=year,
                    month=month, day=day, week=week, day_of_week=day_of_week, hour=hour,
                    minute=minute, second=second, start_date=start_date, args=args, kwargs=kwargs )
        self.jobs[name].append( token )

    def add_date( self, date, args, **kwargs ):
        '''
        Schedule a specific data and time to call sendCommand.

        For more information on the parameter see:

            .. seealso:: http://packages.python.org/APScheduler/dateschedule.html

        :param name: the name of the cron job to start. This will be used to identify the job if there is a need to delete it latter.
        :type weeks: str
        :param date: Set the time to call sendCommand
        :type date: datetime
        :param args: the arguments to call sendCommand with
        :type weeks: tuple
        :param date: the kwwargs to call sendCommand with
        :type date: dictionary

        '''
        name = args[0]

        self.logger.debug( 'add date({}) at {}'.format( name, date ) )
        token = self.scheduler.add_date_job( self.sendCommand, date=date,
                                                             args=args, kwargs=kwargs )
        self.jobs[name].append( token )

    def add_one_shot( self, delta, args=None, kwargs=None ):
        '''
        Schedule sendCommand to be called after some interval. (ie. in 5 seconds or one hour).  For more information
        on timeDelta see:

        .. seealso:: http://docs.python.org/2/library/datetime.html#timedelta-objects

        :param name: delta the time until sendCommand is called
        :type weeks: timedelta
        :param date: Set the time to call sendCommand
        :type date: datetime
        :param args: the arguments to call sendCommand with
        :type weeks: tuple
        :param date: the kwwargs to call sendCommand with
        :type date: dictionary

        '''
        name = args[0]
        now = GetDateTime()
        dt = now.datetime()
        dt = dt + delta
        token = self.scheduler.add_date_job( self.sendCommand, date=dt,
                                name=name, args=args, kwargs=kwargs )
        self.jobs[name].append( token )

    def deleteJob( self, name ):
        '''
        Delete a specified job

        :param name: the name of the job to delete.
        :type weeks: str

        '''
        item = None
        if name in self.jobs:
            for number, item in enumerate( self.jobs[name] ):
                try:
                    self.scheduler.unschedule_job( item )
                except KeyError:
                    pass
                self.logger.info( '{} "{}" removed from scheduler'.format( number, name ) )
            self.jobs[name] = []

    def shutdown( self, wait=True ):
        '''
        shutdown the scheduler

        .. seealso: http://packages.python.org/APScheduler/#shutting-down-the-scheduler

        :param wait: determines whether to wait on threads to commplete.
        :type wait: boolean

        '''

        if ( self.scheduler != None ):
            self.scheduler.shutdown( wait=wait )
            self.scheduler = None

    def print_jobs( self ):
        '''
        print tye currently scheduled jobs

        .. seealso: http://packages.python.org/APScheduler/#getting-a-list-of-scheduled-jobs

        '''
        self.scheduler.print_jobs()

    def sendCommand( self, name, device, port, listeners=[], scheduler_id=str( uuid.uuid4() ) ):
        """
        send command will send the cammand to the HouseMonitor system

        :param device: the device name.
        :type device: str
        :param port: the port name.
        :type days: str
        :param listeners: the listeners that this command will be routed to.
        :type listeners: list of strings that contains the topic name of the listeners.  Most can be found in Constants.TopicNames

        """
        data = {}
        data[Constants.DataPacket.device] = device
        data[Constants.DataPacket.port] = port
        data[Constants.DataPacket.scheduler_id] = scheduler_id
        data[Constants.DataPacket.arrival_time] = GetDateTime()
        data[Constants.DataPacket.listeners] = copy.copy( listeners )
        data[Constants.DataPacket.name] = name
        de = DataEnvelope( type=Constants.EnvelopeTypes.status, data=data )
        self.logger.debug( 'name = {} listeners = {} scheduler_id =  {}'.format( name, listeners,
                                                        data[Constants.DataPacket.scheduler_id] ) )
        self._input_queue.transmit( de, Constants.Queue.low_priority )
