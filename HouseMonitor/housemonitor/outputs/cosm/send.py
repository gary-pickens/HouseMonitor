'''
Created on Sep 23, 2012

@author: Gary

'''
from configuration.cosmconfiguration import CosmConfiguration
from datetime import datetime
from httplib2 import HttpLib2Error
from lib.common import Common
from lib.constants import Constants
from lib.getdatetime import GetDateTime
from pprint import pprint
import httplib2
import json
import copy


class COSMSend( CosmConfiguration ):
    '''
    This class will send data to COSM web site.
    '''

    config = None
    ''' Configuration data read from configuration file. '''

    datastreams = list()
    ''' A dictionary of data items to send to COSM. '''

    datapoints = { }
    ''' A dictionary of lists containing data points for each channel on COSM.  
    It contains the time and value.'''

    json = None

    options = None
    ''' options passed in from command line. '''

    def __init__( self, options ):
        '''
        Initialize COSMSend for sending data to the COSM web site.
        '''
        super( COSMSend, self ).__init__()
        self.options = options

    @property
    def config_topic_name( self ):
        ''' Configuration Topic name for pub/sub '''
        return __name__

    @property
    def configuration_file_name( self ):
        ''' Name of the configuration file'''
        return __name__

    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.outputsCOSM

    def output( self, data={}, http=None ):
        """
        Output the results to COSMSend.com
        
        If the data dictionary contain 'action' and it is set to 'send' this routine will 
        send data to COSM.
        
        if the key is not set to send the this routine will store the data as a data point and 
        transmit with an other packet going to COSM.


        :param value: the current value
        :type value:
        :param data: additional data about the value
        :type dict:
        :returns: None
        :raises: None

        """
        try:
            device, port = Common.getDeviceAndPort( data )
            self.createDataStream( device, port, data )
            if Constants.DataPacket.action in data and \
                    data[Constants.DataPacket.action] == Constants.DataPacket.send:
                self.json = self.createJSONReport( device, port, data )
                self.report_data( self.json, data, http=http )
                self.empty_datastream_list()
        except Exception as ex:
            self.logger.exception( "exception in send.output {}".format( ex ) )

    def report_data( self, json, data, http=None ):
        """
        reportData - Sends the json object to the COSMSend web site

        if the options.in_test_mode is NOT set then don't send data to COSM web site.
        The options.in_test_mode is set with the command line argument --test

        the httplib2 debuglevel is set with the command line argument --http N
        where N is a positive integer.

        :param json: the current value
        :type json:
        :param data: the data that is pasted between steps
        :type dict:
        :returns: None
        :raises: None
        """
        device, port = Common.getDeviceAndPort( data )
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'X-PachubeApiKey': self.config[device][port][Constants.Cosm.apikey]}
        try:
            url = self.config[device][port][Constants.Cosm.url].\
                        format( self.config[device][port][Constants.Cosm.id] )
            if ( http == None ):
                http = httplib2.Http()
            httplib2.debuglevel = self.options.http2lib_debug_level
            self.logger.debug( "send packet {}".format( json ) )
            # if the test flag --test or -t is set at startup
            if ( not self.options.in_test_mode ):
                response, content = http.request( url, method="PUT", body=json, headers=headers )
                if ( response.status == 200 ):
                    self.logger.info( 'Successfully sent data to COSM' )
                else:
                    self.logger.error( 'Error sending data to {} status = {} response = {} content = '.format( url, response.status, response, content ) )

        except HttpLib2Error as error:
            self.logger.error( "exception from httplib2 {}".format( error ) )
        except AttributeError as error:
            self.logger.exception( "exception from httplib2 {}".format( error ) )

    def createDataStream( self, device, port, data ):
        """
        Create a data item, fill it with data, and append it to the list
        datastream.

        :param device: the device
        :param type: string
        :param port the port
        :param type: string
        :param data: the data that is pasted between steps
        :type dict:
        :returns: None
        :raises: KeyError
        """


        if device not in self.config:
            msg = 'Device is not in cosm configuration file: {}'.format( device )
            raise KeyError( msg )
        if port not in self.config[device]:
            msg = 'Port is not in cosm configuration file: {}'.format( port )
            raise KeyError( msg )
        if Constants.DataPacket.arrival_time not in data:
            msg = '{} is not in data'.format( Constants.DataPacket.arrival_time )
            raise KeyError( msg )
        if Constants.DataPacket.current_value not in data:
            msg = '{} is not in data'.format( Constants.DataPacket.current_value )
            raise KeyError( msg )

        if Constants.Cosm.datastream.cosm_channel in self.config[device][port]:
            channel = self.config[device][port][Constants.Cosm.datastream.cosm_channel]

        if Constants.DataPacket.action in data and \
            data[Constants.DataPacket.action] == Constants.DataPacket.accumulate:

            if Constants.DataPacket.arrival_time in data:
                arrival_datetime = data[Constants.DataPacket.arrival_time]
                at = arrival_datetime.isoformat()
            if Constants.DataPacket.current_value in data:
                value = data[Constants.DataPacket.current_value]
            datapoint = {"at":at, "value": value}
            if channel in self.datapoints:
                self.datapoints[channel].append( datapoint )
            else:
                self.datapoints.setdefault( channel, [ datapoint ] )
        else:
            item = {}
            if Constants.DataPacket.arrival_time in data:
                arrival_datetime = data[Constants.DataPacket.arrival_time]
                item[Constants.DataPacket.arrival_time] = arrival_datetime.isoformat()
            if Constants.DataPacket.current_value in data:
                item[Constants.DataPacket.current_value] = data[Constants.DataPacket.current_value]
            if Constants.DataPacket.units in data:
                units = {"label": data[Constants.DataPacket.units]}
                item[Constants.DataPacket.units] = units

            if Constants.Cosm.datastream.tags in self.config[device][port]:
                item[Constants.Cosm.datastream.tags] = self.config[device][port][Constants.Cosm.datastream.tags]
            if Constants.Cosm.datastream.cosm_channel in self.config[device][port]:
                item[Constants.Cosm.datastream.id] = self.config[device][port][Constants.Cosm.datastream.cosm_channel]
            if Constants.Cosm.datastream.max_value in self.config[device][port]:
                item[Constants.Cosm.datastream.max_value] = self.config[device][port][Constants.Cosm.datastream.max_value]
            if Constants.Cosm.datastream.min_value in self.config[device][port]:
                item[Constants.Cosm.datastream.min_value] = self.config[device][port][Constants.Cosm.datastream.min_value]

            if channel in self.datapoints:
                item[Constants.Cosm.datastream.datapoints] = copy.copy( self.datapoints[channel] )
                self.datapoints[channel] = []
            self.datastreams.append( item )

    def createLocation( self, device, port ):
        '''
        Create a location field that will be sent it the json object sent to COSM. The following data
        will be taken from the configuration file.

        :param device: the device name
        :type device: str
        :param port: the port name
        :type port: str
        :returns: None
        :raises: KeyError

        exposure

        disposition

        lat
            latitude of the object being reported.

        long
            longitude of the object being reported

        private


        '''
        if device not in self.config:
            msg = 'Device is not in cosm configuration file: {}'.format( device )
            raise KeyError( msg )
        if port not in self.config[device]:
            msg = 'Port is not in cosm configuration file: {}'.format( port )
            raise KeyError( msg )

        location = {}
        if Constants.Cosm.location.exposure in self.config[device][port]:
            location[Constants.Cosm.location.exposure] = self.config[device][port][Constants.Cosm.location.exposure]
        if ( Constants.Cosm.location.domain in self.config[device][port] ):
            location[Constants.Cosm.location.domain] = self.config[device][port][Constants.Cosm.location.domain]
        if ( Constants.Cosm.location.disposition in self.config[device][port] ):
            location[Constants.Cosm.location.disposition] = self.config[device][port][Constants.Cosm.location.disposition]
        if ( Constants.Cosm.location.latitude in self.config[device][port] ):
            location[Constants.Cosm.location.latitude] = self.config[device][port][Constants.Cosm.location.latitude]
        if ( Constants.Cosm.location.longitude in self.config[device][port] ):
            location[Constants.Cosm.location.longitude] = self.config[device][port][Constants.Cosm.location.longitude]
        if ( Constants.Cosm.location.private in self.config[device][port] ):
            location[Constants.Cosm.location.private] = self.config[device][port][Constants.Cosm.location.private]
        return location

    def createFeed( self, data, device, port ):
        '''
        Build the data object that will be sent to COSM.

        :param data: data that travels with the object
        :param data: dict
        :param device: the device name
        :type device: str
        :param port: the port name
        :type port: str
        :returns: dictionary
        :raises: KeyError


        '''
        if device not in self.config:
            msg = 'Device is not in cosm configuration file: {}'.format( device )
            raise KeyError( msg )
        if port not in self.config[device]:
            msg = 'Port is not in cosm configuration file: {}'.format( port )
            raise KeyError( msg )

        feed = {}
        if Constants.Cosm.title in self.config[device][port]:
            feed[Constants.Cosm.title] = self.config[device][port][Constants.Cosm.title]
        if Constants.Cosm.status in self.config[device][port]:
            feed[Constants.Cosm.status] = self.config[device][port][Constants.Cosm.status]
        if Constants.Cosm.creator in self.config[device][port]:
            feed[Constants.Cosm.creator] = self.config[device][port][Constants.Cosm.creator].format( self.config[device][port][Constants.Cosm.id] )
        if Constants.Cosm.created in self.config[device][port]:
            feed[Constants.Cosm.created] = self.config[device][port][Constants.Cosm.created]
        if Constants.Cosm.feed in self.config[device][port]:
            feed[Constants.Cosm.feed] = self.config[device][port][Constants.Cosm.url].format( self.config[device][port][Constants.Cosm.id] )
        if Constants.Cosm.email in self.config[device][port]:
            feed[Constants.Cosm.email] = self.config[device][port][Constants.Cosm.email]
        if Constants.Cosm.id in self.config[device][port]:
            feed[Constants.Cosm.id] = self.config[device][port][Constants.Cosm.id]
        feed[Constants.Cosm.updated] = datetime.utcnow().isoformat()
        if Constants.Cosm.auto_feed_url in self.config[device][port]:
            feed[Constants.Cosm.auto_feed_url] = self.config[device][port][Constants.Cosm.url].format( self.config[device][port][Constants.Cosm.id] ),
        if Constants.Cosm.version in self.config[device][port]:
            feed[Constants.Cosm.version] = self.config[device][port][Constants.Cosm.version]

        feed[Constants.Cosm.datastreams] = self.datastreams
        feed[Constants.Cosm.location_str] = self.createLocation( device, port )
        return feed

    def createJSONReport( self, device, port, data ):
        """
        Create a JSON report.

        :param device: the device
        :param type: string
        :param port the port
        :param type: string
        :param data: data that travels with the object
        :param data: dict
        :returns: json object
        :raises: KeyError

        """
        feed = self.createFeed( data, device, port )
        self.logger.debug( 'JSON feed = \n{}'.format( json.dumps( feed, indent=4 ) ) )
        return( json.dumps( feed ) )

    def empty_datastream_list( self ):
        """
        Clear the datastrem list

        """
        self.datastreams = list()
