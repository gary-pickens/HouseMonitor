'''
Created on Oct 19, 2013

@author: gary
'''


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from housemonitor.lib.constants import Constants

Base = declarative_base()

class Data ( Base ):
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
