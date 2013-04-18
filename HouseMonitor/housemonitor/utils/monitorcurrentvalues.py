'''
Created on Oct 20, 2012

@author: Gary
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import time
import pprint
import os
from optparse import OptionParser
from datetime import datetime
import time


class Mon( object ):

    def curses_output( self, proxy, options ):
        from cursesmonitorcurrentvalues import CursesMonitorCurrentValues
        mon = CursesMonitorCurrentValues( proxy, options )
        mon.output_values()

    def raw_output( self, proxy, options ):
        from rawmonitorcurrentvalues import RawMonitorCurrentValues
        mon = RawMonitorCurrentValues( proxy, options )
        mon.output_values()

if __name__ == '__main__':

    print( "monitor current values" )
    print( "by Gary Pickens" )
    print( "Version 3.0.3" )
    print( datetime.now().isoformat() )

    display_mode = 'raw'

    Options = OptionParser()
    Options.add_option( "-p", '--port',
                       action="store",
                       dest="port",
                       default='9002' )
    Options.add_option( "--host",
                       action="store",
                       dest="host",
                       default='localhost',
                       help="Enter the URL of the server" )
    Options.add_option( '-t', '--time',
                       action="store",
                       dest="delay_time",
                       default=2.0,
                       type="float",
                       help="Iime to pause between updates" )
    Options.add_option( '-r', '--raw',
                       action="store_false",
                       dest="use_curses",
                       default=False,
                       help="Display raw data" )
    Options.add_option( '-c', '--curses',
                       action="store_true",
                       dest="use_curses",
                       default=True,
                       help="Use Curses to display data" )
    ( options, args ) = Options.parse_args()

    url = 'http://{}:{}'.format( options.host, options.port )
    print( url )
    while True:
        try:
            proxy = xmlrpclib.ServerProxy( url )
            mon = Mon()
            if options.use_curses:
                mon.curses_output( proxy, options )
            else:
                mon.raw_output( proxy, options )
            time.sleep( 10 )
        except Exception as ex:
            print ex
            time.sleep( 30 )
            exit()
