'''
Created on Apr 30, 2013


@author: Gary
'''
import unittest
from housemonitor.lib.constants import Constants


class Test( unittest.TestCase ):


    def header( self, title, doc ):
        print( '{:*^60}'.format( '' ) )
        print( '{:^60}'.format( title ) )
        print( '{:60}'.format( doc ) )
        print( '{:*>60}'.format( '' ) )
        print

    def footer( self ):
        print( '{:*^60}'.format( '' ) )
        print
        print

    def printArg1( self, arg1, arg2, arg3 ):
        '''
        Make a call with 
        
        arg = ( '1', '2', '3' )
        self.printArg1( *arg )
        
        and the function is 
        
        def printArg1( self, arg1, arg2, arg3 )
            print arg1
            print arg2
            print arg3
        
        '''
        self.header( "printArg1", self.printArg1.__doc__ )
        print arg1
        print arg2
        print arg3
        self.footer()


    def printArg2( self, *arg ):
        '''
        Make a call with 
        
        arg = ( '1', '2', '3' )
        printArg2( self, *arg )
        
        and the function is 
        
        def self.printArg2( *arg )
            print arg[0]
            print arg[1]
            print arg[2]
        '''
        self.header( "printArg2", self.printArg2.__doc__ )
        print arg[0]
        print arg[1]
        print arg[2]
        self.footer()

    def printArg3( self, *arg ):
        '''
        Make a call with 
        
        arg = ( '1', '2', '3' )
        def printArg3( self, *arg ):
        
        and the function is 
        
        def self.printArg3( *arg )
            for a, b in enumerate( arg ):
                print( '{:<2} {:>5}'.format( a, b ) )
        '''
        self.header( "printArg3", self.printArg3.__doc__ )
        for a, b in enumerate( arg ):
            print( '{:<2} {:>5}'.format( a, b ) )
        self.footer()

    def printArg4( self, one, two, three ):
        '''
        Make a call with 
        
        arg = ( '1', '2', '3' )
        printArg4( self, *arg ):
        
        and the function is 
        
        def self.printArg4( one, two, three  )
            print one
            print two
            print three
        '''
        self.header( "printArg4", self.printArg4.__doc__ )
        print one
        print two
        print three
        self.footer()

    def printArg5( self, *arg ):
        '''
        Make a call with 
        
        printArg4( 1, 2, 3 ):
        
        and the function is 
        
        def self.printArg5( *arg )
            for a, b in enumerate( arg ):
                print( '{:<2} {:>5}'.format( a, b ) )
        '''
        self.header( "printArg5", self.printArg5.__doc__ )
        for a, b in enumerate( arg ):
            print( '{:<2} {:>5}'.format( a, b ) )
        self.footer()

    def test_arg( self ):

        arg = ( '1', '2', '3' )

        self.printArg1( *arg )

        self.printArg2( *arg )

        self.printArg3( *arg )

        self.printArg4( *arg )

        self.printArg5( 1, 2, 3 )

    def printKWargs1( self, **kwargs ):
        '''
        Make a call with 
        
        kwargs = {Constants.DataPacket.device: 'xbee',
                  Constants.DataPacket.port: 'DA1'}
        self.printKWargs1( **kwargs )
        
        and the function is 
        
        def printKWargs1( self, **kwargs ):
            print kwargs['device']
            print kwargs['port']
        
        '''
        self.header( "printKWargs1", self.printKWargs1.__doc__ )

        print kwargs['device']
        print kwargs['port']
        self.footer()

    def printKWargs2( self, device, port ):
        '''
        Make a call with 
        
        kwargs = {Constants.DataPacket.device: 'xbee',
                  Constants.DataPacket.port: 'DA1'}
        self.printKWargs1( **kwargs )
        
        and the function is 
        
        def printKWargs2( self, device, port ):
            print device
            print port
        
        '''
        self.header( 'printKWargs2', self.printKWargs2.__doc__ )
        print device
        print port
        self.footer()


    def printKWargs3( self, device, port, name ):
        '''
        Make a call with 
        
        kwargs = {Constants.DataPacket.device: 'xbee',
                  Constants.DataPacket.port: 'DA1'}
        self.printKWargs3( **kwargs )
        
        and the function is 
        
        def printKWargs3( self, device, port, name ):
            print device
            print port
            print name
        
        '''
        self.header( "printKWargs3", self.printKWargs2.__doc__ )
        print device
        print port
        print name
        self.footer()

# Does not work
#     def printKWargs4( self, Constants.DataPacket.device,
#                       Constants.DatePacket.port,
#                       Constants.DatePacket.name ):
#         '''
#         Make a call with
#
#         kwargs = {Constants.DataPacket.device: 'xbee',
#                   Constants.DataPacket.port: 'DA1'}
#         self.printKWargs3( **kwargs )
#
#         and the function is
#
#         def printKWargs3( self, device, port, name ):
#             print device
#             print port
#             print name
#
#         '''
#         self.header( self.printKWargs2.__doc__ )
#         print Constants.DataPacket.device
#         print Constants.DatePacket.port
#         print Constants.DatePacket.name
#         self.footer()

    def printKWargs5( self, **kwargs ):
        '''
        Make a call with 
        
        self.printKWargs1( device='device', port='port' )
        
        and the function is 
        
        def printKWargs5( self, **kwargs ):
            print kwargs['device']
            print kwargs['port']
        
        '''
        self.header( "printKWargs5", self.printKWargs1.__doc__ )
        print kwargs['device']
        print kwargs['port']
        self.footer()


    def printKWargs6( self, **kwargs ):
        '''
        Make a call with 
        
        self.printKWargs6( device='device', port='port' )
        
        and the function is 
        
        def printKWargs5( self, **kwargs ):
            return kwargs
        
        '''
        return kwargs

    def printKWargs7( self, **kwargs ):
        '''
        Make a call with 
        
        self.printKWargs7( device='device', port='port' )
        
        and the function is 
        
        def printKWargs7( self, **kwargs ):
            printKWargs8( **kwargs )
            printKWargs9( **kwargs )
        
        '''
        self.header( "printKWargs7", self.printKWargs9.__doc__ )
        self.printKWargs8( **kwargs )
        self.printKWargs9( **kwargs )

    def printKWargs8( self, **kwargs ):
        '''
        Make a call with 
        
        self.printKWargs8( **kwargs )
        
        and the function is 
        
        def printKWargs8( self, **kwargs ):
            print kwargs['device']
            print kwargs['port']
        
        '''
        self.header( "printKWargs8", self.printKWargs8.__doc__ )
        print kwargs['device']
        print kwargs['port']
        self.footer()

    def printKWargs9( self, device, port ):
        '''
        Make a call with 
        
        self.printKWargs9( **kwargs' )
        
        and the function is 
        
        def printKWargs9( self, device, port ):
            print device
            print port
        
        '''
        self.header( "printKWargs9", self.printKWargs9.__doc__ )
        print device
        print port
        self.footer()

    def test_kwargs( self ):

        kwargs = {Constants.DataPacket.device: 'xbee',
                  Constants.DataPacket.port: 'DA1'}

        self.printKWargs1( **kwargs )

        self.printKWargs2( **kwargs )

#         kwargs['name'] = 'printer'
#
#         self.printKWargs2( **kwargs )

        kwargs['name'] = 'printer'

        self.printKWargs3( **kwargs )

#        self.printKWargs4(**kwargs)

        self.printKWargs5( device='device', port='port' )

        data = self.printKWargs6( device='device name', port='port name' )
        self.header( "printKWargs5", self.printKWargs6.__doc__ )
        print data['device']
        print data['port']
        self.footer()

        data = self.printKWargs7( device='device name', port='port name' )

        self.printKWargs8( device='device name 2', port='port name 2' )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_arg']
    unittest.main()
