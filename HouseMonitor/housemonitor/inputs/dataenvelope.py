'''
Created on Oct 10, 2012

@author: Gary
'''
from housemonitor.lib.getdatetime import GetDateTime


class DataEnvelope( object ):

    '''
    This object will be used to pass data through queues between threads.

    '''
    type = 'xbee'
    ''' THe type of data that is being passed. '''
    packet = None
    ''' The data. '''
    arrival_time = GetDateTime()
    ''' The arrival time of the data.'''
    data = None
    ''' Additional data such as it source. '''

    def __init__( self, type='xbee', packet={}, arrival_time=GetDateTime(), data={} ):
        ''' Store the data in the envelope.

        :param type: the type of data that this packet contain.
        :type type: string
        :param packet: the data
        :type packet:  dict
        :param arrival_time: The time that the packet was received by the computer system
        :type arrival_time: datatime
        :param data: Additional information about the packet. (device, port, units, etc)
        :type data: dict

        '''
        self.type = type
        self.packet = packet
        self.arrival_time = arrival_time
        self.data = data

#     def str( self ):
#         return "type = '{}', packet = {}, arrival_time = '{}', data = {})".format(
#                             self.type,
#                             self.packet,
#                             self.arrival_time,
#                             self.data )
#
#     def __repr__( self ):
#         return "DataEnvelope(type = '{}', packet = {}, arrival_time = '{}', data = {})".format(
#                             self.type.__repr__(),
#                             self.packet.__repr__(),
#                             self.arrival_time.__repr__(),
#                             self.data.__repr__() )
