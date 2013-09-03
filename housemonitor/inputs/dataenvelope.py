'''
Created on Oct 10, 2012

@author: Gary
'''
from housemonitor.lib.getdatetime import GetDateTime
from collections import defaultdict
from housemonitor.lib.constants import Constants


class DataEnvelope( dict ):

    '''
    This object will be used to pass data through queues between threads.

    '''
    type = Constants.EnvelopeTypes.XBEE
    ''' The type of data that is being passed. '''
    args = None

    def __init__( self, type=Constants.EnvelopeTypes.XBEE, **kwargs ):
        ''' Store the data in the envelope.

        '''
        super( DataEnvelope, self ).__init__()
        if ( type not in Constants.EnvelopeTypes.set_of_envelope_types ):
            raise KeyError( 'Invalid type error: type = {}'.format( type ) )
        self.args = kwargs
        self.type = type

    def __getitem__( self, key ):
        return self.args[key]

    def __setitem__( self, key, value ):
        self.args[key] = value

    def str( self ):
        'type = {} args = {}'.format( self.type, self.args )

    def repr( self ):
        'DataEnvelope({},  {})'.format( self.type, self.args )
