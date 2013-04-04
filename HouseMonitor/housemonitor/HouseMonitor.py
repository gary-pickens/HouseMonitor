'''
Created on Sep 10, 2012

@author: gary
'''
from optparse import OptionParser
import logging.config
from datetime import datetime
from pubsub import pub


from lib.base import Base
from lib.moduleloader import ModuleLoader
from inputs.inputqueue import InputQueue
from inputs.zigbeeinput.xbeeinputthread import XBeeInputThread
from lib.hmscheduler import HMScheduler
# from inputs.zigbeeinput.xbeeinput import XbeeInput
from outputs.cosm.control import COSMControl
from outputs.zigbee.zigbeecontrol import ZigBeeControl
from inputs.testinputthead import TestInputThread
from inputs.processinput import ProcessInput, abcProcessInput, ProcessXBeeInput
from pprint import pprint
from lib.pubsubaid import PubSubAid
from outputs.xmlrpc.control import XMLRPCControl
from lib.currentvalues import CurrentValues
from lib.hmscheduler import HMScheduler
from lib.constants import Constants


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

    def __init__(self):

        logging.config.fileConfig("house_monitor_logging.conf")
        self.logger = logging.getLogger('HouseMonitor')

        self.print_start_message()
        self.parse_options()

    def print_start_message(self):
        self.logger.info("Monitor House")
        self.logger.info("by Gary Pickens")
        self.logger.info("Version 3.0.2")
        self.logger.info(datetime.now().isoformat())

    def parse_options(self):
        Options = OptionParser()
        Options.add_option("-d",
                           action="store_false",
                           dest="display_data",
                           default=True)
        Options.add_option("-r",
                           action="store_true",
                           dest="display_response",
                           default=False,
                           help="display the data that is received")
        Options.add_option("-j",
                           action="store_true",
                           dest="display_json",
                           default=False,
                           help="display the json that is produced")
        Options.add_option("--http",
                           action="store_const",
                           default=False,
                           const=0,
                           dest="http2lib_debug_level",
                           help="Set the debug level for http2lib")
        Options.add_option("--test",
                           action="store_true",
                           default=False,
                           dest="in_test_mode",
                           help="Run in test mode. (Don't start XBee thread, start test thread. Don't send reports to COSM)")
        (self.options, self.args) = Options.parse_args()

    def startInputs(self):
        ''' Start Home Monitor Input routines '''
        self.logger.info('Start the Input Queue')
        self.input_queue = InputQueue()

        self.input = ProcessInput(self.input_queue)

        # Start thread for inputing data
        if (not self.options.in_test_mode):
            self.logger.info('Starting xbee input')
            self.xbee_thread = XBeeInputThread(self.input_queue)
            self.xbee_thread.start()

        # The following will test various inputs
        if (self.options.in_test_mode):
            self.logger.info('Starting test thread')
            self.test_input = TestInputThread(self.input_queue)
            self.test_input.start()

        self.logger.info('Starting scheduler')
        self.sched = HMScheduler(self.input_queue)
        self.sched.start()

    def startOutputs(self, global_data):

        self.logger.info('Start output communications to COSM')
        self.cosm = COSMControl()
        self.cosm.startCOSM(self.options)

        self.logger.info('Start the XML RPC server')
        self.xmlrpc = XMLRPCControl(global_data)
        self.xmlrpc.startXMLRPC(self.options)

        self.logger.info('Start output communications with ZigBee')
        self.zigbee = ZigBeeControl()
        self.zigbee.startZigBee(self.options)

    def run(self):

        self.logger.info('Setting up global_data for communications between different part of the system')
        global_data = {}
        global_data['current values'] = CurrentValues()
        global_data['options'] = self.options
        global_data['args'] = self.args
        global_data['start time'] = datetime.utcnow()

        self.module_loader = ModuleLoader()
        self.module_loader.load(global_data)

        self.startOutputs(global_data)

        self.startInputs()

        self.pubAid = PubSubAid()

        # Endless loop will never return
        self.input.input()

        self.logger.info("Exiting")

if __name__ == "__main__":
    HouseMonitor().run()
