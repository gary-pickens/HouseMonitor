'''
Created on Aug 5, 2012

@author: Gary
'''
from configuration.xmlconfiguration import XmlConfiguration
from lib.common import Common
from outputs.ioutput import iOutput
from pubsub import pub
import datetime
import os



class Log( iOutput, XmlConfiguration ):
    '''
    Log values to a file
    '''
    os = None

    # configuration varables
    filename = None
    directory = None
    rotate = None
    maxsize = None
    elements_to_read = ['filename', 'directory']

#    log_file_path = ""

    def __init__( self ):

        # Read the configuuration settings i.e. filename and directory
        # is directory does not exit use the base name of the executing
        # module appended with 'log'.
        self.configure()

        # open the file that will be written to
        log_file_path = os.path.join( self.config['directory'],
                                     self.config['filename'] )
        self.os = open( log_file_path, 'a' )

        iOutput.__init__( self )

    @property
    def topic_name( self ):
        return "output.log"

    @property
    def config_topic_name( self ):
        return 'config.log'

    @property
    def log_file_name( self ):
        return __name__

    def output( self, value, data, listeners ):
        '''
        This routine will output a log of data that it receives

        Args:
            value: the value for the data
            data: more information about the value
            listeners:  the various listeners for this object

        Return:
            the string that is printed

        Execptions:
            None
        '''
        name = data['Name']
        date = data['date time received']

        line = "{:25.25s} {} {}{}".format( name, date, value, os.linesep )

        self.os.write( line )
        try:
            Common.send( value=value, data=data, listeners=listeners )
        except pub.ListenerInadequate as li:
            self.logger.exception( 'Common.send exception: {}'.format( li ) )
        except Exception as ex:
            self.logger.exception( 'Common.send exception: {}'.format( ex ) )

        return line

    def configure( self ):
        self.read_xml_configuration( self.elements_to_read, __name__ )
