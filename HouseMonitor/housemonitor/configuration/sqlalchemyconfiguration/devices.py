'''
Created on Apr 14, 2013

@author: Gary
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Device( Base ):
    __tablename__ = 'device'

    id = Column( Integer, primary_key=True )
    device = Column( String )
    port_id = Column( Integer, )
    name = Column( String )

    def __init__( self, device, port_id, name ):
        self.device = device
        self.port_id = port_id
        self.name = name

    def __repr__( self ):
        return "<User('%s','%s', '%s')>" % ( self.device, self.port_id, self.name )
