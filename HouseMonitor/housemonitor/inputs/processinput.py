'''
Created on Oct 10, 2012

@author: Gary Pickens
'''
import abc
from struct import *
import copy
import pprint
from datetime import datetime
from pubsub.core.topicmgr import ListenerSpecIncomplete

from housemonitor.configuration.xmlDeviceConfiguration import InvalidDeviceError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidPortError
from housemonitor.configuration.xmlDeviceConfiguration import InvalidConfigurationOptionError
from housemonitor.configuration.xmlDeviceConfiguration import xmlDeviceConfiguration
from housemonitor.lib.common import Common
from abc_input import abcInput
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants
from housemonitor.lib.getdatetime import GetDateTime
import housemonitor.lib.sddaemon
import thread


class abcProcessInput( Base, object ):
    __metaclass__ = abc.ABCMeta

    def __init__( self ):
        super( abcProcessInput, self ).__init__()

    @abc.abstractproperty
    def process( self, envelope ):
        pass    # pragma: no cover


class ProcessXBeeInput( abcProcessInput ):
    '''
    This class will receive an XBee packet, strip the pertinate data out, and send it allong to be processed.
    '''
    devices = {}

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputsZigBee

    def __init__( self, devices ):
        super( ProcessXBeeInput, self ).__init__()
        self.devices = devices

    def process( self, envelope ):
        '''
        Process a envelope received from the XBee.  This involves the following:
        1.  get the addresses from the header
        2.  get the data out of the packet
        3.  get information about the source of the data
        4.  send each packet using the pub/sub system

        Args:
        :param envelope: a packet received from the XBee radio and decomposed by the ZigBee module
        :type DataEnvelope:
        Return: None
        :Raises: None
        '''
        self.logger.info( 'processing data from zigbee {}'.format( envelope ) )
        try:
            packet = envelope.packet
            if packet[Constants.XBee.id] == Constants.XBee.api_responses.rx_io_data_long_addr:
                source_addr_long = "{:#x}".format( unpack( '!Q', packet[Constants.XBee.source_addr_long] )[0] )
                source_addr = "{:#x}".format( unpack( '!H', packet[Constants.XBee.source_addr] )[0] )
                if Constants.XBee.samples in packet:
                    samples = packet[Constants.XBee.samples]
                    for port in samples[0]:
                        package = {}
                        try:
                            if ( self.devices.valid_device( source_addr_long ) ):
                                package[Constants.DataPacket.device] = source_addr_long
                                package[Constants.DataPacket.name] = self.devices.get_port_name( source_addr_long, port )
                                package[Constants.DataPacket.port] = port
                                package[Constants.DataPacket.arrival_time] = datetime.utcnow()
                                package[Constants.DataPacket.units] = self.devices.get_port_units( source_addr_long, port )
                                package[Constants.DataPacket.steps] = copy.copy( self.devices.get_steps( source_addr_long, port ) )
                                data = samples[0][port]

                                Common.send( data, package, package[Constants.DataPacket.steps] )
                        except InvalidDeviceError as ie:
                                self.logger.exception( str( ie ) )
                        except InvalidPortError as ie:
                                self.logger.exception( str( ie ) )
                        except InvalidConfigurationOptionError as ie:
                                self.logger.exception( str( ie ) )
                        except Exception as ex:
                            self.logger.exception( 'Common.send error {}'.format( ex ) )
            else:
                self.logger.info( 'None processed ZigBee response {}'.format( pprint.pformat( packet ) ) )
        except KeyError:
            self.logger.exception( "error extracting data from {}".format( pprint.pformat( envelope ) ) )
        except ListenerSpecIncomplete as lsi:
            self.logger.error( 'Invalid topic: {}'.format( lsi ) )


class ProcessStatusRequests( abcProcessInput ):

    devices = {}

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputs

    def __init__( self, devices ):
        super( ProcessStatusRequests, self ).__init__()
        self.devices = devices

    def process( self, envelope ):
        '''
        Process a packet received from the XBee.  This involves the following:
        #.  get the addresses from the header
        #.  get the data out of the packet
        #.  get information about the source of the data
        #.  send each packet using the pub/sub system

        :param packet: a packet recived from the XBee radio and decomposed by the ZigBee module
        :return: None
        :Raises: None
        '''
        try:
            data = envelope.data
            if Constants.DataPacket.current_value in data:
                value = data[Constants.DataPacket.current_value]
            else:
                value = 1
            listeners = data[Constants.DataPacket.listeners]
            Common.send( value, data, listeners )
        except Exception as ex:
            self.logger.exception( 'Common.send error {}'.format( ex ) )

class ProcessInput( abcInput ):
    '''
    This class will remove the data off the input queue, determine the the
    the of data and pass the data to the correct routine to futher process the data
    '''

    _input_queue = None
    ''' The queue will be used to receive data from input threads. '''

    commands = {}
    ''' A dictionary used to direct incoming data. '''

    devices = {}
    ''' A dictionary containing information about input devices. '''

    forever = True
    ''' Controls the main loop in the input function. '''

    @property
    def topic_name( self ):
        return Constants.TopicNames.ProcessInputs

    @property
    def configuration_file_name( self ):
        return __name__

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputs

    def __init__( self, input_queue ):
        '''
        Constructor
        '''
        super( ProcessInput, self ).__init__()
        self._input_queue = input_queue
        self.devices = xmlDeviceConfiguration()

        self.commands = {Constants.EnvelopeTypes.xbee: ProcessXBeeInput( self.devices ),
                         Constants.EnvelopeTypes.status: ProcessStatusRequests( self.devices )}

    def work( self ):
        '''
        Processing for the main loop.

        #. Remove the data from the input_queue
        #. Send the data to the object for processing.

        '''
        try:
            envelope = self._input_queue.receive()
            self.logger.debug( 'recieved type {} Envelope'.format( envelope.type ) )
            self.commands[envelope.type].process( envelope )
        except KeyError:
            self.logger.debug( 'Invalid envelope.type = {}'.format( envelope.type ) )

    def input( self ):
        '''
        The input routine will receive data from the xbee thead via the queue.
        Do some preliminary processing and publish the data via the pub/sub
        package.

        '''

        while self.forever:
            housemonitor.lib.sddaemon.sd_notify( 0, 'WATCHDOG=1' )
            self.work()
