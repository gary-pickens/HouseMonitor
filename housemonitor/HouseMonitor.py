#!/usr/bin/python
'''
Created on Sep 10, 2012

@author: gary
'''
from datetime import datetime
import time
import logging.config
import sys
import os
from pprint import pprint
from pubsub import pub
from optparse import OptionParser

from housemonitor.inputs.computermonitor.computermonitor import ComputerMonitor
from housemonitor.inputs.processinput import ProcessInput, abcProcessInput, ProcessXBeeInput
from housemonitor.inputs.testinputthead import TestInputThread
from housemonitor.inputs.zigbeeinput.xbeeinputthread import XBeeInputThread
from housemonitor.lib.base import Base
from housemonitor.lib.constants import Constants
from housemonitor.lib.currentvalues import CurrentValues
from housemonitor.lib.hmqueue import HMQueue
from housemonitor.lib.hmscheduler import HMScheduler, HMScheduler
from housemonitor.lib.moduleloader import ModuleLoader
from housemonitor.lib.pubsubaid import PubSubAid
from housemonitor.outputs.cosm.control import COSMControl
from housemonitor.outputs.xmlrpc.control import XMLRPCControl
from housemonitor.outputs.zigbee.zigbeecontrol import ZigBeeControl
import housemonitor
from housemonitorinfo import ( HouseMonitorAuthor, HouseMonitorBuildDate,
                              HouseMonitorEmail,
                              HouseMonitorTitle, HouseMonitorVersion )


class HouseMonitor():
    '''
    House Monitor is the main program responsible for starting the housemonitor system.  It preforms the the following
    functions:

    1. Set up logging
    2. Print out start message
    3. Parse and set option passed in form the command line
    4. Sets up data that will be available to the rest of the system
    5. Loads all the modules that are in the directory steps
    6. Starts COSM for communicating with COSM.
    7. Starts XMLRPC.
    8. Starts
    '''

    logger = None
    options = None
    args = None

    input = None
    input_queue = None
    test_input = None
    xbee_thread = None
    sched = None

    moduleloader = None
    cosm = None
    xmlrpc = None
    zigbee = None
    pubAid = None

    def __init__( self ):

        logging.config.fileConfig( "house_monitor_logging.conf" )
        self.logger = logging.getLogger( 'HouseMonitor' )

        self.print_start_message()
        self.parse_options()

    def print_start_message( self ):

        self.logger.info( '{:^30}'.format( HouseMonitorTitle ) )
        self.logger.info( '' )
        self.logger.info( 'author:             ' + HouseMonitorAuthor )
        self.logger.info( 'email:              ' + HouseMonitorEmail )
        self.logger.info( 'version:            ' + HouseMonitorVersion )
        self.logger.info( 'date built:         ' + HouseMonitorBuildDate )
        self.logger.info( '' )

    def parse_options( self ):
        Options = OptionParser()
        Options.add_option( "-d",
                           action="store_false",
                           dest="display_data",
                           default=True )
        Options.add_option( "-r",
                           action="store_true",
                           dest="display_response",
                           default=False,
                           help="display the data that is received" )
        Options.add_option( "-j",
                           action="store_true",
                           dest="display_json",
                           default=False,
                           help="display the json that is produced" )
        Options.add_option( "--http",
                           action="store_const",
                           default=False,
                           const=0,
                           dest="http2lib_debug_level",
                           help="Set the debug level for http2lib" )
        Options.add_option( "--test",
                           action="store_true",
                           default=False,
                           dest="in_test_mode",
                           help="Run in test mode. (Don't start XBee thread, start test thread. Don't send reports to COSM)" )
        ( self.options, self.args ) = Options.parse_args()

    def startInputs( self, global_data ):
        ''' Start Home Monitor Input routines '''

        input_queue = global_data[Constants.GlobalData.INPUT_QUEUE]
        self.input = ProcessInput( input_queue )

        # Start thread for inputing data
        if ( not self.options.in_test_mode ):
            self.logger.debug( 'Starting xbee input' )
            self.xbee_thread = XBeeInputThread( input_queue )
            self.xbee_thread.start()

        # The following will test various inputs
        if ( self.options.in_test_mode ):
            self.logger.debug( 'Starting test thread' )
            self.test_input = TestInputThread( input_queue )
            self.test_input.start()

        self.logger.debug( 'Starting scheduler' )
        self.sched = HMScheduler( self.input_queue )
        self.sched.start()

        if ( sys.platform[:5] == 'linux' ):
            self.logger.debug( 'Starting ComputerMonitor' )
            self.computer_monitor = ComputerMonitor( input_queue )
            self.computer_monitor.start()

    def startOutputs( self, global_data ):

        self.logger.debug( 'Start output communications to COSM' )
        self.cosm = COSMControl()
        self.cosm.startCOSM( self.options )

        self.logger.debug( 'Start the XML RPC server' )
        self.xmlrpc = XMLRPCControl( global_data[Constants.GlobalData.CURRENT_VALUES],
                                     global_data[Constants.GlobalData.INPUT_QUEUE],
                                     global_data[Constants.GlobalData.OPTIONS] )
        self.xmlrpc.startXMLRPC( self.options )

        self.logger.debug( 'Start output communications with ZigBee' )
        self.zigbee = ZigBeeControl()
        self.zigbee.startZigBee( self.options )

    def run( self ):

        self.logger.debug( 'Setting up global_data for communications between different part of the system' )
        global_data = {}
        global_data[Constants.GlobalData.CURRENT_VALUES] = CurrentValues()
        global_data[Constants.GlobalData.OPTIONS] = self.options
        global_data[Constants.GlobalData.ARGS] = self.args
        global_data[Constants.GlobalData.START_TIME] = datetime.utcnow()
        global_data[Constants.GlobalData.INPUT_QUEUE] = HMQueue( "Input" )

        self.module_loader = ModuleLoader()
        self.module_loader.load( global_data )

        self.startOutputs( global_data )

        self.startInputs()

        self.pubAid = PubSubAid()

        # Endless loop will never return
        self.input.input()

        self.logger.debug( "Exiting" )

if __name__ == "__main__":
    HouseMonitor().run()
