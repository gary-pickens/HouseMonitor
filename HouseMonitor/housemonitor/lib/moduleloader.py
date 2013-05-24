'''
Created on Sep 17, 2012

@author: Gary
'''
import imp
import os
import sys
from sets import Set
import re
import inspect

from housemonitor.lib.base import Base
from housemonitor.configuration.xmlconfiguration import XmlConfiguration
from housemonitor.lib.getdatetime import GetDateTime


class ModuleLoader( Base ):
    '''
    classdocs
    '''
    # TODO: put directories in configuation file
    # A list of directories to search through for module that will be
    # instantiated.
    directories = ['steps']
    # A list of instantiated classes that have been loaded
    instances = []

    def __init__( self ):
        '''
        Constructor
        '''
        super( ModuleLoader, self ).__init__()

    @property
    def logger_name( self ):
        """ Set the logger level. This needs to be added to house_monitoring_logging.conf"""
        return 'lib'

    def file_name( self ):
        return __name__

    def load( self, data ):
        '''
        Walk though a directory and load all the *py* and *pyc* modules
        '''
        # use a set to insure that no two files are loaded twice
        names = Set()

        for directory in self.directories:
            for root, dirs, files in os.walk( directory ):
                for filename in files:
                    # Get just the file name - no extension
                    name, ext = os.path.splitext( filename )
                    # and to names which will prevent doubles
                    names.add( name )
                for name in names:
                    f = filename = description = package = None
                    continue_processing = True
                    try:
                        f, filename, description = imp.find_module( name, \
                                                            self.directories )
                    except ImportError as er:
                        self.logger.error( "error finding {}: error is {}"  \
                                                            .format( name, er ) )
                        continue_processing = False

                    # Check if we failed.  If so then jump to the beginning
                    # and start next file
                    if ( not continue_processing ):
                        continue

                    try:
                        package = imp.load_module( name, f, filename, description )
                    except ImportError as ex:
                        self.logger.error( "error importing {}: error is {}".\
                                                            format( name, ex ) )
                        continue_processing = False
                    finally:
                        if f:
                            self.close_file( f )

                    # Check if we failed.  If so then jump to the beginning
                    # and start next file
                    if ( not continue_processing ):
                        continue

                    try:
#                        pprint(inspect.getmembers(package))
#                        pprint(inspect.getsourcelines(package.instantuate_me))
                        instance = package.instantuate_me( data )
                        if ( None != instance ):
                            self.instances.append( instance )
                            self.logger.info( "Class {} instantiated".format( name ) )
                    except AttributeError as err:
                        self.logger.error( \
                        "The function \"instantiate_me\" was not found in {}: {}"\
                        .format( name, err ) )

    def close_file( self, f ):    # pragma: no cover
        # Module added for unit test
        f.close()    # pragma: no cover

    def get_class_name( self, package ):    # pragma: no cover
        # Module added for unit test
        return package.instantiate_me()    # pragma: no cover
