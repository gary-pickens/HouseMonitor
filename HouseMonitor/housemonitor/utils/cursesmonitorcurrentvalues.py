'''
Created on Apr 9, 2013

@author: Gary
'''
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
import curses

class CursesMonitorCurrentValues( object ):

    proxy = None
    options = None

    def __init__( self, proxy, options ):
        super( CursesMonitorCurrentValues, self ).__init__()
        self.proxy = proxy
        self.options = options

    def output_values( self ):
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad( 1 )
        curses.halfdelay( 40 )
        value = {}
        try:
            while True:
                value = self.proxy.get_current_values()
                stdscr.addstr( 0, 60, 'uptime' )
                stdscr.addstr( 0, 70, value['HouseMonitor']['uptime']['current_value'] )

                line = 2
                for device in sorted( value ):
                    if not device.startswith( 'HouseMonitor' ):
                        fake_device = device
                        for port in sorted( value[device] ):
                            if port == 'uptime':
                                break
                            fake_port = port
                            for report in value[device][port]:
                                if 'current_value' in value[device][port]:
                                    cv = value[device][port]['current_value']
                                else:
                                    dt = '-'
                                if 'at' in value[device][port]:
                                    at = value[device][port]['at']
                                else:
                                    at = '-'
                            stdscr.addstr( line, 0, fake_device )
                            stdscr.addstr( line, 50, fake_port )
                            stdscr.addstr( line, 60, str( cv ).ljust( 9 ) )
                            stdscr.addstr( line, 70, str( at ) )
                            line = line + 1
                            fake_port = ''
                            fake_device = ''
                        line = line + 1
                stdscr.refresh()
                try:
                    c = stdscr.getch()
                    stdscr.refresh()
                    if ( c == ord( 'q' ) ):
                        curses.endwin()
                        quit()
                except curses.error:
                    pass
        except Exception as ex:
            curses.endwin()
            print( "exception {}".format( ex ) )
            quit()
