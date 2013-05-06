'''
Created on Dec 17, 2012

@author: Gary
'''
import unittest
import logging.config
from mock import Mock, MagicMock, patch
from configuration.cosmconfiguration import CosmConfiguration
from configuration.xmlconfiguration import XmlConfiguration
import xml.etree.ElementTree as ET


class Test( unittest.TestCase ):
    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    @patch( 'configuration.xmlconfiguration.XmlConfiguration.configure' )
    def test_read_configuration_data( self, configure ):
        cosm = CosmConfiguration()
        root = ET.fromstring( xml )
        config = cosm.process_configuration( root )
        self.assertIn( '0x13a200409029bf', config )
        self.assertIn( 'adc-1', config['0x13a200409029bf'] )
        self.assertIn( '0x13a200409029bf', config )
        self.assertIn( "dio-0", config['0x13a200409029bf'] )
        self.assertIn( 'tags', config['0x13a200409029bf']['adc-1'] )

    @patch( 'configuration.xmlconfiguration.XmlConfiguration.configure' )
    def test_getitem( self, configure ):
        cosm = CosmConfiguration()
        cosm.config = {'a': 'b'}
        self.assertEqual( cosm['a'], 'b' )
        cosm['c'] = 'd'
        self.assertEqual( cosm['c'], 'd' )



#    TODO work on this test
#    @patch('configuration.xmlconfiguration.XmlConfiguration.configure')
#    def test_read_config_dict(self, configure):
#        cosm = CosmConfiguration()
#        root = ET.fromstring(xml)
#        cosm.config = cosm.process_configuration(root)
#
#        self.assertIn('0x13a200409029bf', cosm)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover


xml = \
'''<?xml version="1.0" encoding="UTF-8"?>
<cosm>
    <item device="0x13a200409029bf" port="adc-1">
        <apikey>WhOKtmp8qTU_5-C8bl6JCrEQ_EeSAKxJV0lHNkkybzlsaz0g</apikey>
        <id>64451</id>
        <url>https://api.cosm.com/v2/feeds/{}.json</url>
        <title>Garage</title>
        <exposure>indoor</exposure>
        <domain>physical</domain>
        <disposition>fixed</disposition>
        <status>frozen</status>
        <private>false</private>
        <tags>Temperature</tags>
        <cosm_channel>1</cosm_channel>
        <creator>https://cosm.com/users/{}</creator>
        <latitude>30.3351807498968</latitude>
        <longitude>-97.7104604244232</longitude>
        <email>gary_pickens@yahoo.com</email>
        <max_value>120</max_value>
        <min_value>0</min_value>
        <unit>
          <label>F</label>
        </unit>
        <version>1.0.0</version>
    </item>
    <item device="0x13a200409029bf" port="dio-0">
        <apikey>WhOKtmp8qTU_5-C8bl6JCrEQ_EeSAKxJV0lHNkkybzlsaz0g</apikey>
        <id>64451</id>
        <url>https://api.cosm.com/v2/feeds/{}.json</url>
        <title>Garage</title>
        <exposure>indoor</exposure>
        <domain>physical</domain>
        <disposition>fixed</disposition>
        <status>frozen</status>
        <private>false</private>
        <tags>Door</tags>
        <cosm_channel>0</cosm_channel>
        <creator>https://cosm.com/users/{}</creator>
        <latitude>30.3351807498968</latitude>
        <longitude>-97.7104604244232</longitude>
        <email>gary_pickens@yahoo.com</email>
        <max_value>1</max_value>
        <min_value>0</min_value>
        <version>1.0.0</version>
    </item>
</cosm>
'''
