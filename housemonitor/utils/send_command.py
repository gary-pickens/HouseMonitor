#!/usr/local/bin/python2.7
# encoding: utf-8
'''
utils.send_command -- This script will send AT command to the specified XBee.

utils.send_command is a description

It defines classes_and_methods

@author:     Gary Pickens
        
@copyright:  2013 Gary Pickens. All rights reserved.
        
@license:    license

@contact:    gary_pickens@yahoo.com
@deffield    updated: Updated
'''

import sys
import os
import time

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from xbee_command import XBeeCommand

__all__ = []
__version__ = 0.1
__date__ = '2013-09-26'
__updated__ = '2013-09-26'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError( Exception ):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__( self, msg ):
        super( CLIError ).__init__( type( self ) )
        self.msg = "E: %s" % msg
    def __str__( self ):
        return self.msg
    def __unicode__( self ):
        return self.msg

def main( argv=None ):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend( argv )

    program_name = os.path.basename( sys.argv[0] )
    program_version = "v%s" % __version__
    program_build_date = str( __updated__ )
    program_version_message = '%%(prog)s %s (%s)' % ( program_version, program_build_date )
    program_shortdesc = __import__( '__main__' ).__doc__.split( "\n" )[1]
    program_license = '''%s

  Created by Gary Pickens on %s.
  Copyright 2013 Gary Pickens. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % ( program_shortdesc, str( __date__ ) )

    try:

        # Setup argument parser
        parser = ArgumentParser()
        parser.add_argument( "-n", "--host", dest="host", action="store", default='housemonitor', help="computer that is running HouseMonitor" )
        parser.add_argument( "-d", "--device", dest="device", action="store", default='0x13a200408baf45', help="The xbee device number" )
        parser.add_argument( "-z", "--sleep", dest="sleep", type=int, default=1, action="store", help="Time to sleep between commands" )
        parser.add_argument( "-c", "--count", dest="count", type=int, default=10, action="store", help="number of times to send the command" )
        parser.add_argument( "-a", "--at", dest="command", default="SH", action="store", help="AT command to send to XBee" )
        parser.add_argument( "-p", "--port", dest="port", default="DIO-1", action="store", help="port on the XBee" )

        parser.add_argument( "-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]" )
        parser.add_argument( '-V', '--version', action='version', version=program_version_message )

        # Process arguments
        args = parser.parse_args()

        host = args.host
        verbose = args.verbose
        count = args.count
        sleep = args.sleep
        device = args.device
        port = args.port
        command = args.command

        cmd = XBeeCommand( host )

        while count:
            cmd.change_dio( True, device, "DIO-1", ["step.ZigBeeOutput"] )
            cmd.change_dio( True, device, "DIO-2", ["step.ZigBeeOutput"] )
            cmd.change_dio( True, device, "DIO-3", ["step.ZigBeeOutput"] )
            print "lights on"
            time.sleep( sleep )
            cmd.change_dio( False, device, "DIO-1", ["step.ZigBeeOutput"] )
            cmd.change_dio( False, device, "DIO-2", ["step.ZigBeeOutput"] )
            cmd.change_dio( False, device, "DIO-3", ["step.ZigBeeOutput"] )
            print "lights off"
            time.sleep( sleep )
            count = count - 1
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise( e )
        indent = len( program_name ) * " "
        sys.stderr.write( program_name + ": " + repr( e ) + "\n" )
        sys.stderr.write( indent + "  for help use --help" )
        return 2

if __name__ == "__main__":
    if DEBUG:
#         sys.argv.append( "-h" )
#         sys.argv.append( "-v" )
#         sys.argv.append( "-r" )
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'utils.send_command_profile.txt'
        cProfile.run( 'main()', profile_filename )
        statsfile = open( "profile_stats.txt", "wb" )
        p = pstats.Stats( profile_filename, stream=statsfile )
        stats = p.strip_dirs().sort_stats( 'cumulative' )
        stats.print_stats()
        statsfile.close()
        sys.exit( 0 )
    sys.exit( main() )
