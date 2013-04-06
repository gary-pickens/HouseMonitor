'''
Created on Mar 6, 2013

@author: Gary

'''
import os
import struct
from datetime import datetime, timedelta
from xbee import ZigBee
from lib.common import Common
from lib.constants import Constants
from lib.base import Base
from inputs.zigbeeinput.beaglebonexbeecommunications import BeagleboneXbeeCommunications
from inputs.zigbeeinput.windowsxbeecommunications import WindowsXbeeCommunications


class UnsupportedSystemError( Exception ):
    pass


class ZigBeeOutput( Base, object ):
    '''

    '''
    setPinHigh = b'\x05'
    setPinLow = b'\x04'
    serial = None
    zigbee = None
    previous_datetime = datetime.utcnow()

    deviceToCommand = {'DIO-0': b'D0',
                    'DIO-1': b'D1',
                    'DIO-2': b'D2',
                    'DIO-3': b'D3',
                    'DIO-4': b'D4',
                    'DIO-5': b'D5',
                    'DIO-6': b'D6',
                    'DIO-7': b'D7'}

    selectHighOrLow = {False: setPinLow, True: setPinHigh}
    communication_module = {'posix': BeagleboneXbeeCommunications,
                            'nt': WindowsXbeeCommunications}

    def __init__( self ):
        '''
        '''
        super( ZigBeeOutput, self ).__init__()

    def startCorrectZigbee( self, os_name=os.name ):
        if ( os_name in self.communication_module ):
            self.comm = self.communication_module[os_name]()
            self.serial = self.comm.setup()
            self.zigbee = ZigBee( self.serial )
        else:
            raise UnsupportedSystemError( "System {} not supported".format( os_name ) )

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsZigBee


    def sendCommand( self, value, data ):

        try:
            device, port = Common.getDeviceAndPort( data )
            dest_addr_long = struct.pack( '!Q', int( device, 16 ) )
            command = self.deviceToCommand[port.upper()]
            parameter = self.selectHighOrLow[value]
            current_datetime = datetime.utcnow()
            delta = current_datetime - self.previous_datetime
            self.logger.info( '{} dest_addr = {:x} command = {} parameter {:x}'.format( str( delta ).split( '.' )[0], struct.unpack( '!Q', dest_addr_long )[0], command, struct.unpack( 'B', parameter )[0] ) )
            self.zigbee.remote_at( dest_addr_long=dest_addr_long, frame_id=b'\xaa', command=command, parameter=parameter )
            self.previous_datetime = current_datetime
        except KeyError:
            self.logger.exception( 'KeyError exception: value = {} data = {}'.format( value, data ) )
