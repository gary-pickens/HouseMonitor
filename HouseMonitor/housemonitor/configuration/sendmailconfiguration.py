'''
Created on Sep 23, 2012

@author: Gary

'''
from housemonitor.lib.base import Base
from xmlconfiguration import XmlConfiguration
from housemonitor.lib.constants import Constants


class SendMailConfiguration( XmlConfiguration, dict ):
    """
    Read the send mail configuration file for sendmailthread.
    """
    config = {}

    def __init__( self, file_name='' ):
        super( SendMailConfiguration, self ).__init__()

    '''
    Make sure and enter the appropriate entry in the logging configuration
    file
    '''
    @property
    def logger_name( self ):
        ''' Set the logger level. '''
        return Constants.LogKeys.SendMail

    @property
    def configuration_file_name( self ):
        return __name__

    def __getitem__( self, device ):
        return self.config[device]

    def process_configuration( self, parent ):
        for child in parent:
            if ( child.tag == "list" ):
                if ( "name" in child.attrib ):
                    name = child.get( 'name' )
                    to = [x.strip() for x in child.text.split( ',' ) ]
                    self.config[name] = to
            if ( child.tag == "smtp_host" ):
                self.smtp_host = child.text
            if ( child.tag == "smtp_port" ):
                self.smtp_port = int( child.text )
            if ( child.tag == "require_login" ):
                self.require_login = bool( child.text )
            if ( child.tag == 'from_address' ):
                self.from_address = child.text
            if ( child.tag == 'password' ):
                self.password = child.text
            if ( child.tag == "smtp_host" ):
                self.smtp_host = child.text
            if ( child.tag == "debug_level" ):
                self.debug_level = int( child.text )
