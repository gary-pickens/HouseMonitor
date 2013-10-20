'''
Created on Oct 16, 2013

@author: gary
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


Base = declarative_base()

class StepNames( Base ):
    '''
    classdocs
    '''

    __tablename__ = "StepNames"

    id = Column( Integer, primary_key=True )
    step_name = Column( String )

    def __init__( self, step_name ):
        '''
        :param step_name:
        '''
        self.step_name = step_name


    def __repr__( self ):
        return '<StepNames("{}")>'.format( self.step_name )
