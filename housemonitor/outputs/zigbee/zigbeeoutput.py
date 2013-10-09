'''
Created on Mar 6, 2013

@author: Gary

'''
import os
import struct
from datetime import datetime, timedelta
from xbee import ZigBee
from housemonitor.lib.common import Common
from housemonitor.lib.constants import Constants
from housemonitor.lib.base import Base
from housemonitor.inputs.zigbeeinput.beagleboneblackxbeecommunications import BeagleboneBlackXbeeCommunications
from housemonitor.inputs.zigbeeinput.windowsxbeecommunications import WindowsXbeeCommunications


class UnsupportedSystemError( Exception ):
    pass


class ZigBeeOutput( Base, object ):
    '''
    ZigBeeOutput is responsible for formating a ZigBee message and sending it to a remote XBee.
    '''
    setPinHigh = b'\x05'
    setPinLow = b'\x04'
    serial = None
    zigbee = None
    previous_datetime = datetime.utcnow()
    in_test_mode = False

    deviceToCommand = {'DIO-0': b'D0',
                    'DIO-1': b'D1',
                    'DIO-2': b'D2',
                    'DIO-3': b'D3',
                    'DIO-4': b'D4',
                    'DIO-5': b'D5',
                    'DIO-6': b'D6',
                    'DIO-7': b'D7'}

    selectHighOrLow = {False: setPinLow, True: setPinHigh}
    communication_module = {'posix': BeagleboneBlackXbeeCommunications,
                            'nt': WindowsXbeeCommunications}

    def __init__( self, in_test_mode=False ):
        '''
        '''
        super( ZigBeeOutput, self ).__init__()
        self.in_test_mode = in_test_mode

    def startCorrectZigbee( self, os_name=os.name ):
        if not self.in_test_mode:
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


    def sendCommand( self, **packet ):

        try:
            device = packet[Constants.DataPacket.device]
            port = packet[Constants.DataPacket.port]
            value = packet[Constants.DataPacket.value]
            id = packet[Constants.DataPacket.ID]
            dest_addr_long = struct.pack( '!Q', int( device, 16 ) )
            command = self.deviceToCommand[port.upper()]
            frame_id = struct.pack( '!B', id )
            parameter = self.selectHighOrLow[value]
            current_datetime = datetime.utcnow()
            delta = current_datetime - self.previous_datetime
            if not self.in_test_mode:
                self.zigbee.remote_at( dest_addr_long=dest_addr_long,
                                       frame_id=frame_id,
                                       command=command,
                                       parameter=parameter )
                self.logger.debug( '{} dest_addr = {:x} command = {} parameter {:x} frame_id {}'.
                              format( str( delta ).split( '.' )[0],
                                      struct.unpack( '!Q', dest_addr_long )[0], command,
                                      struct.unpack( 'B', parameter )[0],
                                      struct.unpack( 'B', frame_id )[0] ) )
            self.previous_datetime = current_datetime
        except KeyError:
            self.logger.exception( 'KeyError exception: packet = {}'.format( packet ) )
            raise
