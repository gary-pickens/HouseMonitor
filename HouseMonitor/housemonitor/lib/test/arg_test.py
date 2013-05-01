'''
Created on Apr 30, 2013

@author: Gary
'''
import unittest


class Test( unittest.TestCase ):



    def printArg1( self, arg1, arg2, arg3 ):
        print arg1
        print arg2
        print arg3

    def printArg2( self, *arg ):
        print arg[0]
        print arg[1]
        print arg[2]

    def printArg3( self, *arg ):
        for a, b in enumerate( arg ):
            print a, b

    def printArg4( self, one, two, three ):
        print one
        print two
        print three

    def printArg5( self, *arg ):
        for a, b in enumerate( arg ):
            print a, b

    def test_arg( self ):

        arg = ( '1', '2', '3' )

        print '1 ************************'
        self.printArg1( *arg )

        print '2 ************************'
        self.printArg2( *arg )

        print '3 ************************'
        self.printArg3( *arg )

        print '4 ************************'
        self.printArg4( *arg )

        print '5 ************************'
        self.printArg5( 1, 2, 3 )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_arg']
    unittest.main()
