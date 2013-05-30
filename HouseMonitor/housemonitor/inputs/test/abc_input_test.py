'''
Created on Dec 18, 2012

@author: Gary
'''
from housemonitor.inputs.abc_input import abcInput

import unittest
import logging.config
from housemonitor.lib.constants import Constants
from mock import Mock, MagicMock, patch


class myInput( abcInput ):

    def input( self ):
        pass

    @property
    def logger_name( self ):
        return Constants.LogKeys.inputs

    @property
    def topic_name( self ):
        return Constants.TopicNames.UnitTest


class Test( unittest.TestCase ):

    logger = logging.getLogger( 'UnitTest' )

    def setUp( self ):
        logging.config.fileConfig( "unittest_logging.conf" )

    def tearDown( self ):
        pass

    def test_instantuating( self ):
        i = myInput()
        self.assertIsInstance( i, myInput )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()    # pragma: no cover
