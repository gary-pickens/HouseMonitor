'''
Created on Sep 2, 2013

@author: Gary
'''
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib

if __name__ == '__main__':
    host = '192.168.7.2'
    port = 9002
    proxy = None
    url = 'http://{}:{}'.format( host, port )
    print( url )
    proxy = xmlrpclib.ServerProxy( url )

    steps = ["step.ZigBeeOutput"]
    device = "0x13a20040902867"
    port = "dio-1"
    proxy.send_command( 1234, device, port, steps )
