'''
Created on Oct 16, 2013

@author: gary
'''
from sqlalchemy import Column, Base, Integer, String


class Device( Base ):
    '''
    classdocs
    '''

    __tablename__ = "Device"

    id = Column( Integer, primary_key=True )
    long_address = Column( String( 16 ) )
    name = Column( String )
    network_address = Column( String() )


    def __init__( self, long_address, name, network_address ):
        '''
        Constructor
        '''
        self.long_address = long_address
        self.name = name
        self.network_address = network_address

    def __repr__( self ):
        return "<Device({} {} {})".format( 
                        self.long_address, self.name, self.network_address )
