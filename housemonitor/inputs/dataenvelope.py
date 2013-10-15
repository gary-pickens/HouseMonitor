'''
Created on Oct 10, 2012

@author: Gary
'''
from collections import defaultdict
from housemonitor.lib.constants import Constants
from housemonitor.lib.base import Base


class DataEnvelope( Base, dict ):

    '''
    This object will be used to pass data through queues between threads.

    '''
    type = ""
    ''' The type of data that is being passed. '''
    args = {}

    @property
    def logger_name( self ):
        return Constants.LogKeys.DATA_ENVELOPE


    def __init__( self, type, **kwargs ):
        ''' 
        Store the data in the envelope.
        '''
        super( DataEnvelope, self ).__init__()
        if ( type not in Constants.EnvelopeTypes.set_of_envelope_types ):
            raise KeyError( 'Invalid type error: type = {}'.format( type ) )
        self.args = kwargs
        self.type = type

    def __getitem__( self, key ):
        return self.args[key]

    def __contains__( self, key ):
        return key in self.args

    def __setitem__( self, key, value ):
        self.args[key] = value

    def __str__( self ):
        return 'type = {} args = {}'.format( self.type, self.args )

    def __repr__( self ):
        return 'DataEnvelope({},  {})'.format( self.type, self.args )

    def __len__( self ):
        return len( self.type ) + len( self.args )
