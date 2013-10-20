'''
Created on Oct 19, 2013

@author: gary
'''
import threading
import time
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
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
    device = Column( String( 16 ) )
    port = Column( String )
    value = Column( String )
    units = Column( String )
    arrival_datetime = Column ( DateTime( timezone=True ) )

    def __init__( self, value, units, device, port, arrival_datetime ):
        super( Data, self ).__init__()
        self.value = value
        self.units = units
        self.device = device
        self.port = port
        self.arrival_datetime = arrival_datetime

    def __repr__( self ):
        return "<Data({}, {}, {}, {})>".format( 
                                               self.value,
                                               self.units,
                                               self.arrival_datetime,
                                               self.device,
                                               self.port
                                               )


class SqlAlchemyOutputThread( Base, threading.Thread ):
    '''
    classdocs
    '''

    output_queue = None
    zigbee_output = None
    done = False

    def __init__( self, queue, in_test_mode ):
        '''
        
        :param queue:
        :param in_test_mode:
        '''
        super( SqlAlchemyOutputThread, self ).__init__()
        threading.Thread.__init__( self )
        self.output_queue = queue
        self.in_test_mode = in_test_mode

    @property
    def logger_name( self ):
        return Constants.LogKeys.SQL_ALCHEMY_LOG

    def run( self ):
        try:
            self.logger.error( "Initializing database" )
            engine = create_engine( 'sqlite:///:memory:', echo=True )
            Session = sessionmaker( bind=engine )
            session = Session()
            SqlBase.metadata.create_all( engine )
            self.logger.error( "Initialized database" )

            while not self.done:
                packet = self.output_queue.receive()
                self.logger.error( 'Received data packet for sqlAlchemy: packet = {}'.format( packet ) )


                value = packet[Constants.DataPacket.value]
                units = packet[Constants.DataPacket.units]
                device = packet[Constants.DataPacket.device]
                port = packet[Constants.DataPacket.port]
                arrival_time = packet[Constants.DataPacket.arrival_time]

                data = Data( value, units, device, port, arrival_time )
                session.add( data )
                session.commit()
                self.logger.error( "Successfully committed data do database" )
        except KeyboardInterrupt:
            return
        except Exception as ex:
            self.logger.exception( "Exception in sqlAlchemy thread" )
