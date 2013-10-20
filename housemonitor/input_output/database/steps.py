'''
Created on Oct 16, 2013

@author: gary
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


Base = declarative_base()

class Steps( Base ):
    '''
    classdocs
    '''

    __tablename__ = "Steps"

    id = Column( Integer, primary_key=True )
    descriptive_name = Column( Integer, ForeignKey( 'port.steps' ) )

    ports = relationship( "Ports", backref=backref( 'Ports', order_by=id ) )
    order = Column( Integer )

    def __init__( self, descriptive_name, order ):
        '''
        A table that contains the steps that data must pass 
        thuugh.
        :param descriptive_name:
        :param order:
        '''
        self.descriptive_name = descriptive_name
        self.order = order


    def __repr__( self ):
        return "<Device({} {})>".format( self.descriptive_name, self.order )
