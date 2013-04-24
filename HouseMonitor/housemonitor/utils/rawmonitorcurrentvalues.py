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

class RawMonitorCurrentValues( object ):

    proxy = None
    options = None

    def __init__( self, proxy, options ):
        super( RawMonitorCurrentValues, self ).__init__()
        self.proxy = proxy
        self.options = options

    def output_values( self ):
        while True:
            try:
                value = self.proxy.get_current_values()
#                pprint.pprint( value )
                os.system( ['clear', 'cls'][os.name == 'nt'] )
                for device in value:
                    fake_device = device
                    for port in value[device]:
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
                        print( '{:<50}{:<20}{:>15}   {:<30}'.format( fake_device, fake_port, cv, at ) )
                        fake_port = ''
                        fake_device = ''
                time.sleep( self.options.delay_time )
            except Exception as ex:
                print( ex )
                time.sleep( 10 )
                return
