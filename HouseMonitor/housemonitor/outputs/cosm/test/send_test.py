'''
Created on Dec 10, 2012

@author: Gary
'''
from configuration.cosmconfiguration import CosmConfiguration
from httplib2 import HttpLib2Error
from lib.common import Common
from lib.getdatetime import GetDateTime
from lib.constants import Constants
from lib.hmqueue import HMQueue
from mock import Mock, MagicMock, patch
from outputs.cosm.control import COSMControl
from outputs.cosm.outputStep import COSMOutputStep
from outputs.cosm.outputthread import COSMOutputThread
from outputs.cosm.send import COSMSend
import datetime
import httplib2
import json
import logging.config
import pprint
import unittest


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    config_data = \
    {'device 1': {'port 1': {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: 'disposition',
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 'lat',
                                Constants.Cosm.location.longitude: 'lon',
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: 'auto_feed_url',
                                Constants.Cosm.creator: 'creator',
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: 'email',
                                Constants.Cosm.feed: 'feed',
                                Constants.Cosm.id: 'id',
                                Constants.Cosm.private: 'private',
                                Constants.Cosm.status: 'status',
                                Constants.Cosm.tags: 'tags',
                                Constants.Cosm.title: 'title',
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: 'version',
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                  },
     'device 2': {'port 1': {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '2',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: 'disposition',
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 'lat',
                                Constants.Cosm.location.longitude: 'lon',
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: 'auto_feed_url',
                                Constants.Cosm.creator: 'creator',
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: 'email',
                                Constants.Cosm.feed: 'feed',
                                Constants.Cosm.id: 'id',
                                Constants.Cosm.private: 'private',
                                Constants.Cosm.status: 'status',
                                Constants.Cosm.tags: 'tags',
                                Constants.Cosm.title: 'title',
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: 'version',
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                  }
     }

    config_data_1 = \
    {'device': {'port': {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: 'disposition',
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 'lat',
                                Constants.Cosm.location.longitude: 'lon',
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: 'auto_feed_url',
                                Constants.Cosm.creator: 'creator',
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: 'email',
                                Constants.Cosm.feed: 'feed',
                                Constants.Cosm.id: 'id',
                                Constants.Cosm.private: 'private',
                                Constants.Cosm.status: 'status',
                                Constants.Cosm.tags: 'tags',
                                Constants.Cosm.title: 'title',
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: 'version',
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }}}

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 1'
        current_value = 10
        data = {'device': device,
                'port': port,
                Constants.DataPacket.units: 'X',
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: current_value}
        cs.createDataStream( device, port, data )
        item = cs.datastreams.pop()
        self.assertEqual( item[Constants.Cosm.datastream.min_value], 0 )
        self.assertEqual( item[Constants.Cosm.datastream.max_value], 100 )
        self.assertEqual( item[Constants.Cosm.datastream.tags], 'tags' )
        self.assertEqual( item[Constants.DataPacket.current_value], current_value )
        self.assertEqual( item['id'], '1' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream_with_two_datapoints( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 1'
        current_value = 10
        data = {'device': device,
                'port': port,
                Constants.DataPacket.units: 'X',
                Constants.DataPacket.action: Constants.DataPacket.accumulate,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: current_value}
        cs.createDataStream( device, port, data )
#        self.assertListEqual( cs.datapoints['1'], [{'at':'2012-01-02T03:04:05', 'value': 10}] )
        cs.createDataStream( device, port, data )
#        self.assertListEqual( cs.datapoints['1'], [{'at':'2012-01-02T03:04:05', 'value': 10}, {'at':'2012-01-02T03:04:05', 'value': 10}] )

        data = {'device': device,
                'port': port,
                Constants.DataPacket.units: 'X',
                Constants.DataPacket.action: Constants.DataPacket.accumulate,
                Constants.DataPacket.action: Constants.DataPacket.send,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 6 ),
                Constants.DataPacket.current_value: 11}

        cs.createDataStream( device, port, data )
        self.assertListEqual( cs.datapoints['1'], [] )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream_with_bad_device( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 3'
        port = 'port 1'
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: '12:12:12 12/12/11',
                Constants.DataPacket.current_value: 10}
        with self.assertRaisesRegexp( KeyError, 'Device is not in cosm configuration file: device 3' ):
            cs.createDataStream( device, port, data )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream_with_bad_port( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 2'
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: '12:12:12 12/12/12',
                Constants.DataPacket.current_value: 10}
        with self.assertRaisesRegexp( KeyError, 'Port is not in cosm configuration file: port 2' ):
            cs.createDataStream( device, port, data )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream_with_bad_no_arrival_time( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 1'
        data = {'device': device,
                'port': port,
#                Constants.DataPacket.arrival_time: '12:12:12 12/12/13',
                Constants.DataPacket.current_value: 10}
        with self.assertRaisesRegexp( KeyError, 'at is not in data' ):
            cs.createDataStream( device, port, data )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createDataStream_with_bad_no_current_value( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        device = 'device 1'
        port = 'port 1'
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: '12:12:12 12/12/14',
#                Constants.DataPacket.current_value: 10
        }
        with self.assertRaisesRegexp( KeyError, 'current_value is not in data' ):
            cs.createDataStream( device, port, data )

####################################################################################
# Test Location
####################################################################################

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createLocation( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = self.config_data
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: '12:12:12 12/12/15',
                Constants.DataPacket.current_value: 10}
        location = cs.createLocation( device, port )
        self.assertEqual( location[Constants.Cosm.location.exposure], Constants.Cosm.location.exposure )
        self.assertEqual( location[Constants.Cosm.location.domain], Constants.Cosm.location.domain )
        self.assertEqual( location[Constants.Cosm.location.disposition], Constants.Cosm.location.disposition )
        self.assertEqual( location[Constants.Cosm.location.latitude], Constants.Cosm.location.latitude )
        self.assertEqual( location[Constants.Cosm.location.longitude], Constants.Cosm.location.longitude )
        self.assertEqual( location[Constants.Cosm.location.private], Constants.Cosm.location.private )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createLocation_with_bad_device( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        with self.assertRaisesRegexp( KeyError, 'Device is not in cosm configuration file: device 3' ):
            cs.createLocation( 'device 3', 'port 1' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createLocation_with_bad_port( self, config ):
        options = None
        cs = COSMSend( options )
        config.assert_called_once_with()
        cs.config = self.config_data
        with self.assertRaisesRegexp( KeyError, 'Port is not in cosm configuration file: port 2' ):
            cs.createLocation( 'device 1', 'port 2' )

##########################################################
# test empty_datastreas
##########################################################

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_empty_datastream_list( self, config ):
        options = None
        cs = COSMSend( options )
        cs.empty_datastream_list()
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = self.config_data
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        self.assertEqual( len( cs.datastreams ), 0 )
        cs.createDataStream( device, port, data )
        cs.createDataStream( device, port, data )
        cs.empty_datastream_list()

##########################################################
# test feed
##########################################################
    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createFeed( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = self.config_data
        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs.createDataStream( device, port, data )
        feed = cs.createFeed( data, device, port )
        pprint.pprint( feed )
        self.assertEqual( feed[Constants.Cosm.title], Constants.Cosm.title )
        self.assertEqual( feed[Constants.Cosm.status], Constants.Cosm.status )
        self.assertEqual( feed[Constants.Cosm.creator], Constants.Cosm.creator )
        self.assertEqual( feed[Constants.Cosm.created], Constants.Cosm.created )
        self.assertEqual( feed[Constants.Cosm.feed], 'url' )
        self.assertEqual( feed[Constants.Cosm.email], Constants.Cosm.email )
        self.assertEqual( feed[Constants.Cosm.id], Constants.Cosm.id )
        self.assertEqual( feed[Constants.Cosm.auto_feed_url], ( 'url', ) )
        self.assertEqual( feed[Constants.Cosm.version], Constants.Cosm.version )
        cs.empty_datastream_list()
        cs = None

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createFeed_with_no_device_in_config_file( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = self.config_data_1
        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        with self.assertRaisesRegexp( KeyError, 'Device is not in cosm configuration file:.*' ):
            feed = cs.createFeed( data, device, port )
        cs = None

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createFeed_with_no_port_in_config_file( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port'
        config.assert_called_once_with()
        cs.config = self.config_data
        data = {
                Constants.DataPacket.device: device,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        with self.assertRaisesRegexp( KeyError, 'Port is not in cosm configuration file:.*' ):
            feed = cs.createFeed( data, device, port )
        cs = None

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createFeed_with_two_datestreams( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = self.config_data
        data = {'device': device,
                'port': port,
                Constants.DataPacket.action: Constants.DataPacket.accumulate,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs.createDataStream( device, port, data )

        data[Constants.DataPacket.current_value] = 545454
        cs.createDataStream( device, port, data )

        data['device'] = device = 'device 2'
        data[Constants.DataPacket.current_value] = 999
        cs.createDataStream( device, port, data )

        data['device'] = device = 'device 1'
        data[Constants.DataPacket.action] = Constants.DataPacket.send
        cs.report_data = MagicMock()
        cs.output( data )
        pprint.pprint( cs.json )
        pprint.pprint( cs.datapoints )
#         self.assertEqual( cs.[Constants.Cosm.title], Constants.Cosm.title )
#         self.assertEqual( cs.json[Constants.Cosm.status], Constants.Cosm.status )
#         self.assertEqual( cs.json[Constants.Cosm.creator], Constants.Cosm.creator )
#         self.assertEqual( cs.json[Constants.Cosm.created], Constants.Cosm.created )
#         self.assertEqual( cs.json[Constants.Cosm.feed], 'url' )
#         self.assertEqual( cs.json[Constants.Cosm.email], Constants.Cosm.email )
#         self.assertEqual( cs.json[Constants.Cosm.id], Constants.Cosm.id )
#         self.assertEqual( cs.json[Constants.Cosm.auto_feed_url], ( 'url', ) )
#         self.assertEqual( cs.json[Constants.Cosm.version], Constants.Cosm.version )
        cs = None

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_createJSONReport( self, config ):
        options = None
        cs = COSMSend( options )
        device = 'device 1'
        port = 'port 1'
        config.assert_called_once_with()
        cs.config = config_data = \
                {'device 1': \
                    {'port 1': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }

        data = {'device': device,
                'port': port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs.createDataStream( device, port, data )

        data[Constants.DataPacket.current_value] = 545454
        cs.createDataStream( device, port, data )

        json = cs.createJSONReport( device, port, data )

        pprint.pprint( json )
        cs.empty_datastream_list()
        cs = None

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data( self, config ):
        device = 'device'
        port = 'port'
        options = MagicMock( in_test_mode=False )
        response = Mock( status=200 )
        attrs = {'request.return_value': ( response, 3 )}
        http = Mock( **attrs )

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        json = 'test'
        cs.report_data( json, data, http )
        print http.request.call_args
        http.request.assert_called_once_with( 'url', body='test', headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-PachubeApiKey': 'apikey'}, method='PUT' )

    @patch( 'outputs.cosm.send.httplib2.Http' )
    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data_passing_in_http( self, config, http ):
        device = 'device'
        port = 'port'
        options = MagicMock( in_test_mode=False )

        http = Mock()
        response = Mock()
        attrs = {'request.return_value': ( response, 3 )}
        http.configure_mock( **attrs )

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        json = 'test'
        cs.report_data( json, data, http )
        print http.request.call_args
        http.request.assert_called_once_with( 'url', body='test', headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-PachubeApiKey': 'apikey'}, method='PUT' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data_with_300_status( self, config ):
        device = 'device'
        port = 'port'
        options = MagicMock( in_test_mode=False )
        response = Mock( status=300 )
        attrs = {'request.return_value': ( response, 3 )}
        http = Mock( **attrs )

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        json = 'test'
        cs.report_data( json, data, http )
        print http.request.call_args
        http.request.assert_called_once_with( 'url', body='test', headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-PachubeApiKey': 'apikey'}, method='PUT' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data_in_test_mode( self, config ):
        device = 'device'
        port = 'port'
        options = MagicMock()
        options.in_test_mode = MagicMock()

        http = Mock()

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        cs.report_data( json, data, http )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data_with_HttpLib2Error( self, config ):
        device = 'device'
        port = 'port'
        options = MagicMock( in_test_mode=False )
        response = Mock( status=200 )

        attr = {'request.side_effect': HttpLib2Error}
        http = Mock( **attr )

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        json = 'test'
        cs.report_data( json, data, http )
        print http.request.call_args
        http.request.assert_called_once_with( 'url', body='test', headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-PachubeApiKey': 'apikey'}, method='PUT' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_report_data_with_AttribueError( self, config ):
        device = 'device'
        port = 'port'
        options = MagicMock( in_test_mode=False )
        response = Mock( status=200 )

        attr = {'request.side_effect': AttributeError}
        http = Mock( **attr )

        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port,
                Constants.DataPacket.arrival_time: datetime.datetime( 2012, 1, 2, 3, 4, 5 ),
                Constants.DataPacket.current_value: 10}
        cs = COSMSend( options )
        cs.config = config_data = \
                {'device': \
                    {'port': \
                        {
                                Constants.Cosm.datastream.tags: 'tag',
                                Constants.Cosm.datastream.cosm_channel: '1',
                                Constants.Cosm.datastream.max_value: 100,
                                Constants.Cosm.datastream.min_value: 0,
                                Constants.Cosm.location.created: 'created',
                                Constants.Cosm.location.disposition: "fixed",
                                Constants.Cosm.location.domain: 'domain',
                                Constants.Cosm.location.exposure: 'exposure',
                                Constants.Cosm.location.latitude: 30.3351807498968,
                                Constants.Cosm.location.longitude: 97.7104604244232 * -1.0,    # Eclipse save causes error
                                Constants.Cosm.location.private: 'private',
                                Constants.Cosm.apikey: 'apikey',
                                Constants.Cosm.auto_feed_url: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.creator: "https://cosm.com/users/gary_pickens",
                                Constants.Cosm.created: 'created',
                                Constants.Cosm.email: "gary_pickens@yahoo.com",
                                Constants.Cosm.feed: "https://api.cosm.com/v2/feeds/64451.json",
                                Constants.Cosm.id: 64451,
                                Constants.Cosm.private: "false",
                                Constants.Cosm.status: "frozen",
                                Constants.Cosm.tags: ["Door", "Temperature"],
                                Constants.Cosm.title: "Garage",
                                Constants.Cosm.updated: 'updated',
                                Constants.Cosm.url: 'url',
                                Constants.Cosm.version: "1.0.0",
                                Constants.Cosm.location_str: 'location',
                                Constants.Cosm.datastreams: 'datastreams',
                            }
                        }
                    }
        json = 'test'
        cs.report_data( json, data, http )
        print http.request.call_args
        http.request.assert_called_once_with( 'url', body='test', headers={'Content-Type': 'application/x-www-form-urlencoded', 'X-PachubeApiKey': 'apikey'}, method='PUT' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_config_topic_name( self, c ):
        options = MagicMock( in_test_mode=False )
        cs = COSMSend( options )
        self.assertEqual( cs.config_topic_name, 'outputs.cosm.send' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_config_file_name( self, c ):
        options = MagicMock( in_test_mode=False )
        cs = COSMSend( options )
        self.assertEqual( cs.configuration_file_name, 'outputs.cosm.send' )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_output( self, c ):
        options = MagicMock( in_test_mode=False )
        device = 'device'
        port = 'port'
        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port}
        cs = COSMSend( options )
        cs.createDataStream = Mock()
        cs.createJSONReport = Mock()
        cs.report_data = Mock()
        cs.output( data )
        cs.createDataStream.called_once_with( device, port, data )
        cs.createJSONReport.called_once_with( device, port, data )
        cs.report_data.called_once_with( device, port, data )

    @patch( 'outputs.cosm.send.CosmConfiguration.configure' )
    def test_output_with_exception( self, c ):
        options = MagicMock( in_test_mode=False )
        device = 'device'
        port = 'port'
        data = {Constants.DataPacket.device: device,
                Constants.DataPacket.port: port}
        cs = COSMSend( options )
        cs.createDataStream = Mock()
        cs.createJSONReport = Mock()
        cs.report_data = Mock( side_effect=Exception( 'Test' ) )
        cs.output( data )
        cs.createDataStream.called_once_with( device, port, data )
        cs.createJSONReport.called_once_with( device, port, data )
        cs.report_data.called_once_with( device, port, data )

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
