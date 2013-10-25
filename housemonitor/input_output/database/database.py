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
    long_address = Column( String( 16 ) )
    descriptive_name = Column( String( 35 ) )

    def __init__( self, long_address, descriptive_name, ports=[] ):
        '''
        Initialize the device object.
        :param long_address:
        :param descriptive_name:
        :param ports_list
        '''
        super( Device, self ).__init__()
        self.descriptive_name = descriptive_name
        self.long_address = long_address

    def __repr__( self ):
        return "<Devices({}, {}, {}, {})>".format( 
                                        self.id, self.descriptive_name,
                                        self.long_address)

class Port( Base ):
    '''
    Create the Port table and object.
    '''

    __tablename__ = "ports"

    id = Column( Integer, primary_key=True )
    port_name = Column( String(10) )
    devices_id = Column( Integer, ForeignKey( 'devices.id' ) )
    units = Column( String(5) )
    devices = relationship( "Device", backref=backref( 'ports', order_by=id ) )

    def __init__( self, port_name, units ):
        super( Port, self ).__init__()
        self.port_name = port_name
        self.units = units

    def __repr__( self ):
        return "<Ports({}, {}, {}, {}, {})>".format( self.id, self.port_name,
                                self.units, self.devices_id, self.devices )

if __name__ == '__main__':

#    engine = create_engine( 'sqlite:///:memory:', echo=True )
    engine = create_engine( 'mysql+mysqldb://root:Helena&Patrick@localhost:3306/housemonitor', echo=True )

    Session = sessionmaker( bind=engine )
    session = Session()
    Base.metadata.create_all( engine )

    devices1 = Device( 'device 1', "Common Name" )
    p1 = Port( 'port 1', 'C' )
    p2 = Port( 'port 2', 'C' )
    ps1 = [p1, p2]
    devices1.ports_list = ps1
    session.add( devices1 )
    session.add_all( devices1.ports_list )
    session.commit()

    port_list = [Port( 'port 3', 'C' ), Port( 'port 4', 'C' )]
    devices2 = Device( 'device 2', "Garage Door")
    session.add( devices2 )
    session.add_all( port_list )
    session.commit()

    devices = session.query( Device ).all()
    print( devices )
    ports = session.query( Port ).all()
    print( ports )

    p = session.query( Device ).filter( Device.long_address == 'device 1' )\
                    .filter( Port.port_name == 'port 1' ).all()
    print( 'port 1 = {}'.format( p ) )


    p = session.query( Device ).filter( Device.long_address == 'device 2' )\
                    .filter( Port.port_name == 'port 3' ).all()
    print( 'port 2 = {}'.format( p ) )

    p = session.query( Device ).filter( Device.long_address == 'device 3' )\
                    .filter( Port.port_name == 'port 3' ).all()
    print( 'port 3 = {}'.format( p ) )
