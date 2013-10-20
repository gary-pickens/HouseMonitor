'''
Created on Oct 17, 2013

@author: gary
'''
'''
Created on Oct 16, 2013

@author: gary
'''

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from housemonitor.lib.constants import Constants

Base = declarative_base()

class Device( Base ):
    '''
    This object contains all the information about the device.
    '''

    __tablename__ = "devices"

    id = Column( Integer, primary_key=True )
#     long_address = Column( String( 16 ) )
#     descriptive_name = Column( String )
#     network_address = Column( String )
    ports = relationship( "ports" )

    def __init__( self, long_address, descriptive_name, ports, network_address="" ):
        '''
        Construct an object that contains all the data that is held by
        this object and table.

        :param long_address:
        :param descriptive_name:
        :param network_address:
        '''
#         self.long_address = long_address
#         self.descriptive_name = descriptive_name
#         self.network_address = network_address

    def __repr__( self ):
        return "<Device({} {} {})>".format( 
                        self.long_address,
                        self.descriptive_name,
                        self.network_address )


class Ports( Base ):
    '''
    classdocs
    '''

    __tablename__ = "ports"

    id = Column( Integer, primary_key=True )
#     port_name = Column( String( 16 ) )
#     descriptive_name = Column( String )
#     units = Column( String )
    devices_id = Column( Integer, ForeignKey( 'devices.id' ) )

#     def __init__( self, port_name, descriptive_name, units ):
#         '''
#         Construct an object that contains all the data that is held by
#         this object and table.
#         :param port_name:
#         :param descriptive_name:
#         :param units:
#         :param steps:
#         '''
#         self.port_name = port_name
#         self.descriptive_name = descriptive_name
#         self.units = units
#        self.steps = steps


    def __repr__( self ):
        return "<Device({}, {}, {}, {})>".format( 
                        self.long_address,
                        self.descriptive_name,
                        self.steps,
                        self.network_address )

class Steps( Base ):
    '''
    classdocs
    '''

    __tablename__ = "Steps"

    id = Column( Integer, primary_key=True )
    order = Column( Integer )
    port_id = relationship( "Ports", backref=backref( 'Steps', order_by=order ) )
    topic = Column( Integer, ForeignKey( 'StepNames.topic' ) )
    order = Column( Integer )



    def __init__( self, order, topics ):
        '''
        A table that contains the steps that data must pass
        thuugh.
        :param descriptive_name:
        :param order:
        '''
        self.topics = topics.id
        self.order = order

    def __repr__( self ):
        return "<Steps({}, {})>".format( self.order, self.topics )

class StepNames( Base ):
    '''
    classdocs
    '''

    __tablename__ = "StepNames"

    id = Column( Integer, primary_key=True )
    topic = Column( String )

    def __init__( self, topic ):
        '''
        :param step_name:
        '''
        self.topic = topic


    def __repr__( self ):
        return '<StepNames("{}")>'.format( self.topic )

if __name__ == '__main__':
    steps = [
        Constants.TopicNames.SchedulerAddIntervalStep,
        Constants.TopicNames.SchedulerAddDateStep,
        Constants.TopicNames.SchedulerAddCronStep,
        Constants.TopicNames.SchedulerAddOneShotStep,
        Constants.TopicNames.SchedulerDeleteJob,
        Constants.TopicNames.SchedulerPrintJobs,
        Constants.TopicNames.SchedulerStep,
        Constants.TopicNames.CurrentValueStep,
        Constants.TopicNames.AverageStep,
        Constants.TopicNames.Centigrade2FahrenheitStep,
        Constants.TopicNames.GarageDoorStateStep,
        Constants.TopicNames.FormatValueStep,
        Constants.TopicNames.onBooleanChangeStep,
        Constants.TopicNames.OneInNStep,
        Constants.TopicNames.TMP36Volts2CentigradeStep,
        Constants.TopicNames.ZigbeeAnalogNumberToVoltsStep,
        Constants.TopicNames.CentigradeToFahrenheitStep,
        Constants.TopicNames.MaxValue,
        Constants.TopicNames.MinValue,
        Constants.TopicNames.Statistics,
        Constants.TopicNames.UpTime,
        Constants.TopicNames.ZigBeeOutput,
        Constants.TopicNames.Step,
        Constants.TopicNames.StatusPanel_GarageDoorMonitor,
        Constants.TopicNames.StatusPanel_ProcessDelayedAlarm,
        Constants.TopicNames.StatusPanel_DisableAlarmButton,
        Constants.TopicNames.StatusPanel_SystemCheck,
        Constants.TopicNames.StatusPanel_SilenceAlarm,
        Constants.TopicNames.xmlDeviceConfiguration,
        Constants.TopicNames.Outputs,
        Constants.TopicNames.COSM,
        Constants.TopicNames.ProcessInputs,
        Constants.TopicNames.UnitTest,
        Constants.TopicNames.ALL_TOPICS,
    ]

    engine = create_engine( 'sqlite:///:memory:', echo=True )
    Session = sessionmaker( bind=engine )
    session = Session()
    Base.metadata.create_all( engine )

    p1 = Ports(),
    p2 = Ports( 'ADT-1', 'Garage Door', 'C', ['a', 'b'] )

    ports = [
             p1,
             p2
             ]
    devices = [
        Device( "0x13a200409029bf", "Garage Door XBee Monitor", ports, "0xf9f2" ),
        Device( "0x13a200408cccc3", "Sunroom", ports ),
        Device( "0x13a20040902867", "Kitchen", ports ),
        Device( "0x13a200408b68b5", "Outdoor", ports )
    ]
    for s in devices:
        session.add( s )

    for s in steps:
        sn = StepNames( s )
        session.add( sn )
    session.commit()

    topics = session.query( StepNames ).all()
    devices = session.query( Device ).all()
    st = [t.topic for t in topics]
    print( topics )
    print st

    cosm = session.query( StepNames ).filter( StepNames.topic == Constants.TopicNames.COSM ).all()
    alarm = session.query( StepNames ).filter( StepNames.topic == Constants.TopicNames.StatusPanel_SilenceAlarm ).all()
    l = []
    for i, s in enumerate( [cosm, alarm] ):
        l.append( Steps( i, s.id ) )

    print l

    print( devices )
    print( 'done' )


