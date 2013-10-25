'''
Created on Oct 19, 2013

@author: gary
'''
import threading
import time
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from housemonitor.lib.hmqueue import HMQueue
from housemonitor.inputs.dataenvelope import DataEnvelope
from housemonitor.lib.constants import Constants
from housemonitor.lib.base import Base

SqlBase = declarative_base()

class Data ( SqlBase ):
    '''
    This object contains selected data received from the remote XBees.
    '''

    __tablename__ = "data"

    id = Column( Integer, primary_key=True )
    device = Column( String( 20 ) )
    port = Column( String(10) )
    value = Column( String(10) )
    units = Column( String(3) )
    arrival_datetime = Column ( DateTime( ) )

    def __init__( self, value, units, device, port, arrival_datetime ):
        super( Data, self ).__init__()
        self.value = value
        self.units = units
        self.device = device
        self.port = port
        self.arrival_datetime = arrival_datetime

    def __repr__( self ):
        return '<Data({}, "{}", "{}", "{}", {})>'.format( 
                                               self.value,
                                               self.units,
                                               self.device,
                                               self.port,
                                               self.arrival_datetime
                                               )


class SqlAlchemyOutputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    output_queue = None
    zigbee_output = None
    done = False
    connectedToDatabase = False
    in_test_mode = False  # Set True when running in test mode
    
    databaseHost = "ubu"
    databaseUser = "root"
    databasePassword = "Helena&Patrick"
    databaseProgram = "mysql"
    databaseDriver = "mysqldb"
    database = 'housemonitor' if not in_test_mode else 'housemonitor.test'
    
    connectionString = "{}+{}://{}:{}@{}/{}".format(
                                                databaseProgram,
                                                databaseDriver,
                                                databaseUser,
                                                databasePassword,
                                                databaseHost,
                                                database)

    def __init__( self, queue, in_test_mode ):
        '''
        
        :param queue:
        :param in_test_mode: A boolean that indicates whetber the software is in test 
        mode of actually running.
        '''
        super( SqlAlchemyOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue
        self.in_test_mode = in_test_mode

    @property
    def logger_name( self ):
        return Constants.LogKeys.SQL_ALCHEMY_LOG

    def connect(self):
        self.connectedToDatabase = False
        try:
            engine = create_engine( self.connectionString, echo=True )
            Session = sessionmaker( bind=engine )
            self.session = Session()
            SqlBase.metadata.create_all( engine )
            self.connectedToDatabase = True
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            self.logger.exception( "Exception connecting to database in  sqlAlchemy" )

    def storeData(self, packet):
        try:
            value = packet[Constants.DataPacket.value]
            units = packet[Constants.DataPacket.units]
            device = packet[Constants.DataPacket.device]
            port = packet[Constants.DataPacket.port]
            arrival_time = packet[Constants.DataPacket.arrival_time]
    
            data = Data( value, units, device, port, arrival_time )
            self.session.add( data )
            self.session.commit()
            self.logger.error( "Successfully committed data do database" )
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            self.logger.exception( "Exception in sqlAlchemy thread" )

    def run( self ):
        try:
            while self.loop_forever:
                # wait for data
                packet = self.output_queue.receive()
    
                while not self.connectedToDatabase:
                    self.connect()
    
                self.storeData(packet)
        except KeyboardInterrupt:
            return
