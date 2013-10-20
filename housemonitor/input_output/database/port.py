'''
Created on Oct 16, 2013

@author: gary
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


Base = declarative_base()

class Port( Base ):
    '''
    classdocs
    '''

    __tablename__ = "Ports"

    id = Column( Integer, primary_key=True )
    port_name = Column( String( 16 ) )
    descriptive_name = Column( String )
    units = Column( String )
    steps = Column( Integer, ForeignKey( 'steps.id' ) )

    device = relationship( "Device", backref=backref( 'Ports', order_by=id ) )

    def __init__( self, port_name, descriptive_name, units, steps ):
        '''
        Construct an object that contains all the data that is held by 
        this object and table.
        :param port_name:
        :param descriptive_name:
        :param units:
        :param steps:
        '''
        self.port_name = port_name
        self.descriptive_name = descriptive_name
        self.units = units
        self.steps = steps


    def __repr__( self ):
        return "<Device({} {} {})>".format( 
                        self.long_address,
                        self.descriptive_name,
                        self.network_address )
