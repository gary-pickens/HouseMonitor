'''
Created on Oct 16, 2013

@author: gary
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class Device( Base ):
    '''
    This object contains all the information about the device.
    '''

    __tablename__ = "Devices"

    id = Column( Integer, primary_key=True )
    long_address = Column( String( 16 ) )
    descriptive_name = Column( String )
    network_address = Column( String() )

    def __init__( self, long_address, descriptive_name, network_address ):
        '''
        Construct an object that contains all the data that is held by 
        this object and table.

        :param long_address:
        :param descriptive_name:
        :param network_address:
        '''
        self.long_address = long_address
        self.descriptive_name = descriptive_name
        self.network_address = network_address

    def __repr__( self ):
        return "<Device({} {} {})>".format( 
                        self.long_address,
                        self.descriptive_name,
                        self.network_address )
